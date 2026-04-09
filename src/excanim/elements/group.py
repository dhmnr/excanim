from __future__ import annotations

from excanim.elements.base import Element, _make_id


RIGHT = "right"
LEFT = "left"
DOWN = "down"
UP = "up"


class Group:
    """Group elements together and apply layout operations."""

    def __init__(self, *elements: Element):
        self.elements = list(elements)
        self.group_id = _make_id()
        # Assign group ID to all elements
        for el in self.elements:
            el.group_ids.append(self.group_id)

    def arrange(self, direction: str = RIGHT, gap: float = 20) -> Group:
        """Arrange elements in a row or column with consistent spacing."""
        if not self.elements:
            return self
        if direction == RIGHT:
            x = self.elements[0].x
            for el in self.elements:
                el.x = x
                x += el.width + gap
        elif direction == LEFT:
            x = self.elements[0].x
            for el in reversed(self.elements):
                el.x = x
                x += el.width + gap
        elif direction == DOWN:
            y = self.elements[0].y
            for el in self.elements:
                el.y = y
                y += el.height + gap
        elif direction == UP:
            y = self.elements[0].y
            for el in reversed(self.elements):
                el.y = y
                y += el.height + gap
        return self

    def align(self, axis: str = "center") -> Group:
        """Align elements along an axis.

        axis: "left", "right", "center" (horizontal), "top", "bottom", "middle" (vertical)
        """
        if not self.elements:
            return self
        if axis == "left":
            min_x = min(el.x for el in self.elements)
            for el in self.elements:
                el.x = min_x
        elif axis == "right":
            max_r = max(el.x + el.width for el in self.elements)
            for el in self.elements:
                el.x = max_r - el.width
        elif axis == "center":
            cx = sum(el.x + el.width / 2 for el in self.elements) / len(self.elements)
            for el in self.elements:
                el.x = cx - el.width / 2
        elif axis == "top":
            min_y = min(el.y for el in self.elements)
            for el in self.elements:
                el.y = min_y
        elif axis == "bottom":
            max_b = max(el.y + el.height for el in self.elements)
            for el in self.elements:
                el.y = max_b - el.height
        elif axis == "middle":
            cy = sum(el.y + el.height / 2 for el in self.elements) / len(self.elements)
            for el in self.elements:
                el.y = cy - el.height / 2
        return self

    def distribute(self, direction: str = RIGHT) -> Group:
        """Distribute elements evenly between the first and last."""
        if len(self.elements) < 3:
            return self
        if direction in (RIGHT, LEFT):
            sorted_els = sorted(self.elements, key=lambda e: e.x)
            start = sorted_els[0].x
            end = sorted_els[-1].x + sorted_els[-1].width
            total_width = sum(el.width for el in sorted_els)
            gap = (end - start - total_width) / (len(sorted_els) - 1)
            x = start
            for el in sorted_els:
                el.x = x
                x += el.width + gap
        elif direction in (DOWN, UP):
            sorted_els = sorted(self.elements, key=lambda e: e.y)
            start = sorted_els[0].y
            end = sorted_els[-1].y + sorted_els[-1].height
            total_height = sum(el.height for el in sorted_els)
            gap = (end - start - total_height) / (len(sorted_els) - 1)
            y = start
            for el in sorted_els:
                el.y = y
                y += el.height + gap
        return self
