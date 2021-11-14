from manim import *
import random


class Old1(Scene):
    def construct(self):

        box = Rectangle(
            height=4, width=6, fill_color=BLUE, fill_opacity=0.55, stroke_color=WHITE
        )
        text = MathTex("ln(2)")

        text.add_updater(lambda m: text.move_to(box.get_center()))

        self.add(box, text)
        self.play(box.animate.scale(0.5).to_edge(UL), run_time=3)
        self.wait()

        text.clear_updaters()

        self.play(box.animate.to_edge(RIGHT), run_time=3)
        self.wait()


class Old2(Scene):
    def construct(self):
        box = Rectangle(
            height=4, width=6, fill_color=BLUE, fill_opacity=0.55, stroke_color=WHITE
        )
        text = always_redraw(lambda: MathTex("ln(2)").move_to(box.get_center()))

        self.add(box, text)
        self.play(box.animate.scale(0.5).to_edge(UL), run_time=3)
        self.wait()

        text.clear_updaters()

        self.play(box.animate.to_edge(RIGHT), run_time=3)
        self.wait()


def get_helper_function(color):
    result = VGroup()
    box = Rectangle(
        height=4, width=6, fill_color=color, fill_opacity=0.5, stroke_color=color
    )
    text = MathTex("ln(2)").move_to(box.get_center())
    result.add(box, text)
    return result


class New(Scene):  # You will notice this renders faster
    def construct(self):

        stuff = get_helper_function(color=BLUE)

        self.play(Create(stuff))
        self.play(stuff.animate.scale(1.5).to_edge(UL), run_time=3)
        self.play(stuff[0].animate.to_edge(RIGHT), run_time=2)


class UpdateFunc(Scene):
    def construct(self):
        def get_coin():
            res = VGroup()
            a = random.uniform(0, 1)
            if a <= 0.5:
                c = Circle(radius=1, fill_opacity=0.5)
                c.set_style(fill_color=RED, stroke_color=RED)
                text = Tex("T").move_to(c.get_center())
                res.add(c, text)
                res.add(c, text)
            else:
                c = Circle(radius=1, fill_opacity=0.5)
                c.set_style(fill_color=BLUE, stroke_color=BLUE)
                text = Tex("H").move_to(c.get_center())
                res.add(c, text)
                res.add(c, text)
            return res

        def animate_coin(coin):
            a = random.uniform(0, 1)
            res = VGroup()
            if a <= 0.5:
                coin.set_style(fill_color=RED, stroke_color=RED)
                text = Tex("T").move_to(coin.get_center())
                res.add(coin, text)
            else:
                coin.set_style(fill_color=BLUE, stroke_color=BLUE)
                text = Tex("H").move_to(coin.get_center())
                res.add(coin, text)
            p = random.uniform(-0.04, 0.04)
            k = random.uniform(-0.04, 0.04)
            coin.shift(UP * k + LEFT * p)

        coin = always_redraw(lambda: get_coin())

        self.add(coin)
        self.wait()
        self.play(UpdateFromFunc(coin, animate_coin), run_time=2)
        self.wait()
