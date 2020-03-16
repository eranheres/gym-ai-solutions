import gym
from agent import Agent
from models import DenseModel
from memories import BasicMemory
import rl
import argparse

ENV_NAME = "CartPole-v1"
NUM_LAYERS = 2
UNITS_PER_LAYER = 20
MAX_MEMORY = 1000
BATCH_SIZE = 100
MAX_EPISODES = 500
MAX_STEPS = 1000
FILE_NAME = "cart_pole_v1.h5"
MODEL_CLS = DenseModel


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


def train_model(env, agent):
    # First we train the model
    rl.train(env, agent, max_episodes=MAX_EPISODES, max_steps=MAX_STEPS)


def run(env, agent):
    rl.run(env, agent)


def parse_command_line():
    parser = argparse.ArgumentParser(description='Run RL for gym CartPole-v1.')
    parser.add_argument('action', action="store", type=str, help='action to perform [train, run]')
    parser.add_argument('--load', dest='load', default=None, help='load from a file')
    return parser.parse_args()


def main():
    args = parse_command_line()

    do_train = args.action == 'train'
    do_test = args.action == 'run'
    load_file = args.load

    if not do_test and not do_train:
        print("Mode of operation must be selected, %s is unknown" % {args.action})
        exit(-1)

    env = gym.make(ENV_NAME)
    agent = build_agent(env)

    if load_file:
        agent.from_file(load_file)

    if do_train:
        train_model(env, agent)

    if do_test:
        run(env, agent)


if __name__ == "__main__":
    main()
