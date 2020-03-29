import gym
from .agent import Agent
from .models import DenseModel
from .memories import BasicMemory
from . import rl
from .renderer import Renderer
from .uploaders import GCPUploader, LocalUploader
from .console_printer import ConsolePrinter
import argparse
import sys
import os
import json
from datetime import datetime

MODEL_CLS = DenseModel

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))


def read_config(config_file):
    with open(config_file) as json_data_file:
        data = json.load(json_data_file)
    return data


def build_agent(env, dqn_config):
    # Initialize the agent
    model = MODEL_CLS()
    model.build_model(observation_space=env.observation_space,
                      action_space=env.action_space,
                      num_layers=dqn_config["network"]["layers"],
                      units_per_layer=dqn_config["network"]["units_per_layer"])
    return Agent(action_space=env.action_space,
                 observation_space=env.observation_space,
                 model=model,
                 memory=BasicMemory(max_memory=dqn_config["memory_size"]),
                 batch_size=dqn_config["batch_size"])


def train_model(env, agent, renderer, config):
    console_printer = ConsolePrinter(config["max_episodes"])
    # First we train the model
    rl.train(env=env,
             agent=agent,
             max_episodes=config["max_episodes"],
             max_steps=config["max_steps"],
             callbacks=[renderer.callback, console_printer.callback])


def run(env, agent, renderer):
    rl.run(env, agent, callbacks=[])


def parse_command_line():
    parser = argparse.ArgumentParser(description='Run RL for gym CartPole-v1.')
    parser.add_argument('action', action="store", type=str, choices=['train', 'run'], help='action to perform')
    parser.add_argument('config', type=str, help='json config file')
    parser.add_argument('--load', default=None, help='load from a file')
    parser.add_argument('--job-dir', type=str, default=".", help='local or GCS location for writing checkpoints')
    parser.add_argument('--save-render', action='store_true', help='save rendering output to a file')
    parser.add_argument('--gcp', action='store_true', help='run on GCP')

    return parser.parse_args()


def virtual_display():
    from pyvirtualdisplay import Display
    virtual_display = Display(visible=0, size=(1400, 900))
    virtual_display.start()


def write_file(path, filename):
    file = open(os.path.join(path, filename), "w")
    file.write("Hello World")
    file.close()


def main():
    args = parse_command_line()

    do_train = args.action == 'train'
    do_test = args.action == 'run'
    load_file = args.load
    job_dir = args.job_dir
    run_on_gcp = args.gcp
    config_file = args.config

    config = read_config(config_file)

    env = gym.make(config["environment"])
    agent = build_agent(env, config["dqn"])
    uploader = None
    if args.save_render:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        if run_on_gcp:
            print("Initalizing GCP Uploader")
            uploader = GCPUploader(os.path.join(job_dir))
        else:
            print("Initalizing local Uploader")
            uploader = LocalUploader(os.path.join('export', config['environment'], now))
    renderer = Renderer(uploader=uploader, render_every=config["render_every"], save_every=config["checkpoint_every"])

    if run_on_gcp:
        print("Initalizing virtual display")
        virtual_display()

    if load_file:
        agent.from_file(load_file)

    if do_train:
        train_model(env, agent, renderer, config)

    if do_test:
        run(env, agent, renderer)


if __name__ == "__main__":
    main()
