import numpy as np
from .callbacks import CALLBACK_STATE


def train(env, agent, max_episodes, max_steps, callbacks=[]):
    for episode in range(max_episodes):
        [callback(CALLBACK_STATE.PRE_EPISODE, env, None) for callback in callbacks]
        losses = []
        observation = env.reset()
        for step in range(max_steps):
            [callback(CALLBACK_STATE.PRE_STEP, env, None) for callback in callbacks]
            action = agent.action(observation)
            next_observation, reward, done, info = env.step(action)
            loss = agent.learn(
                observation=observation,
                action=action,
                reward=reward,
                done=done,
                next_observation=next_observation,
                info=info)
            agent.decay_epsilon()
            losses.append(loss)
            observation = next_observation
            [callback(CALLBACK_STATE.POST_STEP, env, None) for callback in callbacks]
            if done:
                break
        loss = np.average(losses)
        [callback(CALLBACK_STATE.POST_EPISODE, env, loss) for callback in callbacks]
    env.close()


def run(env, agent, callbacks=[]):
    observation = env.reset()
    done = False
    step = 0
    [callback(CALLBACK_STATE.PRE_EPISODE, 0, 0, "run", env) for callback in callbacks]
    while not done:
        [callback(CALLBACK_STATE.PRE_STEP, 0, step, "run", env) for callback in callbacks]
        action = agent.action(observation, exploration=False)
        observation, reward, done, info = env.step(action)
        if done:
            observation = env.reset()
        [callback(CALLBACK_STATE.POST_STEP, 0, step, "run", env) for callback in callbacks]
        step = step+1
    [callback(CALLBACK_STATE.POST_EPISODE, 0, 0, "run", env) for callback in callbacks]
    env.close()


