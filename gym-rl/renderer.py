from moviepy.editor import ImageSequenceClip
from .callbacks import CALLBACK_STATE


class Renderer:
    def __init__(self, uploader, render_every=1, save_every=1):
        self._snapshots = []
        self._uploader = uploader
        self._render_every = render_every
        self._save_every = save_every
        self._episode = 0

    def _should_render(self):
        return self._episode % self._render_every == 0

    def _should_save(self):
        return self._uploader is not None and self._episode % self._save_every == 0

    def _reset(self):
        self._snapshots = []

    def _render(self, env):
        if not self._should_render():
            return
        s = env.render('rgb_array')
        if self._should_save():
            self._snapshots.append(s)

    def _close(self):
        if len(self._snapshots) == 0:
            return
        filename = 'render_' + str(self._episode) + '.gif'
        clip = ImageSequenceClip(self._snapshots, fps=30)
        source_folder = "/tmp/"
        local_filename = source_folder+filename
        print("writing file to:"+local_filename)
        clip.write_gif(local_filename, fps=30, logger=None)
        print("uploading file")
        self._uploader.upload(source_folder, filename)

    def callback(self, state, env, attr):
        if state == CALLBACK_STATE.PRE_EPISODE:
            self._reset()
        elif state == CALLBACK_STATE.POST_STEP:
            self._render(env)
        elif state == CALLBACK_STATE.POST_EPISODE:
            self._close()
            self._episode = self._episode + 1

