from __future__ import annotations

from dataclasses import dataclass, field

from excanim.elements.base import Element, _make_id, _random_seed


ARROWHEAD_TYPES = {"arrow", "bar", "dot", "triangle", None}


@dataclass
class Line(Element):
    points: list[list[float]] = field(default_factory=list)

    def __init__(
        self,
        start: tuple[float, float] | Element = (0, 0),
        end: tuple[float, float] | Element = (100, 100),
        waypoints: list[tuple[float, float]] | None = None,
        **kwargs,
    ):
        sx, sy = _resolve_point(start)
        ex, ey = _resolve_point(end)
        super().__init__(
            x=sx, y=sy,
            width=abs(ex - sx), height=abs(ey - sy),
            **kwargs,
        )
        pts = [[0, 0]]
        if waypoints:
            for wx, wy in waypoints:
                pts.append([wx - sx, wy - sy])
        pts.append([ex - sx, ey - sy])
        self.points = pts

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
    start_arrowhead: str | None = None
    end_arrowhead: str = "arrow"
    _start_element: Element | None = field(default=None, repr=False)
    _end_element: Element | None = field(default=None, repr=False)

    def __init__(
        self,
        start: tuple[float, float] | Element = (0, 0),
        end: tuple[float, float] | Element = (100, 100),
        label: str | None = None,
        waypoints: list[tuple[float, float]] | None = None,
        start_arrowhead: str | None = None,
        end_arrowhead: str = "arrow",
        **kwargs,
    ):
        sx, sy = _resolve_point(start, anchor="right")
        ex, ey = _resolve_point(end, anchor="left")
        super().__init__(
            x=sx, y=sy,
            width=abs(ex - sx), height=abs(ey - sy),
            **kwargs,
        )
        pts = [[0, 0]]
        if waypoints:
            for wx, wy in waypoints:
                pts.append([wx - sx, wy - sy])
        pts.append([ex - sx, ey - sy])
        self.points = pts
        self.label = label
        self.start_arrowhead = start_arrowhead
        self.end_arrowhead = end_arrowhead
        self._start_element = start if isinstance(start, Element) else None
        self._end_element = end if isinstance(end, Element) else None

    def to_excalidraw(self) -> dict:
        d = self._base_excalidraw()
        d["type"] = "arrow"
        d["points"] = self.points
        d["lastCommittedPoint"] = None
        d["startBinding"] = _make_binding(self._start_element)
        d["endBinding"] = _make_binding(self._end_element)
        d["startArrowhead"] = self.start_arrowhead
        d["endArrowhead"] = self.end_arrowhead
        d["roundness"] = {"type": 2}
        return d

    def to_excalidraw_list(self) -> list[dict]:
        if self.label:
            label_el = self._make_label_element(self.label)
            return [self.to_excalidraw(), label_el]
        return [self.to_excalidraw()]


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
