from excanim import Scene, Rect, Arrow, Text


class Arch(Scene):
    def construct(self):
        client = Rect(pos=(100, 300), size=(180, 100), fill="#a8d8ea", label="Client")
        api = Rect(pos=(450, 300), size=(180, 100), fill="#fcbad3", label="API Server")
        db = Rect(pos=(800, 300), size=(180, 100), fill="#aa96da", label="Database")

        a1 = Arrow(client, api, label="HTTP")
        a2 = Arrow(api, db, label="SQL")

        title = Text("Architecture", pos=(400, 150), font_size=28)

        self.add(client, api, db, a1, a2, title)


Arch().render("examples/arch.svg")
print("Rendered examples/arch.svg")
