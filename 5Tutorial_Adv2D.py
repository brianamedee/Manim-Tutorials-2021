from manim import *

# HELPERS FOR COMPLEX SCENES, you can always create your own :)
def get_horizontal_line_to_graph(axes, function, x, width, color):
    result = VGroup()
    line = DashedLine(
        start=axes.c2p(0, function.underlying_function(x)),
        end=axes.c2p(x, function.underlying_function(x)),
        stroke_width=width,
        stroke_color=color,
    )
    dot = Dot().set_color(color).move_to(axes.c2p(x, function.underlying_function(x)))
    result.add(line, dot)
    return result


def get_arc_lines_on_function(
    graph, plane, dx=1, line_color=WHITE, line_width=1, x_min=None, x_max=None
):

    dots = VGroup()
    lines = VGroup()
    result = VGroup(dots, lines)

    x_range = np.arange(x_min, x_max, dx)
    colors = color_gradient([BLUE_B, GREEN_B], len(x_range))

    for x, color in zip(x_range, colors):
        p1 = Dot().scale(0.7).move_to(plane.input_to_graph_point(x, graph))
        p2 = Dot().scale(0.7).move_to(plane.input_to_graph_point(x + dx, graph))
        dots.add(p1, p2)
        dots.set_fill(colors, opacity=0.8)

        line = Line(
            p1.get_center(),
            p2.get_center(),
            stroke_color=line_color,
            stroke_width=line_width,
        )
        lines.add(line)

    return result


class Derivatives(Scene):
    def construct(self):

        k = ValueTracker(-3)  # Tracking the end values of stuff to show

        # Adding Mobjects for the first plane
        plane1 = (
            NumberPlane(x_range=[-3, 4, 1], x_length=5, y_range=[-8, 9, 2], y_length=5)
            .add_coordinates()
            .shift(LEFT * 3.5)
        )

        func1 = plane1.get_graph(
            lambda x: (1 / 3) * x ** 3, x_range=[-3, 3], color=RED_C
        )
        func1_lab = (
            MathTex("f(x)=\\frac{1}{3} {x}^{3}")
            .set(width=2.5)
            .next_to(plane1, UP, buff=0.2)
            .set_color(RED_C)
        )

        moving_slope = always_redraw(
            lambda: plane1.get_secant_slope_group(
                x=k.get_value(),
                graph=func1,
                dx=0.05,
                secant_line_length=4,
                secant_line_color=YELLOW,
            )
        )

        dot = always_redraw(
            lambda: Dot().move_to(
                plane1.c2p(k.get_value(), func1.underlying_function(k.get_value()))
            )
        )

        # Adding Mobjects for the second plane
        plane2 = (
            NumberPlane(x_range=[-3, 4, 1], x_length=5, y_range=[0, 11, 2], y_length=5)
            .add_coordinates()
            .shift(RIGHT * 3.5)
        )

        func2 = always_redraw(
            lambda: plane2.get_graph(
                lambda x: x ** 2, x_range=[-3, k.get_value()], color=GREEN
            )
        )
        func2_lab = (
            MathTex("f'(x)={x}^{2}")
            .set(width=2.5)
            .next_to(plane2, UP, buff=0.2)
            .set_color(GREEN)
        )

        moving_h_line = always_redraw(
            lambda: get_horizontal_line_to_graph(
                axes=plane2, function=func2, x=k.get_value(), width=4, color=YELLOW
            )
        )

        # Adding the slope value stuff
        slope_value_text = (
            Tex("Slope value: ")
            .next_to(plane1, DOWN, buff=0.1)
            .set_color(YELLOW)
            .add_background_rectangle()
        )

        slope_value = always_redraw(
            lambda: DecimalNumber(num_decimal_places=1)
            .set_value(func2.underlying_function(k.get_value()))
            .next_to(slope_value_text, RIGHT, buff=0.1)
            .set_color(YELLOW)
        ).add_background_rectangle()

        # Playing the animation
        self.play(
            LaggedStart(
                DrawBorderThenFill(plane1),
                DrawBorderThenFill(plane2),
                Create(func1),
                Write(func1_lab),
                Write(func2_lab),
                run_time=5,
                lag_ratio=0.5,
            )
        )
        self.add(moving_slope, moving_h_line, func2, slope_value, slope_value_text, dot)
        self.play(k.animate.set_value(3), run_time=15, rate_func=linear)
        self.wait()


