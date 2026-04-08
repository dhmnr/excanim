from __future__ import annotations

import random
import uuid
from dataclasses import dataclass, field

from excanim.constants import (
    DEFAULT_BACKGROUND_COLOR,
    DEFAULT_FILL_STYLE,
    DEFAULT_OPACITY,
    DEFAULT_ROUGHNESS,
    DEFAULT_STROKE_COLOR,
    DEFAULT_STROKE_STYLE,
    DEFAULT_STROKE_WIDTH,
)


def _random_seed() -> int:
    return random.randint(1, 2**31 - 1)


def _make_id() -> str:
    return uuid.uuid4().hex[:20]


@dataclass
class Element:
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    stroke_color: str = DEFAULT_STROKE_COLOR
    background_color: str = DEFAULT_BACKGROUND_COLOR
    fill_style: str = DEFAULT_FILL_STYLE
    stroke_width: float = DEFAULT_STROKE_WIDTH
    stroke_style: str = DEFAULT_STROKE_STYLE
    roughness: int = DEFAULT_ROUGHNESS
    opacity: int = DEFAULT_OPACITY
    angle: float = 0.0
    id: str = field(default_factory=_make_id)
    seed: int = field(default_factory=_random_seed)
    # Original dimensions for ScaleTo to reference
    _base_width: float = field(default=0.0, repr=False)
    _base_height: float = field(default=0.0, repr=False)

    def __post_init__(self):
        if self._base_width == 0.0:
            self._base_width = self.width
        if self._base_height == 0.0:
            self._base_height = self.height

    def bounds(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, self.width, self.height)

    def _base_excalidraw(self) -> dict:
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "strokeColor": self.stroke_color,
            "backgroundColor": self.background_color,
            "fillStyle": self.fill_style,
            "strokeWidth": self.stroke_width,
            "strokeStyle": self.stroke_style,
            "roughness": self.roughness,
            "opacity": self.opacity,
            "angle": self.angle,
            "seed": self.seed,
            "version": 1,
            "versionNonce": random.randint(1, 2**31 - 1),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": None,
            "locked": False,
            "link": None,
            "updated": 1,
            "roundness": None,
        }

    def to_excalidraw(self) -> dict:
        return self._base_excalidraw()
