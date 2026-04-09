from __future__ import annotations

from excanim.anim.base import Animation, KeyFrame
from excanim.anim.easing import EasingFunc, linear
from excanim.elements.base import Element


class Create(Animation):
    """Fade-in animation. Alias for FadeIn."""

    def __init__(self, target: Element, duration: float = 1.0, easing: EasingFunc = linear):
        super().__init__(target, duration, easing)

    def resolve(self, t_start: float) -> list[KeyFrame]:
        return [
            KeyFrame(
                element_id=self.target.id, prop="opacity",
                t_start=t_start, t_end=t_start + self.duration,
                val_start=0, val_end=self.target.opacity, easing=self.easing,
            )
        ]


class Write(Animation):
    """Fade-in for text. Alias for FadeIn."""

    def __init__(self, target: Element, duration: float = 1.0, easing: EasingFunc = linear):
        super().__init__(target, duration, easing)

    def resolve(self, t_start: float) -> list[KeyFrame]:
        return [
            KeyFrame(
                element_id=self.target.id, prop="opacity",
                t_start=t_start, t_end=t_start + self.duration,
                val_start=0, val_end=self.target.opacity, easing=self.easing,
            )
        ]


class DrawIn(Animation):
    """Hand-drawn stroke reveal animation.

    The element's outline traces itself progressively, then the fill fades in.
    Uses stroke-dashoffset SVG manipulation at rasterization time.
    """

    def __init__(
        self,
        target: Element,
        duration: float = 1.0,
        easing: EasingFunc = linear,
        fill_ratio: float = 0.2,
    ):
        super().__init__(target, duration, easing)
        self.fill_ratio = fill_ratio  # last 20% of duration for fill fade-in

    def resolve(self, t_start: float) -> list[KeyFrame]:
        # _draw_progress: 0 = invisible, 1 = fully drawn
        # _draw_fill: 0 = fill hidden, 1 = fill visible
        stroke_dur = self.duration * (1 - self.fill_ratio)
        fill_dur = self.duration * self.fill_ratio

        return [
            # Start with element invisible, then immediately show at opacity
            KeyFrame(
                element_id=self.target.id, prop="opacity",
                t_start=t_start, t_end=t_start + 0.001,
                val_start=0, val_end=self.target.opacity, easing=self.easing,
            ),
            # Stroke progress 0 → 1
            KeyFrame(
                element_id=self.target.id, prop="_draw_progress",
                t_start=t_start, t_end=t_start + stroke_dur,
                val_start=0.0, val_end=1.0, easing=self.easing,
            ),
            # Fill fade 0 → 1 (starts after stroke finishes)
            KeyFrame(
                element_id=self.target.id, prop="_draw_fill",
                t_start=t_start + stroke_dur, t_end=t_start + self.duration,
                val_start=0.0, val_end=1.0, easing=self.easing,
            ),
        ]
