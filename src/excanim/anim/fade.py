from __future__ import annotations

from excanim.anim.base import Animation, KeyFrame
from excanim.anim.easing import EasingFunc, linear
from excanim.elements.base import Element


class FadeIn(Animation):
    def __init__(self, target: Element, duration: float = 1.0, easing: EasingFunc = linear):
        super().__init__(target, duration, easing)

    def resolve(self, t_start: float) -> list[KeyFrame]:
        return [
            KeyFrame(
                element_id=self.target.id,
                prop="opacity",
                t_start=t_start,
                t_end=t_start + self.duration,
                val_start=0,
                val_end=self.target.opacity,
                easing=self.easing,
            )
        ]


class FadeOut(Animation):
    def __init__(self, target: Element, duration: float = 1.0, easing: EasingFunc = linear):
        super().__init__(target, duration, easing)

    def resolve(self, t_start: float) -> list[KeyFrame]:
        return [
            KeyFrame(
                element_id=self.target.id,
                prop="opacity",
                t_start=t_start,
                t_end=t_start + self.duration,
                val_start=self.target.opacity,
                val_end=0,
                easing=self.easing,
            )
        ]
