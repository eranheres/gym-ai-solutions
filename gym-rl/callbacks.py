from enum import Enum


class CALLBACK_STATE(Enum):
    PRE_EPISODE = 1
    POST_EPISODE = 2
    PRE_STEP = 3
    POST_STEP = 4


def callback_print(state, episode, step, mode, env):
    if state == CALLBACK_STATE.PRE_EPISODE:
        print("==> Callback: Episode:%d " % (episode))

