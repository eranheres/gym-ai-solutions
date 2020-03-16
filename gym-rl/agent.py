import random
import numpy as np
import math

MAX_EPISODES = 3000
MAX_EPSILON = 1
MIN_EPSILON = 0.005
LAMBDA = 0.0001
GAMMA = 0.99
LEARNING_RATE = 0.99


class Agent():
    def __init__(self, action_space, observation_space,  model, memory, batch_size, epsilon=1.):
        self._eps = epsilon
        self._action_space = action_space
        self._model = model
        self._memory = memory
        self._batch_size = batch_size
        self._steps_cnt = 0
        self._observation_space = observation_space

    def _obs_to_input(self, obs):
        return np.array(obs)

    def action(self, obs, exploration=True):
        if exploration and random.random() < self._eps:
            action = random.randint(0, self._action_space.n - 1)
        else:
            s = self._obs_to_input([obs])
            actions = self._model.predict_batch(s)
            action = np.argmax(actions[0])
        return action

    def decay_epsilon(self):
        self._steps_cnt += 1
        self._eps = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) * math.exp(-LAMBDA * self._steps_cnt)
        return self._eps

    def learn(self, observation, action, reward, done, info, next_observation):
        state = self._obs_to_input(observation)
        next_state = self._obs_to_input(next_observation)
        self._memory.add_sample((state, action, reward, next_state, done))
        return self._replay(self._memory.sample(self._batch_size))

    def _replay(self, batch):
        inputs = np.array([val[0] for val in batch])
        # predict Q(s,a) given the batch of states
        q_s_a = self._model.predict_batch(inputs)
        # predict Q(s',a') - so that we can do gamma * max(Q(s'a')) below
        zeros = np.zeros(self._observation_space.shape)
        next_states = np.array([zeros if val[4] else val[3] for val in batch])
        q_s_a_d = self._model.predict_batch(next_states)

        x = []
        y = []
        for i, b in enumerate(batch):
            state, action, reward, next_state, done = b
            current_q = q_s_a[i][0]
            new_rew = q_s_a[i]
            if done:
                new_rew[action] = reward
            else:
                max_rew = np.max(q_s_a_d[i])
                new_rew_val = current_q + LEARNING_RATE * (reward + (GAMMA * max_rew) - current_q)
                new_rew[action] = new_rew_val
            x.append(inputs[i])
            y.append(new_rew)

        return self._model.train_batch(np.array(x), np.array(y))

    def from_file(self, filename):
        self._model.from_file(filename)

    def save(self, filename):
        self._model.save(filename)

if __name__ == '__main__':
    pass

