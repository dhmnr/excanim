from __future__ import annotations

import math
from dataclasses import dataclass, field

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
    "angle": "angle",
    "stroke_width": "strokeWidth",
}

# Color channel props need special handling
COLOR_CHANNELS = {"stroke_r", "stroke_g", "stroke_b", "fill_r", "fill_g", "fill_b"}

# DrawIn props — handled by SVG post-processing, not Excalidraw JSON
DRAW_PROPS = {"_draw_progress", "_draw_fill"}


@dataclass
class DrawEffect:
    """Per-element draw-in effect for a single frame."""
    element_id: str     # Excalidraw element ID to target
    progress: float     # 0.0 to 1.0 — how much stroke is revealed
    fill_opacity: float # 0.0 to 1.0 — fill visibility


@dataclass
class FrameData:
    """One frame's worth of element JSON + draw effects."""
    elements: list[dict]
    draw_effects: list[DrawEffect] = field(default_factory=list)


def _make_canvas_anchor(width: int, height: int) -> dict:
    return {
        "id": "__excanim_canvas__",
        "type": "rectangle",
        "x": 0, "y": 0, "width": width, "height": height,
        "strokeColor": "transparent", "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 0, "strokeStyle": "solid",
        "roughness": 0, "opacity": 0, "angle": 0, "seed": 1,
        "version": 1, "versionNonce": 1, "isDeleted": False,
        "groupIds": [], "boundElements": None, "locked": False,
        "link": None, "updated": 1, "roundness": None,
    }


def _apply_overrides(d: dict, overrides: dict[str, float]) -> dict[str, float]:
    """Apply overrides to element dict. Returns any draw-in props found."""
    stroke_channels = {}
    fill_channels = {}
    draw_props = {}

    for prop, val in overrides.items():
        if prop in DRAW_PROPS:
            draw_props[prop] = val
        elif prop in COLOR_CHANNELS:
            if prop.startswith("stroke_"):
                stroke_channels[prop[-1]] = int(round(val))
            else:
                fill_channels[prop[-1]] = int(round(val))
        else:
            key = PROP_MAP.get(prop, prop)
            if key == "opacity":
                d[key] = int(round(val))
            else:
                d[key] = val

    if stroke_channels:
        d["strokeColor"] = f"#{stroke_channels.get('r', 0):02x}{stroke_channels.get('g', 0):02x}{stroke_channels.get('b', 0):02x}"
    if fill_channels:
        d["backgroundColor"] = f"#{fill_channels.get('r', 0):02x}{fill_channels.get('g', 0):02x}{fill_channels.get('b', 0):02x}"

    return draw_props


def build_frames(
    base_elements: dict[str, Element],
    timeline: Timeline,
    fps: int,
    canvas_width: int = 800,
    canvas_height: int = 600,
) -> list[FrameData]:
    """Build per-frame data from timeline."""
    duration = timeline.duration
    num_frames = max(1, math.ceil(duration * fps))
    anchor = _make_canvas_anchor(canvas_width, canvas_height)

    frames: list[FrameData] = []
    for i in range(num_frames):
        t = i / fps
        overrides = timeline.resolve_frame(t)

        frame_elements = [anchor]
        draw_effects: list[DrawEffect] = []
        el_index = 1  # start after anchor

        for el_id, el in base_elements.items():
            el_dicts = el.to_excalidraw_list()
            for d in el_dicts:
                if d["id"] == el_id and el_id in overrides:
                    draw_props = _apply_overrides(d, overrides[el_id])
                    if draw_props:
                        draw_effects.append(DrawEffect(
                            element_id=el_id,
                            progress=draw_props.get("_draw_progress", 1.0),
                            fill_opacity=draw_props.get("_draw_fill", 1.0),
                        ))
                    # Also hide bound label text during DrawIn
                    if draw_props and draw_props.get("_draw_progress", 1.0) < 1.0:
                        for label_d in el_dicts:
                            if label_d.get("containerId") == el_id:
                                label_d["opacity"] = 0
                    elif draw_props and "_draw_fill" in draw_props:
                        fill_op = draw_props["_draw_fill"]
                        for label_d in el_dicts:
                            if label_d.get("containerId") == el_id:
                                label_d["opacity"] = int(round(fill_op * 100))
                frame_elements.append(d)

        frames.append(FrameData(elements=frame_elements, draw_effects=draw_effects))

    return frames


# Legacy API
def build_frame_data(
    base_elements: dict[str, Element],
    timeline: Timeline,
    fps: int,
    canvas_width: int = 800,
    canvas_height: int = 600,
) -> list[list[dict]]:
    return [f.elements for f in build_frames(base_elements, timeline, fps, canvas_width, canvas_height)]


def render_frames(
    base_elements: dict[str, Element],
    timeline: Timeline,
    fps: int,
    canvas_width: int = 800,
    canvas_height: int = 600,
) -> tuple[list[str], list[list[DrawEffect]], list[list[str]]]:
    """Render frames to SVGs. Returns (svgs, per_frame_draw_effects, per_frame_element_ids)."""
    frames = build_frames(base_elements, timeline, fps, canvas_width, canvas_height)
    all_elements = [f.elements for f in frames]
    all_effects = [f.draw_effects for f in frames]
    # Element IDs per frame, in same order as SVG <g> groups
    all_ids = [[d["id"] for d in f.elements] for f in frames]
    svgs = batch_elements_to_svg(all_elements)
    return svgs, all_effects, all_ids
