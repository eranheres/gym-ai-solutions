from moviepy.editor import ImageSequenceClip
from enum import Enum
from .callbacks import CALLBACK_STATE

class Renderer:
    class MODES(Enum):
        DISPLAY = 1
        GIF = 2

    def __init__(self, mode, uploader, render_every=1):
        self._snapshots = []
        self._mode = mode
        self._uploader = uploader
        self._render_every = render_every
        self._episode = 0

    def _should_render(self):
        return self._episode % self._render_every == 0

    def _reset(self):
        self._snapshots = []

    def _render(self, env):
        if not self._should_render():
            return
        s = env.render('human' if self._mode == Renderer.MODES.DISPLAY else 'rgb_array')
        if self._mode == self.MODES.GIF:
            self._snapshots.append(s)

    def _close(self):
        if self._mode != Renderer.MODES.GIF or len(self._snapshots) == 0:
            return
        filename = 'render_' + str(self._episode) + '.gif'
        clip = ImageSequenceClip(self._snapshots, fps=30)
        source_folder = "/tmp/"
        local_filename = source_folder+filename
        print("writing file to:"+local_filename)
        clip.write_gif(local_filename, fps=30)
        print("uploading file")
        self._uploader.upload(source_folder, filename)

    def callback(self, state, episode, step, mode, env):
        if state == CALLBACK_STATE.PRE_EPISODE:
            self._reset()
        if state == CALLBACK_STATE.POST_STEP:
            self._render(env)
        if state == CALLBACK_STATE.POST_EPISODE:
            self._close()
            self._episode = self._episode + 1

