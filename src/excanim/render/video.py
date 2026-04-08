from __future__ import annotations

import tempfile
from pathlib import Path


def frames_to_video(svgs: list[str], output: Path, fps: int):
    import imageio.v3 as iio
    import numpy as np

    from excanim.render.bridge import get_browser

    ext = output.suffix.lower()

    with tempfile.TemporaryDirectory(prefix="excanim_") as tmpdir:
        tmp = Path(tmpdir)

        # Rasterize SVGs to PNGs via shared Chromium browser
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
            page.screenshot(path=str(tmp / f"frame_{i:06d}.png"), type="png")

        page.close()

        # Encode video
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
                str(output),
                frames,
                fps=fps,
                codec="libx264" if ext == ".mp4" else "libvpx-vp9",
                quality=8,
            )
        else:
            raise ValueError(f"Unsupported video format: {ext}")

    print(f"Wrote {output}")
