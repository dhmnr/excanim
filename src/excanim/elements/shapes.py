from __future__ import annotations

from dataclasses import dataclass

from excanim.elements.base import Element


@dataclass
class Rect(Element):
    label: str | None = None

    def __init__(
        self,
        pos: tuple[float, float] = (0, 0),
        size: tuple[float, float] = (100, 100),
        fill: str = "transparent",
        label: str | None = None,
        **kwargs,
    ):
        super().__init__(
            x=pos[0],
            y=pos[1],
            width=size[0],
            height=size[1],
            background_color=fill,
            **kwargs,
        )
        self.label = label

    def to_excalidraw(self) -> dict:
        d = self._base_excalidraw()
        d["type"] = "rectangle"
        d["roundness"] = {"type": 3}
        return d


@dataclass
class Ellipse(Element):
    label: str | None = None

    def __init__(
        self,
        pos: tuple[float, float] = (0, 0),
        size: tuple[float, float] = (100, 100),
        fill: str = "transparent",
        label: str | None = None,
        **kwargs,
    ):
        super().__init__(
            x=pos[0],
            y=pos[1],
            width=size[0],
            height=size[1],
            background_color=fill,
            **kwargs,
        )
        self.label = label

    def to_excalidraw(self) -> dict:
        d = self._base_excalidraw()
        d["type"] = "ellipse"
        return d


@dataclass
class Diamond(Element):
    label: str | None = None

    def __init__(
        self,
        pos: tuple[float, float] = (0, 0),
        size: tuple[float, float] = (100, 100),
        fill: str = "transparent",
        label: str | None = None,
        **kwargs,
    ):
        super().__init__(
            x=pos[0],
            y=pos[1],
            width=size[0],
            height=size[1],
            background_color=fill,
            **kwargs,
        )
        self.label = label

    def to_excalidraw(self) -> dict:
        d = self._base_excalidraw()
        d["type"] = "diamond"
        return d
