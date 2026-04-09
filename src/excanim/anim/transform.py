from __future__ import annotations

from excanim.anim.base import Animation, KeyFrame
from excanim.anim.easing import EasingFunc, linear
from excanim.elements.base import Element


class MoveTo(Animation):
    def __init__(
        self,
        target: Element,
        x: float | None = None,
        y: float | None = None,
        duration: float = 1.0,
        easing: EasingFunc = linear,
    ):
        super().__init__(target, duration, easing)
        self._x = x
        self._y = y

    def resolve(self, t_start: float) -> list[KeyFrame]:
        kfs = []
        if self._x is not None:
            kfs.append(KeyFrame(
                element_id=self.target.id, prop="x",
                t_start=t_start, t_end=t_start + self.duration,
                val_start=self.target.x, val_end=self._x, easing=self.easing,
            ))
        if self._y is not None:
            kfs.append(KeyFrame(
                element_id=self.target.id, prop="y",
                t_start=t_start, t_end=t_start + self.duration,
                val_start=self.target.y, val_end=self._y, easing=self.easing,
            ))
        return kfs


class ScaleTo(Animation):
    def __init__(
        self,
        target: Element,
        sx: float = 1.0,
        sy: float = 1.0,
        duration: float = 1.0,
        easing: EasingFunc = linear,
    ):
        super().__init__(target, duration, easing)
        self._sx = sx
        self._sy = sy

    def resolve(self, t_start: float) -> list[KeyFrame]:
        cx = self.target.x + self.target.width / 2
        cy = self.target.y + self.target.height / 2
        new_w = self.target._base_width * self._sx
        new_h = self.target._base_height * self._sy
        new_x = cx - new_w / 2
        new_y = cy - new_h / 2

        return [
            KeyFrame(element_id=self.target.id, prop="width",
                     t_start=t_start, t_end=t_start + self.duration,
                     val_start=self.target.width, val_end=new_w, easing=self.easing),
            KeyFrame(element_id=self.target.id, prop="height",
                     t_start=t_start, t_end=t_start + self.duration,
                     val_start=self.target.height, val_end=new_h, easing=self.easing),
            KeyFrame(element_id=self.target.id, prop="x",
                     t_start=t_start, t_end=t_start + self.duration,
                     val_start=self.target.x, val_end=new_x, easing=self.easing),
            KeyFrame(element_id=self.target.id, prop="y",
                     t_start=t_start, t_end=t_start + self.duration,
                     val_start=self.target.y, val_end=new_y, easing=self.easing),
        ]


class RotateTo(Animation):
    def __init__(
        self,
        target: Element,
        angle: float = 0.0,
        duration: float = 1.0,
        easing: EasingFunc = linear,
    ):
        super().__init__(target, duration, easing)
        self._angle = angle

    def resolve(self, t_start: float) -> list[KeyFrame]:
        return [KeyFrame(
            element_id=self.target.id, prop="angle",
            t_start=t_start, t_end=t_start + self.duration,
            val_start=self.target.angle, val_end=self._angle, easing=self.easing,
        )]


class StrokeWidthTo(Animation):
    def __init__(
        self,
        target: Element,
        width: float = 2.0,
        duration: float = 1.0,
        easing: EasingFunc = linear,
    ):
        super().__init__(target, duration, easing)
        self._width = width

    def resolve(self, t_start: float) -> list[KeyFrame]:
        return [KeyFrame(
            element_id=self.target.id, prop="stroke_width",
            t_start=t_start, t_end=t_start + self.duration,
            val_start=self.target.stroke_width, val_end=self._width, easing=self.easing,
        )]


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


class ColorTo(Animation):
    """Animate stroke or background color. Uses RGB channel keyframes."""

    def __init__(
        self,
        target: Element,
        stroke: str | None = None,
        fill: str | None = None,
        duration: float = 1.0,
        easing: EasingFunc = linear,
    ):
        super().__init__(target, duration, easing)
        self._stroke = stroke
        self._fill = fill

    def resolve(self, t_start: float) -> list[KeyFrame]:
        kfs = []
        if self._stroke:
            sr, sg, sb = _hex_to_rgb(self.target.stroke_color)
            er, eg, eb = _hex_to_rgb(self._stroke)
            for ch, sv, ev in [("stroke_r", sr, er), ("stroke_g", sg, eg), ("stroke_b", sb, eb)]:
                kfs.append(KeyFrame(
                    element_id=self.target.id, prop=ch,
                    t_start=t_start, t_end=t_start + self.duration,
                    val_start=sv, val_end=ev, easing=self.easing,
                ))
        if self._fill:
            sr, sg, sb = _hex_to_rgb(self.target.background_color if self.target.background_color != "transparent" else "#ffffff")
            er, eg, eb = _hex_to_rgb(self._fill)
            for ch, sv, ev in [("fill_r", sr, er), ("fill_g", sg, eg), ("fill_b", sb, eb)]:
                kfs.append(KeyFrame(
                    element_id=self.target.id, prop=ch,
                    t_start=t_start, t_end=t_start + self.duration,
                    val_start=sv, val_end=ev, easing=self.easing,
                ))
        return kfs
