from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

from excanim.render.bridge import _find_node, BRIDGE_DIR


def frames_to_video(svgs: list[str], output: Path, fps: int):
    import imageio.v3 as iio
    import numpy as np

    ext = output.suffix.lower()

    with tempfile.TemporaryDirectory(prefix="excanim_") as tmpdir:
        # Rasterize SVGs to PNGs via Playwright (preserves Excalidraw fonts)
        print(f"Rasterizing {len(svgs)} frames via browser...")
        node = _find_node()
        rasterize_script = BRIDGE_DIR / "rasterize.mjs"

        result = subprocess.run(
            [node, str(rasterize_script), tmpdir, "1920", "1080"],
            input=json.dumps(svgs),
            capture_output=True,
            text=True,
            timeout=600,
            cwd=str(BRIDGE_DIR),
        )
        if result.returncode != 0:
            raise RuntimeError(f"Rasterize failed:\n{result.stderr}")

        # Read PNGs into numpy arrays
        print("Encoding video...")
        frames = []
        for i in range(len(svgs)):
            png_path = Path(tmpdir) / f"frame_{i:06d}.png"
            img = iio.imread(str(png_path))
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