class AdditiveFunctions(Scene):
    def construct(self):

        axes = (
            Axes(x_range=[0, 2.1, 1], x_length=12, y_range=[0, 7, 2], y_length=7)
            .add_coordinates()
            .to_edge(DL, buff=0.25)
        )

        func1 = axes.get_graph(lambda x: x ** 2, x_range=[0, 2], color=YELLOW)
        func1_lab = (
            MathTex("y={x}^{2}").scale(0.8).next_to(func1, UR, buff=0).set_color(YELLOW)
        )

        func2 = axes.get_graph(lambda x: x, x_range=[0, 2], color=GREEN)
        func2_lab = (
            MathTex("y=x").scale(0.8).next_to(func2, UR, buff=0).set_color(GREEN)
        )

        func3 = axes.get_graph(lambda x: x ** 2 + x, x_range=[0, 2], color=PURPLE_D)
        func3_lab = (
            MathTex("y={x}^{2} + x")
            .scale(0.8)
            .next_to(func3, UR, buff=0)
            .set_color(PURPLE_D)
        )

        self.add(axes, func1, func2, func3, func1_lab, func2_lab, func3_lab)
        self.wait()

        for k in np.arange(0.2, 2.1, 0.2):
            line1 = DashedLine(
                start=axes.c2p(k, 0),
                end=axes.c2p(k, func1.underlying_function(k)),
                stroke_color=YELLOW,
                stroke_width=5,
            )

            line2 = DashedLine(
                start=axes.c2p(k, 0),
                end=axes.c2p(k, func2.underlying_function(k)),
                stroke_color=GREEN,
                stroke_width=7,
            )

            line3 = Line(
                start=axes.c2p(k, 0),
                end=axes.c2p(k, func3.underlying_function(k)),
                stroke_color=PURPLE,
                stroke_width=10,
            )

            self.play(Create(line1))
            self.play(Create(line2))

            if len(line1) > len(line2):
                self.play(line2.animate.shift(UP * line1.get_length()))
            else:
                self.play(line1.animate.shift(UP * line2.get_length()))

            self.play(Create(line3))
        self.wait()

        # Explaining the area additive rule
        area1 = axes.get_riemann_rectangles(
            graph=func1, x_range=[0, 2], dx=0.1, color=[BLUE, GREEN]
        )
        area2 = axes.get_riemann_rectangles(
            graph=func2, x_range=[0, 2], dx=0.1, color=[YELLOW, PURPLE]
        )

        self.play(Create(area1))
        self.play(area1.animate.set_opacity(0.5))
        self.play(Create(area2))
        self.wait()
        for k in range(20):
            self.play(area2[k].animate.shift(UP * area1[k].get_height()))
        self.wait()


