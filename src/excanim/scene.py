from __future__ import annotations

from pathlib import Path

from excanim.anim.base import Animation
from excanim.anim.easing import EasingFunc
from excanim.elements.base import Element
from excanim.render.bridge import elements_to_svg
from excanim.timeline import Timeline


class Scene:
    def __init__(self, width: int = 800, height: int = 600, fps: int = 60):
        self._elements: dict[str, Element] = {}
        self._timeline = Timeline()
        self._clock: float = 0.0
        self._frames: list[list[dict]] | None = None
        self.width = width
        self.height = height
        self.fps = fps

    def add(self, *elements: Element):
        for el in elements:
            self._elements[el.id] = el

    def play(self, *animations: Animation, duration: float | None = None, easing: EasingFunc | None = None):
        max_dur = 0.0
        for anim in animations:
            if duration is not None:
                anim.duration = duration
            if easing is not None:
                anim.easing = easing
            if anim.target.id not in self._elements:
                self._elements[anim.target.id] = anim.target
            keyframes = anim.resolve(self._clock)
            self._timeline.add(*keyframes)
            max_dur = max(max_dur, anim.duration)
            for kf in keyframes:
                setattr(self._elements[kf.element_id], kf.prop, kf.val_end)
        self._clock += max_dur

    def wait(self, seconds: float = 1.0):
        self._clock += seconds

    def capture(self):
        """Snapshot current element state as a frame (for simulation mode)."""
        if self._frames is None:
            self._frames = []
        from excanim.render.frames import _make_canvas_anchor
        frame = [_make_canvas_anchor(self.width, self.height)]
        for el in self._elements.values():
            frame.extend(el.to_excalidraw_list())
        self._frames.append(frame)

    def construct(self):
        raise NotImplementedError("Subclass Scene and implement construct()")

    def simulate(self):
        raise NotImplementedError("Subclass Scene and implement simulate()")

    def _build(self):
        self._frames = None
        try:
            self.simulate()
        except NotImplementedError:
            self.construct()

    def render(self, path: str, fps: int | None = None):
        target_fps = fps or self.fps
        self._build()
        out = Path(path)
        ext = out.suffix.lower()

        if ext == ".svg":
            self._render_svg(out)
        elif ext == ".excalidraw":
            self._render_excalidraw(out)
        elif ext in (".mp4", ".gif", ".webm"):
            self._render_video(out, target_fps)
        else:
            raise ValueError(f"Unsupported output format: {ext}")

    def _all_element_dicts(self) -> list[dict]:
        result = []
        for el in self._elements.values():
            result.extend(el.to_excalidraw_list())
        return result

    def _render_svg(self, out: Path):
        svg = elements_to_svg(self._all_element_dicts())
        out.write_text(svg)

    def _render_excalidraw(self, out: Path):
        import json
        data = {
            "type": "excalidraw",
            "version": 2,
            "source": "excanim",
            "elements": self._all_element_dicts(),
            "appState": {"viewBackgroundColor": "#ffffff"},
            "files": {},
        }
        out.write_text(json.dumps(data, indent=2))

    def _render_video(self, out: Path, fps: int):
        from excanim.render.frames import render_frames
        from excanim.render.bridge import batch_elements_to_svg
        from excanim.render.video import frames_to_video

        if self._frames:
            svgs = batch_elements_to_svg(self._frames)
            frames_to_video(svgs, out, fps)
        else:
            svgs, draw_effects, frame_ids = render_frames(self._elements, self._timeline, fps, self.width, self.height)
            frames_to_video(svgs, out, fps, draw_effects=draw_effects, frame_element_ids=frame_ids)
