from __future__ import annotations

import random
import uuid
from dataclasses import dataclass, field

from excanim.constants import (
    DEFAULT_BACKGROUND_COLOR,
    DEFAULT_FILL_STYLE,
    DEFAULT_FONT_FAMILY,
    DEFAULT_FONT_SIZE,
    DEFAULT_LINE_HEIGHT,
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
    group_ids: list[str] = field(default_factory=list)
    # Original dimensions for ScaleTo to reference
    _base_width: float = field(default=0.0, repr=False)
    _base_height: float = field(default=0.0, repr=False)
    # Label creates a bound text element
    _label_id: str | None = field(default=None, repr=False)

    def __post_init__(self):
        if self._base_width == 0.0:
            self._base_width = self.width
        if self._base_height == 0.0:
            self._base_height = self.height

    def bounds(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, self.width, self.height)

    def _base_excalidraw(self) -> dict:
        bound = None
        if self._label_id is not None:
            bound = [{"id": self._label_id, "type": "text"}]
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
            "groupIds": list(self.group_ids),
            "boundElements": bound,
            "locked": False,
            "link": None,
            "updated": 1,
            "roundness": None,
        }

    def to_excalidraw(self) -> dict:
        return self._base_excalidraw()

    def to_excalidraw_list(self) -> list[dict]:
        """Return this element + any bound elements (e.g. label text)."""
        return [self.to_excalidraw()]

    def _make_label_element(self, label: str) -> dict:
        """Create an Excalidraw text element bound inside this container."""
        self._label_id = _make_id()
        return {
            "id": self._label_id,
            "type": "text",
            "x": self.x + self.width / 2,
            "y": self.y + self.height / 2,
            "width": len(label) * DEFAULT_FONT_SIZE * 0.6,
            "height": DEFAULT_FONT_SIZE * DEFAULT_LINE_HEIGHT,
            "text": label,
            "fontSize": DEFAULT_FONT_SIZE,
            "fontFamily": DEFAULT_FONT_FAMILY,
            "textAlign": "center",
            "verticalAlign": "middle",
            "containerId": self.id,
            "originalText": label,
            "autoResize": True,
            "lineHeight": DEFAULT_LINE_HEIGHT,
            "strokeColor": self.stroke_color,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 1,
            "strokeStyle": "solid",
            "roughness": self.roughness,
            "opacity": self.opacity,
            "angle": 0,
            "seed": _random_seed(),
            "version": 1,
            "versionNonce": random.randint(1, 2**31 - 1),
            "isDeleted": False,
            "groupIds": list(self.group_ids),
            "boundElements": None,
            "locked": False,
            "link": None,
            "updated": 1,
            "roundness": None,
        }