class ArcLength(Scene):
    def construct(self):

        axes = (
            Axes(x_range=[-1, 4.1, 1], x_length=8, y_range=[0, 3.1, 1], y_length=6)
            .to_edge(DL)
            .add_coordinates()
        )
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        graph = axes.get_graph(
            lambda x: 0.1 * x * (x + 1) * (x - 3) + 1, x_range=[-1, 4], color=BLUE
        )

        # Mobjects for explaining construction of Line Integral
        dist = ValueTracker(1)

        dx = always_redraw(
            lambda: DashedLine(
                start=axes.c2p(2, graph.underlying_function(2)),
                end=axes.c2p(2 + dist.get_value(), graph.underlying_function(2)),
                stroke_color=GREEN,
            )
        )

        dx_brace = always_redraw(lambda: Brace(dx).next_to(dx, DOWN, buff=0.1))
        dx_text = always_redraw(
            lambda: MathTex("dx").set(width=0.3).next_to(dx_brace, DOWN, buff=0)
        )

        dy = always_redraw(
            lambda: DashedLine(
                start=axes.c2p(
                    2 + dist.get_value(),
                    graph.underlying_function(2 + dist.get_value()),
                ),
                end=axes.c2p(2 + dist.get_value(), graph.underlying_function(2)),
                stroke_color=GREEN,
            )
        )

        dy_brace = always_redraw(
            lambda: Brace(dy, direction=RIGHT).next_to(dy, RIGHT, buff=0.1)
        )
        dy_text = always_redraw(
            lambda: MathTex("dy").set(width=0.3).next_to(dy_brace, RIGHT, buff=0)
        )

        dl = always_redraw(
            lambda: Line(
                start=axes.c2p(2, graph.underlying_function(2)),
                end=axes.c2p(
                    2 + dist.get_value(),
                    graph.underlying_function(2 + dist.get_value()),
                ),
                stroke_color=YELLOW,
            )
        )

        dl_brace = always_redraw(
            lambda: BraceBetweenPoints(point_1=dl.get_end(), point_2=dl.get_start())
        )
        dl_text = always_redraw(
            lambda: MathTex("dL")
            .set(width=0.3)
            .next_to(dl_brace, UP, buff=0)
            .set_color(YELLOW)
        )

        demo_mobjects = VGroup(
            dx, dx_brace, dx_text, dy, dy_brace, dy_text, dl, dl_brace, dl_text
        )

        # Adding the Latex Mobjects for Mini-Proof
        helper_text = (
            MathTex("dL \\ approximates \\ curve \\ as \\ dx\\ approaches \\ 0")
            .set(width=6)
            .to_edge(UR, buff=0.2)
        )
        line1 = MathTex("{dL}^{2}={dx}^{2}+{dy}^{2}")
        line2 = MathTex("{dL}^{2}={dx}^{2}(1+(\\frac{dy}{dx})^{2})")
        line3 = MathTex(
            "dL = \\sqrt{ {dx}^{2}(1+(\\frac{dy}{dx})^{2}) }"
        )  # Then using surds
        line4 = MathTex("dL = \\sqrt{1 + (\\frac{dy}{dx})^{2} } dx")
        proof = (
            VGroup(line1, line2, line3, line4)
            .scale(0.8)
            .arrange(DOWN, aligned_edge=LEFT)
            .next_to(helper_text, DOWN, buff=0.25)
        )

        box = SurroundingRectangle(helper_text)

        # The actual line integral
        dx_tracker = ValueTracker(1)  # Tracking the dx distance of line integral

        line_integral = always_redraw(
            lambda: get_arc_lines_on_function(
                graph=graph,
                plane=axes,
                dx=dx_tracker.get_value(),
                x_min=-1,
                x_max=4,
                line_color=RED,
                line_width=5,
            )
        )

        # Playing the animation
        self.add(axes, graph)
        self.wait()
        self.play(Create(dx), Create(dy))
        self.play(Create(dl))
        self.add(dx_brace, dx_text, dy_brace, dy_text, dl_brace, dl_text)

        self.play(Write(proof), run_time=5, rate_func=linear)
        self.wait()
        self.play(Write(helper_text))
        self.play(Create(box), run_time=2)
        self.play(dist.animate.set_value(0.5), run_time=10)
        self.play(
            FadeOut(proof),
            demo_mobjects.animate.set_width(0.5).next_to(box, LEFT, buff=0.1),
            FadeOut(demo_mobjects),
            run_time=3,
        )

        self.play(Create(line_integral))
        self.play(dx_tracker.animate.set_value(0.2), run_time=10)
        self.wait()
