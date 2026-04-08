from excanim import Scene, Rect, Ellipse


class BouncingSim(Scene):
    def simulate(self):
        box = Rect(pos=(50, 50), size=(700, 500), stroke_width=3)
        ball = Ellipse(pos=(200, 200), size=(40, 40), fill="#e03131")
        self.add(box, ball)

        vx, vy = 300, 200  # px/sec
        dt = 1 / self.fps

        for _ in range(self.fps * 5):  # 5 seconds
            ball.x += vx * dt
            ball.y += vy * dt

            if ball.x <= box.x:
                ball.x = box.x
                vx = abs(vx)
            elif ball.x + ball.width >= box.x + box.width:
                ball.x = box.x + box.width - ball.width
                vx = -abs(vx)

            if ball.y <= box.y:
                ball.y = box.y
                vy = abs(vy)
            elif ball.y + ball.height >= box.y + box.height:
                ball.y = box.y + box.height - ball.height
                vy = -abs(vy)

            self.capture()


BouncingSim(fps=60).render("examples/bounce_sim.mp4")
print("Done!")
