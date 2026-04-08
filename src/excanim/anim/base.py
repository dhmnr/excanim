from __future__ import annotations

from dataclasses import dataclass, field

from excanim.anim.easing import EasingFunc, linear
from excanim.elements.base import Element


@dataclass
class KeyFrame:
    element_id: str
    prop: str  # "opacity", "x", "y", "width", "height"
    t_start: float
    t_end: float
    val_start: float
    val_end: float
    easing: EasingFunc = field(default=linear, repr=False)

    def interpolate(self, t: float) -> float:
        if t <= self.t_start:
            return self.val_start
        if t >= self.t_end:
            return self.val_end
        duration = self.t_end - self.t_start
        if duration == 0:
            return self.val_end
        progress = (t - self.t_start) / duration
        eased = self.easing(progress)
        return self.val_start + (self.val_end - self.val_start) * eased


class Animation:
    def __init__(self, target: Element, duration: float = 1.0, easing: EasingFunc = linear):
        self.target = target
        self.duration = duration
        self.easing = easing

    def resolve(self, t_start: float) -> list[KeyFrame]:
        raise NotImplementedError
