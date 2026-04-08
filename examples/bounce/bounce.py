from excanim import Scene, Ellipse, Line
from excanim.anim import FadeIn, FadeOut, MoveTo, ScaleTo, EaseIn, EaseOut


class Bounce(Scene):
    def construct(self):
        floor = Line(start=(100, 500), end=(700, 500))
        ball = Ellipse(pos=(370, 100), size=(60, 60), fill="#e03131")

        self.add(floor)
        self.play(FadeIn(ball, duration=0.3))

        for _ in range(3):
            self.play(MoveTo(ball, y=440, duration=0.4, easing=EaseIn))
            self.play(ScaleTo(ball, sx=1.3, sy=0.7, duration=0.05))
            self.play(ScaleTo(ball, sx=1.0, sy=1.0, duration=0.05))
            self.play(MoveTo(ball, y=150, duration=0.35, easing=EaseOut))

        self.play(FadeOut(ball, duration=0.3))


Bounce().render("examples/bounce/bounce.mp4", fps=30)

