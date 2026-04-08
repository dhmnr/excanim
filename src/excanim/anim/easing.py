from __future__ import annotations

import math
from typing import Callable

EasingFunc = Callable[[float], float]


def linear(t: float) -> float:
    return t


def ease_in(t: float) -> float:
    return t * t


def ease_out(t: float) -> float:
    return 1 - (1 - t) * (1 - t)


def ease_in_out(t: float) -> float:
    if t < 0.5:
        return 2 * t * t
    return 1 - (-2 * t + 2) ** 2 / 2


def ease_in_cubic(t: float) -> float:
    return t * t * t


def ease_out_cubic(t: float) -> float:
    return 1 - (1 - t) ** 3


def ease_in_out_cubic(t: float) -> float:
    if t < 0.5:
        return 4 * t * t * t
    return 1 - (-2 * t + 2) ** 3 / 2


def bounce_out(t: float) -> float:
    n1, d1 = 7.5625, 2.75
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375


def bounce_in(t: float) -> float:
    return 1 - bounce_out(1 - t)


def ease_out_quart(t: float) -> float:
    return 1 - (1 - t) ** 4


def ease_in_out_quart(t: float) -> float:
    if t < 0.5:
        return 8 * t * t * t * t
    return 1 - (-2 * t + 2) ** 4 / 2


def spring(t: float) -> float:
    """Apple-style spring easing — slight overshoot then settle."""
    return 1 - math.cos(t * math.pi * 0.5) * math.exp(-t * 3.5) * (1 - t)


# Convenience aliases
Linear = linear
EaseIn = ease_in
EaseOut = ease_out
EaseInOut = ease_in_out
EaseInCubic = ease_in_cubic
EaseOutCubic = ease_out_cubic
EaseInOutCubic = ease_in_out_cubic
BounceIn = bounce_in
BounceOut = bounce_out
