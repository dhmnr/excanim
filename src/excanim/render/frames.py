from __future__ import annotations

import math

from excanim.elements.base import Element
from excanim.render.bridge import batch_elements_to_svg
from excanim.timeline import Timeline


# Map our property names to Excalidraw element attributes
PROP_MAP = {
    "x": "x",
    "y": "y",
    "width": "width",
    "height": "height",
    "opacity": "opacity",
}


def _make_canvas_anchor(width: int, height: int) -> dict:
    """Fixed-size invisible rectangle that pins the SVG viewBox to (0,0,w,h)."""
    return {
        "id": "__excanim_canvas__",
        "type": "rectangle",
        "x": 0,
        "y": 0,
        "width": width,
        "height": height,
        "strokeColor": "transparent",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 0,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 0,
        "angle": 0,
        "seed": 1,
        "version": 1,
        "versionNonce": 1,
        "isDeleted": False,
        "groupIds": [],
        "boundElements": None,
        "locked": False,
        "link": None,
        "updated": 1,
        "roundness": None,
    }


def build_frame_data(
    base_elements: dict[str, Element],
    timeline: Timeline,
    fps: int,
    canvas_width: int = 800,
    canvas_height: int = 600,
) -> list[list[dict]]:
    """Build per-frame element JSON dicts from timeline. No bridge call."""
    duration = timeline.duration
    num_frames = max(1, math.ceil(duration * fps))
    anchor = _make_canvas_anchor(canvas_width, canvas_height)

    all_frames: list[list[dict]] = []
    for i in range(num_frames):
        t = i / fps
        overrides = timeline.resolve_frame(t)

        frame_elements = [anchor]
        for el_id, el in base_elements.items():
            d = el.to_excalidraw()
            if el_id in overrides:
                for prop, val in overrides[el_id].items():
                    excalidraw_key = PROP_MAP.get(prop, prop)
                    if excalidraw_key == "opacity":
                        d[excalidraw_key] = int(round(val))
                    else:
                        d[excalidraw_key] = val
            frame_elements.append(d)
        all_frames.append(frame_elements)

    return all_frames


def render_frames(
    base_elements: dict[str, Element],
    timeline: Timeline,
    fps: int,
    canvas_width: int = 800,
    canvas_height: int = 600,
) -> list[str]:
    all_frames = build_frame_data(base_elements, timeline, fps, canvas_width, canvas_height)
    return batch_elements_to_svg(all_frames)
