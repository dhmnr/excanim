from __future__ import annotations

import json
import tempfile
from pathlib import Path


# JS to apply DrawIn effects by matching element IDs to SVG groups.
# Excalidraw renders elements in input order. <g stroke-linecap="round"> groups
# correspond to shapes/lines. <g transform="translate(...)"> without stroke-linecap
# are text. We match by walking both lists in order.
DRAW_EFFECT_JS = """
({effects, elementIds}) => {
    const svg = document.querySelector('svg');
    if (!svg) return;

    // Excalidraw SVG structure: metadata, defs, rect (bg), then <g> per element in input order
    const allGs = Array.from(svg.children).filter(el => el.tagName === 'g');

    // Map element IDs to <g> groups (1:1 same order)
    const idToGroup = {};
    for (let i = 0; i < elementIds.length && i < allGs.length; i++) {
        idToGroup[elementIds[i]] = allGs[i];
    }

    for (const effect of effects) {
        const g = idToGroup[effect.elementId];
        if (!g) continue;

        const paths = g.querySelectorAll('path');
        if (paths.length === 0) continue;

        for (const path of paths) {
            const isFill = path.getAttribute('stroke') === 'none' ||
                           path.getAttribute('stroke-width') === '0';

            if (!isFill) {
                // Split multi-segment path into individual subpaths for sequential reveal
                const d = path.getAttribute('d') || '';
                const segments = d.split(/(?=M)/).filter(s => s.trim());
                const ns = path.namespaceURI;
                const parent = path.parentNode;

                const segData = segments.map(seg => {
                    const tmp = document.createElementNS(ns, 'path');
                    tmp.setAttribute('d', seg);
                    parent.appendChild(tmp);
                    const len = tmp.getTotalLength();
                    parent.removeChild(tmp);
                    return { d: seg, len };
                });

                const totalLen = segData.reduce((s, x) => s + x.len, 0);
                const revealLen = totalLen * effect.progress;

                let accumulated = 0;
                for (const seg of segData) {
                    const sp = document.createElementNS(ns, 'path');
                    sp.setAttribute('d', seg.d);
                    sp.setAttribute('stroke', path.getAttribute('stroke'));
                    sp.setAttribute('stroke-width', path.getAttribute('stroke-width'));
                    sp.setAttribute('fill', 'none');
                    const remaining = revealLen - accumulated;
                    if (remaining <= 0) {
                        sp.style.display = 'none';
                    } else {
                        const segProgress = Math.min(1, remaining / seg.len);
                        sp.style.strokeDasharray = seg.len;
                        sp.style.strokeDashoffset = seg.len * (1 - segProgress);
                    }
                    parent.insertBefore(sp, path);
                    accumulated += seg.len;
                }
                path.style.display = 'none';
            }

            if (isFill) {
                path.style.opacity = effect.fillOpacity;
            }
        }
    }
}
"""


def frames_to_video(svgs: list[str], output: Path, fps: int, draw_effects: list | None = None,
                    frame_element_ids: list[list[str]] | None = None):
    import imageio.v3 as iio
    import numpy as np

    from excanim.render.bridge import get_browser

    ext = output.suffix.lower()

    with tempfile.TemporaryDirectory(prefix="excanim_") as tmpdir:
        tmp = Path(tmpdir)

        print(f"Rasterizing {len(svgs)} frames...")
        browser = get_browser()
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})

        for i, svg_str in enumerate(svgs):
            page.set_content(
                f"""<!DOCTYPE html>
                <html><head><style>
                body {{ margin:0; background:white; display:flex; align-items:center;
                       justify-content:center; width:1920px; height:1080px; overflow:hidden; }}
                svg {{ width:1920px; height:1080px; }}
                </style></head><body>{svg_str}</body></html>""",
                wait_until="networkidle",
            )

            if draw_effects and draw_effects[i] and frame_element_ids:
                effects_data = [
                    {
                        "elementId": e.element_id,
                        "progress": e.progress,
                        "fillOpacity": e.fill_opacity,
                    }
                    for e in draw_effects[i]
                ]
                # Element IDs in the frame (excluding canvas anchor)
                el_ids = frame_element_ids[i]
                page.evaluate(DRAW_EFFECT_JS, {"effects": effects_data, "elementIds": el_ids})

            page.screenshot(path=str(tmp / f"frame_{i:06d}.png"), type="png")

        page.close()

        print("Encoding video...")
        frames = []
        for i in range(len(svgs)):
            img = iio.imread(str(tmp / f"frame_{i:06d}.png"))
            if img.ndim == 3 and img.shape[2] == 4:
                img = img[:, :, :3]
            frames.append(img)

        if ext == ".gif":
            iio.imwrite(str(output), frames, fps=min(fps, 30), loop=0)
        elif ext in (".mp4", ".webm"):
            iio.imwrite(
                str(output), frames, fps=fps,
                codec="libx264" if ext == ".mp4" else "libvpx-vp9",
                quality=8,
            )
        else:
            raise ValueError(f"Unsupported video format: {ext}")

    print(f"Wrote {output}")
