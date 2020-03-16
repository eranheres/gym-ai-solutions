from .callbacks import CALLBACK_STATE
import time

class ConsolePrinter():
    def __init__(self, max_episodes):
        self._episode = 0
        self._step = 0
        self._max_episodes = max_episodes
        self._episode_start_time = 0

    def callback(self, state, env, attr):
        if state == CALLBACK_STATE.PRE_EPISODE:
            self._episode_start_time = time.time()
            self._step = 0
        elif state == CALLBACK_STATE.PRE_STEP:
            pass
        elif state == CALLBACK_STATE.POST_STEP:
            self._step += 1
        elif state == CALLBACK_STATE.POST_EPISODE:
            self._episode += 1
            duration = time.time() - self._episode_start_time
            print("==> episode:%d/%d(%.1fs) steps:%d loss:%.3f" %
                  (self._episode, self._max_episodes, duration, self._step, attr))


