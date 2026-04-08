from __future__ import annotations

from dataclasses import dataclass, field

from excanim.elements.base import Element, _make_id, _random_seed
from excanim.constants import (
    DEFAULT_STROKE_COLOR,
    DEFAULT_STROKE_WIDTH,
    DEFAULT_STROKE_STYLE,
    DEFAULT_ROUGHNESS,
    DEFAULT_OPACITY,
)


@dataclass
class Line(Element):
    points: list[list[float]] = field(default_factory=list)

    def __init__(
        self,
        start: tuple[float, float] | Element = (0, 0),
        end: tuple[float, float] | Element = (100, 100),
        **kwargs,
    ):
        sx, sy = _resolve_point(start)
        ex, ey = _resolve_point(end)
        super().__init__(
            x=sx,
            y=sy,
            width=abs(ex - sx),
            height=abs(ey - sy),
            **kwargs,
        )
        self.points = [[0, 0], [ex - sx, ey - sy]]

    def to_excalidraw(self) -> dict:
        d = self._base_excalidraw()
        d["type"] = "line"
        d["points"] = self.points
        d["lastCommittedPoint"] = None
        d["startBinding"] = None
        d["endBinding"] = None
        d["startArrowhead"] = None
        d["endArrowhead"] = None
        return d


@dataclass
class Arrow(Element):
    points: list[list[float]] = field(default_factory=list)
    label: str | None = None
    _start_element: Element | None = field(default=None, repr=False)
    _end_element: Element | None = field(default=None, repr=False)

    def __init__(
        self,
        start: tuple[float, float] | Element = (0, 0),
        end: tuple[float, float] | Element = (100, 100),
        label: str | None = None,
        **kwargs,
    ):
        sx, sy = _resolve_point(start, anchor="right")
        ex, ey = _resolve_point(end, anchor="left")
        super().__init__(
            x=sx,
            y=sy,
            width=abs(ex - sx),
            height=abs(ey - sy),
            **kwargs,
        )
        self.points = [[0, 0], [ex - sx, ey - sy]]
        self.label = label
        self._start_element = start if isinstance(start, Element) else None
        self._end_element = end if isinstance(end, Element) else None

    def to_excalidraw(self) -> dict:
        d = self._base_excalidraw()
        d["type"] = "arrow"
        d["points"] = self.points
        d["lastCommittedPoint"] = None
        d["startBinding"] = _make_binding(self._start_element)
        d["endBinding"] = _make_binding(self._end_element)
        d["startArrowhead"] = None
        d["endArrowhead"] = "arrow"
        d["roundness"] = {"type": 2}
        return d


def _resolve_point(
    target: tuple[float, float] | Element,
    anchor: str = "center",
) -> tuple[float, float]:
    if isinstance(target, tuple):
        return target
    bx, by, bw, bh = target.bounds()
    if anchor == "center":
        return (bx + bw / 2, by + bh / 2)
    elif anchor == "left":
        return (bx, by + bh / 2)
    elif anchor == "right":
        return (bx + bw, by + bh / 2)
    elif anchor == "top":
        return (bx + bw / 2, by)
    elif anchor == "bottom":
        return (bx + bw / 2, by + bh)
    return (bx + bw / 2, by + bh / 2)


def _make_binding(element: Element | None) -> dict | None:
    if element is None:
        return None
    return {
        "elementId": element.id,
        "fixedPoint": None,
        "focus": 0,
        "gap": 8,
    }
