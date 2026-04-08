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
            kfs.append(
                KeyFrame(
                    element_id=self.target.id,
                    prop="x",
                    t_start=t_start,
                    t_end=t_start + self.duration,
                    val_start=self.target.x,
                    val_end=self._x,
                    easing=self.easing,
                )
            )
        if self._y is not None:
            kfs.append(
                KeyFrame(
                    element_id=self.target.id,
                    prop="y",
                    t_start=t_start,
                    t_end=t_start + self.duration,
                    val_start=self.target.y,
                    val_end=self._y,
                    easing=self.easing,
                )
            )
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
        # Scale relative to ORIGINAL base size (not current animated size)
        # This prevents compounding: ScaleTo(sx=1.0) always returns to original
        cx = self.target.x + self.target.width / 2
        cy = self.target.y + self.target.height / 2
        new_w = self.target._base_width * self._sx
        new_h = self.target._base_height * self._sy
        new_x = cx - new_w / 2
        new_y = cy - new_h / 2

        return [
            KeyFrame(
                element_id=self.target.id,
                prop="width",
                t_start=t_start,
                t_end=t_start + self.duration,
                val_start=self.target.width,
                val_end=new_w,
                easing=self.easing,
            ),
            KeyFrame(
                element_id=self.target.id,
                prop="height",
                t_start=t_start,
                t_end=t_start + self.duration,
                val_start=self.target.height,
                val_end=new_h,
                easing=self.easing,
            ),
            KeyFrame(
                element_id=self.target.id,
                prop="x",
                t_start=t_start,
                t_end=t_start + self.duration,
                val_start=self.target.x,
                val_end=new_x,
                easing=self.easing,
            ),
            KeyFrame(
                element_id=self.target.id,
                prop="y",
                t_start=t_start,
                t_end=t_start + self.duration,
                val_start=self.target.y,
                val_end=new_y,
                easing=self.easing,
            ),
        ]
