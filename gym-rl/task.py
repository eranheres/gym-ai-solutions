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


print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

ENV_NAME = "Acrobot-v1"
NUM_LAYERS = 2
UNITS_PER_LAYER = 20
MAX_MEMORY = 1000
BATCH_SIZE = 100
MAX_EPISODES = 100
MAX_STEPS = 10
FILE_NAME = "cart_pole_v1.h5"
MODEL_CLS = DenseModel
CHECKPOINT_EVERY = 10


def build_agent(env):
    # Initialize the agent
    model = MODEL_CLS()
    model.build_model(observation_space=env.observation_space,
                      action_space=env.action_space,
                      num_layers=NUM_LAYERS,
                      units_per_layer=UNITS_PER_LAYER)
    return Agent(action_space=env.action_space,
                 observation_space=env.observation_space,
                 model=model,
                 memory=BasicMemory(max_memory=MAX_MEMORY),
                 batch_size=BATCH_SIZE)


def train_model(env, agent, renderer):
    console_printer = ConsolePrinter(MAX_EPISODES)
    # First we train the model
    rl.train(env=env,
             agent=agent,
             max_episodes=MAX_EPISODES,
             max_steps=MAX_STEPS,
             callbacks=[renderer.callback, console_printer.callback])


def run(env, agent, renderer):
    rl.run(env, agent, callbacks=[])


def parse_command_line():
    parser = argparse.ArgumentParser(description='Run RL for gym CartPole-v1.')
    parser.add_argument('action', action="store", type=str, choices=['train', 'run'], help='action to perform')
    parser.add_argument('--load', dest='load', default=None, help='load from a file')
    parser.add_argument('--job-dir', type=str, default=".", help='local or GCS location for writing checkpoints')
    parser.add_argument('--save-render', action='store_false', help='save rendering output to a file')
    parser.add_argument('--headless', action='store_true', help='run headless mode')
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

    env = gym.make(ENV_NAME)
    agent = build_agent(env)
    uploader = None
    if args.save_render:
        uploader = GCPUploader(job_dir) if args.headless else LocalUploader('export')
    renderer = Renderer(uploader=uploader, render_every=CHECKPOINT_EVERY)

    if args.headless:
        virtual_display()

    if load_file:
        agent.from_file(load_file)

    if do_train:
        train_model(env, agent, renderer)

    if do_test:
        run(env, agent, renderer)


if __name__ == "__main__":
    main()
