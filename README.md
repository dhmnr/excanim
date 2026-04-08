# excanim

Manim-style Python API for Excalidraw drawings and animations. Pixel-perfect hand-drawn output powered by Excalidraw's own renderer.

## Setup

**System dependencies:**
- Python 3.12+
- Node.js 18+ (for the Excalidraw rendering bridge)
- [uv](https://docs.astral.sh/uv/) (Python package manager)

**Install:**
```bash
uv sync
cd bridge && npm install && npx esbuild bundle-entry.js --bundle --outfile=bundle.js --format=iife --platform=browser --loader:.css=empty --define:process.env.NODE_ENV=\"production\" && cd ..
npx playwright install chromium
```

## Usage

### Static diagram
```python
from excanim import Scene, Rect, Arrow, Text

class Arch(Scene):
    def construct(self):
        client = Rect(pos=(100, 300), size=(180, 100), fill="#a8d8ea")
        api    = Rect(pos=(450, 300), size=(180, 100), fill="#fcbad3")
        self.add(client, api, Arrow(client, api))

Arch().render("out.svg")
```

### Animated (keyframe)
```python
from excanim import Scene, Ellipse, Line
from excanim.anim import FadeIn, MoveTo, EaseIn, EaseOut

class Bounce(Scene):
    def construct(self):
        ball = Ellipse(pos=(370, 100), size=(60, 60), fill="#e03131")
        self.add(Line(start=(100, 500), end=(700, 500)))
        self.play(FadeIn(ball, duration=0.3))
        self.play(MoveTo(ball, y=440, duration=0.4, easing=EaseIn))
        self.play(MoveTo(ball, y=150, duration=0.35, easing=EaseOut))

Bounce().render("out.mp4", fps=60)
```

### Simulation (frame-by-frame)
```python
from excanim import Scene, Rect, Ellipse

class Sim(Scene):
    def simulate(self):
        box = Rect(pos=(50, 50), size=(700, 500))
        ball = Ellipse(pos=(200, 200), size=(40, 40), fill="#e03131")
        self.add(box, ball)

        vx, vy = 300, 200
        for _ in range(self.fps * 5):
            ball.x += vx / self.fps
            ball.y += vy / self.fps
            if ball.x <= box.x or ball.x + ball.width >= box.x + box.width: vx = -vx
            if ball.y <= box.y or ball.y + ball.height >= box.y + box.height: vy = -vy
            self.capture()

Sim(fps=60).render("out.mp4")
```

## Output formats

| Extension | Output |
|-----------|--------|
| `.svg` | Static Excalidraw SVG |
| `.excalidraw` | Excalidraw JSON (open in excalidraw.com) |
| `.mp4` | H.264 video |
| `.gif` | Animated GIF |
| `.webm` | VP9 WebM |

## Elements

`Rect`, `Ellipse`, `Diamond`, `Line`, `Arrow`, `Text`

## Animations

`FadeIn`, `FadeOut`, `MoveTo`, `ScaleTo`, `Create`, `Write`

## Easing

`Linear`, `EaseIn`, `EaseOut`, `EaseInOut`, `EaseInCubic`, `EaseOutCubic`, `EaseInOutCubic`, `BounceIn`, `BounceOut`

## How it works

Python builds Excalidraw JSON elements -> Node.js bridge renders them via `@excalidraw/excalidraw` in headless Chromium (Playwright) -> SVG/PNG output -> imageio-ffmpeg encodes video.

## Examples

See [`examples/`](examples/) for working demos: architecture diagram, bouncing ball, physics simulation, matrix multiplication animation.
