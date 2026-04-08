# excanim

Manim-style Python API for Excalidraw drawings and animations.

## Install

```bash
pip install excanim
playwright install chromium
```

**Requirements:** Python 3.12+

## Examples

See [`examples/`](examples/) — architecture diagram, bouncing ball, physics simulation, matrix multiplication.

## How it works

Python builds Excalidraw element JSON, renders it through `@excalidraw/excalidraw` in headless Chromium via Playwright, outputs SVG/PNG/MP4.
