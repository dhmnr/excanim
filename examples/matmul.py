import math
from excanim import Scene, Rect, Text
from excanim.anim.easing import ease_in_out_quart


def _blend(hex1: str, hex2: str) -> str:
    r1, g1, b1 = int(hex1[1:3], 16), int(hex1[3:5], 16), int(hex1[5:7], 16)
    r2, g2, b2 = int(hex2[1:3], 16), int(hex2[3:5], 16), int(hex2[5:7], 16)
    return f"#{(r1+r2)//2:02x}{(g1+g2)//2:02x}{(b1+b2)//2:02x}"


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


class MatMul(Scene):
    def simulate(self):
        cell = 50
        ease = ease_in_out_quart

        ax, ay = 80, 180
        bx, by = ax + 2 * cell + 80, 30
        cx, cy = bx, ay

        a_row_colors = ["#a8d8ea", "#b6e3f4", "#c8edff"]
        b_col_colors = ["#fcbad3", "#f490ad", "#d4a5e5", "#c3e8bd"]

        # Labels
        self.add(Text("A", pos=(ax + cell - 12, ay - 40), font_size=24))
        self.add(Text("B", pos=(bx + 2 * cell - 12, by - 40), font_size=24))
        self.add(Text("C", pos=(cx + 2 * cell - 12, cy - 40), font_size=24))

        # Matrix A cells
        for r in range(3):
            for c in range(2):
                self.add(Rect(
                    pos=(ax + c * cell, ay + r * cell),
                    size=(cell, cell),
                    fill=a_row_colors[r],
                    stroke_width=1,
                ))

        # Matrix B cells
        for r in range(2):
            for c in range(4):
                self.add(Rect(
                    pos=(bx + c * cell, by + r * cell),
                    size=(cell, cell),
                    fill=b_col_colors[c],
                    stroke_width=1,
                ))

        # Matrix C cells (start dimmed)
        c_cells = {}
        for r in range(3):
            for c in range(4):
                rect = Rect(
                    pos=(cx + c * cell, cy + r * cell),
                    size=(cell, cell),
                    fill="transparent",
                    stroke_width=1,
                    opacity=30,
                )
                c_cells[(r, c)] = rect
                self.add(rect)

        # Highlights
        row_hl = Rect(
            pos=(ax - 4, ay - 4),
            size=(2 * cell + 8, cell + 8),
            fill="transparent",
            stroke_color="#e03131",
            stroke_width=3,
            opacity=0,
        )
        col_hl = Rect(
            pos=(bx - 4, by - 4),
            size=(cell + 8, 2 * cell + 8),
            fill="transparent",
            stroke_color="#e03131",
            stroke_width=3,
            opacity=0,
        )
        res_hl = Rect(
            pos=(cx - 4, cy - 4),
            size=(cell + 8, cell + 8),
            fill="transparent",
            stroke_color="#e03131",
            stroke_width=3,
            opacity=0,
        )
        self.add(row_hl, col_hl, res_hl)

        move_frames = 18       # frames for highlight slide
        hold_frames = 12       # frames to hold on result
        fade_in_frames = 10    # frames for result cell fade-in

        # Initial pause
        for _ in range(self.fps // 2):
            self.capture()

        prev_row_y = ay - 4
        prev_col_x = bx - 4
        prev_res_x = cx - 4
        prev_res_y = cy - 4
        first = True

        for r in range(3):
            for c in range(4):
                target_row_y = ay + r * cell - 4
                target_col_x = bx + c * cell - 4
                target_res_x = cx + c * cell - 4
                target_res_y = cy + r * cell - 4

                # Slide highlights to new position
                for f in range(move_frames):
                    t = ease(f / (move_frames - 1))

                    row_hl.y = _lerp(prev_row_y, target_row_y, t)
                    col_hl.x = _lerp(prev_col_x, target_col_x, t)
                    res_hl.x = _lerp(prev_res_x, target_res_x, t)
                    res_hl.y = _lerp(prev_res_y, target_res_y, t)

                    # Fade in highlights on first step
                    if first:
                        row_hl.opacity = int(_lerp(0, 100, t))
                        col_hl.opacity = int(_lerp(0, 100, t))
                        res_hl.opacity = int(_lerp(0, 100, t))

                    self.capture()

                first = False
                prev_row_y = target_row_y
                prev_col_x = target_col_x
                prev_res_x = target_res_x
                prev_res_y = target_res_y

                # Fade in result cell
                target_color = _blend(a_row_colors[r], b_col_colors[c])
                c_cells[(r, c)].background_color = target_color
                for f in range(fade_in_frames):
                    t = ease(f / (fade_in_frames - 1))
                    c_cells[(r, c)].opacity = int(_lerp(30, 100, t))
                    self.capture()

                # Hold
                for _ in range(hold_frames):
                    self.capture()

        # Fade out highlights
        fade_out_frames = 30
        for f in range(fade_out_frames):
            t = ease(f / (fade_out_frames - 1))
            row_hl.opacity = int(_lerp(100, 0, t))
            col_hl.opacity = int(_lerp(100, 0, t))
            res_hl.opacity = int(_lerp(100, 0, t))
            self.capture()

        # Final hold
        for _ in range(self.fps):
            self.capture()


MatMul(fps=60).render("examples/matmul.mp4")
print("Done!")
