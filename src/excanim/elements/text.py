from __future__ import annotations

from dataclasses import dataclass

from excanim.elements.base import Element
from excanim.constants import (
    DEFAULT_FONT_SIZE,
    DEFAULT_FONT_FAMILY,
    DEFAULT_LINE_HEIGHT,
)


@dataclass
class Text(Element):
    text: str = ""
    font_size: int = DEFAULT_FONT_SIZE
    font_family: int = DEFAULT_FONT_FAMILY
    text_align: str = "left"
    vertical_align: str = "top"
    line_height: float = DEFAULT_LINE_HEIGHT

    def __init__(
        self,
        text: str = "",
        pos: tuple[float, float] = (0, 0),
        font_size: int = DEFAULT_FONT_SIZE,
        font_family: int = DEFAULT_FONT_FAMILY,
        text_align: str = "left",
        **kwargs,
    ):
        # Approximate text dimensions
        lines = text.split("\n")
        approx_width = max(len(line) for line in lines) * font_size * 0.6
        approx_height = len(lines) * font_size * DEFAULT_LINE_HEIGHT
        super().__init__(
            x=pos[0],
            y=pos[1],
            width=approx_width,
            height=approx_height,
            **kwargs,
        )
        self.text = text
        self.font_size = font_size
        self.font_family = font_family
        self.text_align = text_align
        self.vertical_align = "top"
        self.line_height = DEFAULT_LINE_HEIGHT

    def to_excalidraw(self) -> dict:
        d = self._base_excalidraw()
        d["type"] = "text"
        d["text"] = self.text
        d["fontSize"] = self.font_size
        d["fontFamily"] = self.font_family
        d["textAlign"] = self.text_align
        d["verticalAlign"] = self.vertical_align
        d["containerId"] = None
        d["originalText"] = self.text
        d["autoResize"] = True
        d["lineHeight"] = self.line_height
        return d
