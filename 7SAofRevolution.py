from re import L
from manim import *

# HELPERS
def get_arc_lines(
    graph, plane, dx=1, x_min=None, x_max=None, line_color=RED, line_width=3
):

    dots = VGroup()
    lines = VGroup()
    result = VGroup(dots, lines)

    x_range = np.arange(x_min, x_max, dx)
    colors = color_gradient([BLUE_B, GREEN_B], len(x_range))

    for x, color in zip(x_range, colors):
        p1 = Dot().move_to(plane.input_to_graph_point(x, graph))
        p2 = Dot().move_to(plane.input_to_graph_point(x + dx, graph))
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


def get_conic_approximations(
    axes, graph, x_min=0, x_max=1, dx=0.5, color_A=RED, color_B=GREEN, opacity=1
):
    result = VGroup()
    for x in np.arange(x_min + dx, x_max + dx, dx):
        if graph.underlying_function(x) == 0:
            k = 0
            conic_surface = VectorizedPoint()
        else:
            k = graph.underlying_function(x) / x
            conic_surface = ParametricSurface(
                lambda u, v: axes.c2p(v, k * v * np.cos(u), k * v * np.sin(u)),
                u_min=0,
                u_max=2 * PI,
                v_min=x - dx,
                v_max=x,
                checkerboard_colors=[color_A, color_B],
                fill_opacity=opacity,
            )
        result.add(conic_surface)
    return result


def get_riemann_truncated_cones(
    axes,
    graph,
    x_min=0,
    x_max=1,
    dx=0.5,
    color_A=RED,
    color_B=GREEN,
    stroke_color=WHITE,
    stroke_width=1,
    opacity=1,
    theta=45,
):
    result = VGroup()
    for x in np.arange(x_min, x_max, dx):
        points = VGroup()
        p1 = axes.c2p(x + dx, 0)
        p2 = axes.c2p(x + dx, graph.underlying_function(x + dx))
        p3 = axes.c2p(x, graph.underlying_function(x))
        p4 = axes.c2p(x, 0)
        truncated_conic = ArcPolygon(
            p1,
            p2,
            p3,
            p4,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            fill_color=[color_A, color_B],
            fill_opacity=opacity,
            arc_config=[
                {"angle": theta * DEGREES, "color": stroke_color},
                {"angle": 0, "color": stroke_color},
                {"angle": -theta * DEGREES, "color": stroke_color},
                {"angle": 0, "color": stroke_color},
            ],
        )

        result.add(truncated_conic)

    return result


class One(ThreeDScene):
    def construct(self):

        l = 2
        w = 4
        h = 1

        rect_prism = Prism(dimensions=[l, w, h]).to_edge(LEFT, buff=1)

        kwargs = {"stroke_color": BLUE_D, "fill_color": BLUE_B, "fill_opacity": 0.8}
        bottom = Rectangle(width=w, height=l, **kwargs)
        s1 = Rectangle(height=h, width=w, **kwargs).next_to(bottom, UP, buff=0)
        s2 = Rectangle(height=h, width=w, **kwargs).next_to(bottom, DOWN, buff=0)
        l1 = Rectangle(height=l, width=h, **kwargs).next_to(bottom, LEFT, buff=0)
        l2 = Rectangle(height=l, width=h, **kwargs).next_to(bottom, RIGHT, buff=0)
        top = Rectangle(width=w, height=l, **kwargs).next_to(s1, UP, buff=0)
        net = VGroup(top, bottom, s1, s2, l1, l2).rotate(-PI / 2).to_edge(RIGHT, buff=1)

        arrow = Line(
            start=rect_prism.get_right(), end=net.get_left(), buff=0.2
        ).add_tip()

        self.begin_ambient_camera_rotation()
        self.set_camera_orientation(phi=45 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(rect_prism))
        self.play(
            LaggedStart(Create(arrow), Transform(rect_prism.copy(), net)),
            run_time=2,
            lag_ratio=0.5,
        )

        self.wait()
        self.play(FadeOut(Group(*self.mobjects)))
        self.stop_ambient_camera_rotation()

        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)
        text = Tex("Surface Area of a Solid Revolutions?")
        self.play(Write(text))
        self.wait()
        self.play(FadeOut(text))

        self.begin_ambient_camera_rotation()
        self.set_camera_orientation(phi=45 * DEGREES, theta=-45 * DEGREES)

        axes = ThreeDAxes(
            x_range=[0, 4.1, 1],
            x_length=5,
            y_range=[-4, 4.1, 1],
            y_length=5,
            z_range=[-4, 4, 1],
            z_length=5,
        ).add_coordinates()

        function = axes.get_graph(lambda x: 0.25 * x ** 2, x_range=[0, 4], color=YELLOW)
        area = axes.get_area(graph=function, x_range=[0, 4], color=[BLUE_B, BLUE_D])

        e = ValueTracker(2 * PI)
        surface = always_redraw(
            lambda: ParametricSurface(
                lambda u, v: axes.c2p(
                    v, 0.25 * v ** 2 * np.cos(u), 0.25 * v ** 2 * np.sin(u)
                ),
                u_min=0,
                u_max=e.get_value(),
                v_min=0,
                v_max=4,
                checkerboard_colors=[BLUE_B, BLUE_D],
            )
        )

        self.play(
            LaggedStart(Create(axes), Create(function), Create(area), Create(surface)),
            run_time=4,
            lag_ratio=0.5,
        )

        self.play(
            Rotating(
                VGroup(function, area),
                axis=RIGHT,
                radians=2 * PI,
                about_point=axes.c2p(0, 0, 0),
            ),
            e.animate.set_value(2 * PI),
            run_time=5,
            rate_func=linear,
        )
        self.wait(3)


class Two(ThreeDScene):
    def construct(self):

        axes = (
            ThreeDAxes(
                x_range=[0, 4.1, 1],
                x_length=5,
                y_range=[-4, 4.1, 1],
                y_length=5,
                z_range=[-4, 4, 1],
                z_length=5,
            )
            .to_edge(LEFT)
            .add_coordinates()
        )

        graph = axes.get_graph(lambda x: 0.25 * x ** 2, x_range=[0, 4], color=YELLOW)

        surface = always_redraw(
            lambda: ParametricSurface(
                lambda u, v: axes.c2p(
                    v, 0.25 * v ** 2 * np.cos(u), 0.25 * v ** 2 * np.sin(u)
                ),
                u_min=0,
                u_max=2 * PI,
                v_min=0,
                v_max=4,
                checkerboard_colors=[BLUE_B, BLUE_D],
            )
        )

        self.set_camera_orientation(phi=30 * DEGREES, theta=-90 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.play(
            LaggedStart(Create(axes), Create(graph), Create(surface)),
            run_time=2,
            lag_ratio=0.4,
        )

        cone = get_conic_approximations(
            axes=axes, graph=graph, x_min=0, x_max=4, dx=4, opacity=0.4
        )

        dist = ValueTracker(2)
        truncated_cone = always_redraw(
            lambda: ParametricSurface(
                lambda u, v: axes.c2p(v, v * np.cos(u), v * np.sin(u)),
                u_min=0,
                u_max=2 * PI,
                v_min=2,
                v_max=2 + dist.get_value(),
                checkerboard_colors=[RED, GREEN],
                opacity=0.6,
            )
        )

        self.play(Create(cone))
        self.play(Create(truncated_cone))
        self.wait()

        a = [0, 0, 0]
        b = [4, 0, 0]
        c = [3, 2, 0]
        d = [1, 2, 0]

        ##Now wanting to work on 2D Screen

        truncated_net = always_redraw(
            lambda: ArcPolygon(
                [0, 0, 0],
                [4, 0, 0],
                [3, dist.get_value(), 0],
                [1, dist.get_value(), 0],
                stroke_color=RED_B,
                fill_color=[GREEN_B, GREEN_D],
                fill_opacity=0.8,
                arc_config=[
                    {"angle": 45 * DEGREES, "color": RED},
                    {"angle": 0, "color": RED},
                    {"angle": -45 * DEGREES, "color": RED},
                    {"angle": 0, "color": RED},
                ],
            )
            .rotate(PI / 2)
            .next_to(axes, RIGHT, buff=1.5)
        )

        self.play(
            ReplacementTransform(truncated_cone.copy(), truncated_net), run_time=2
        )
        self.wait(2)

        self.stop_ambient_camera_rotation()
        self.move_camera(phi=0, theta=-90 * DEGREES)

        anot1 = always_redraw(
            lambda: MathTex("2 \\pi {r}_{0}")
            .set(width=0.8)
            .next_to(truncated_net, LEFT, buff=0.2)
        )
        anot2 = always_redraw(
            lambda: MathTex("2 \\pi {r}_{1}")
            .set(width=0.8)
            .next_to(truncated_net, RIGHT, buff=0.2)
        )
        anot3 = always_redraw(lambda: MathTex("L").next_to(truncated_net, UP, buff=0.1))
        annotations = VGroup(anot1, anot2, anot3)

        area = MathTex("Area = 2 \\pi r L").next_to(truncated_net, DOWN, buff=0.5)
        anot = MathTex("where \\ r=average \\ radius").next_to(
            area, DOWN, aligned_edge=LEFT
        )
        formula = VGroup(area, anot)

        self.play(FadeOut(VGroup(surface, cone)))

        self.play(Write(annotations))
        self.play(Write(formula))

        bound_a = MathTex("a").next_to(axes.c2p(0, 0, 0), DOWN, buff=0.1)
        bound_b = MathTex("b").next_to(axes.c2p(4, 0, 0), DOWN, buff=0.1)

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

        radius_line = Line(
            start=axes.c2p(2.25, 0),
            end=axes.c2p(2.25, graph.underlying_function(2.25)),
            stroke_color=BLUE,
            stroke_width=10,
        )

        radius_text = (
            MathTex("r")
            .set_color(BLUE)
            .set(width=0.3)
            .next_to(radius_line, RIGHT, buff=0.1)
        )

        demo_mobjects = VGroup(
            bound_a,
            bound_b,
            dx,
            dx_brace,
            dx_text,
            dy,
            dy_brace,
            dy_text,
            dl,
            dl_brace,
            dl_text,
        )

        self.play(Create(demo_mobjects))
        self.play(dist.animate.set_value(0.5), run_time=5)

        intuition_text = MathTex(
            "As \\ L\\rightarrow 0, L \\ is \\ Arc \\ Length"
        ).to_edge(UR, buff=0.2)
        sa_formula = MathTex("SA = \\int_{a}^{b}2\pi", "x", "\\ dL").next_to(
            intuition_text, DOWN, buff=0.2, aligned_edge=LEFT
        )

        self.play(Write(intuition_text))
        self.play(Write(sa_formula))
        self.wait()
        self.play(Create(radius_line), Write(radius_text))
        self.wait()
        self.play(Transform(radius_text.copy(), sa_formula[1]))
        self.wait()


class ThreePers1(ThreeDScene):
    def construct(self):

        axes = ThreeDAxes(
            x_range=[0, 4, 1],
            x_length=5,
            y_range=[-4, 4, 1],
            y_length=5,
            z_range=[-4, 4, 1],
            z_length=5,
            axis_config={"decimal_number_config": {"num_decimal_places": 0}},
        ).to_edge(LEFT)

        graph = axes.get_graph(lambda x: 0.25 * x ** 2, x_range=[0, 4], color=YELLOW)

        surface = always_redraw(
            lambda: ParametricSurface(
                lambda u, v: axes.c2p(
                    v, 0.25 * v ** 2 * np.cos(u), 0.25 * v ** 2 * np.sin(u)
                ),
                u_min=0,
                u_max=2 * PI,
                v_min=0,
                v_max=4,
                checkerboard_colors=[BLUE_B, BLUE_D],
            )
        )

        dx = ValueTracker(1)
        conic_approx = always_redraw(
            lambda: get_conic_approximations(
                axes=axes, graph=graph, x_min=0, x_max=4, dx=dx.get_value()
            )
        )

        num_text = MathTex("dx=").next_to(axes, UP, buff=0.5)
        num = always_redraw(
            lambda: DecimalNumber()
            .set_value(dx.get_value())
            .next_to(num_text, RIGHT, buff=0.1)
        )

        plane = NumberPlane(
            x_range=[0, 4, 1],
            x_length=5,
            y_range=[0, 61, 20],
            y_length=6,
            axis_config={"decimal_number_config": {"num_decimal_places": 0}},
        ).to_edge(DR)
        plane.add_coordinates()

        def sa_func(x):
            return 6.2832 * x * (1 + (x ** 2 / 4)) ** 0.5

        graph2 = plane.get_graph(sa_func, x_range=[0, 4], color=BLUE)
        graph2_lab = Tex("SA Function").next_to(plane, UP, buff=0.2)

        t = ValueTracker(
            45
        )  # Tracking the bowness in the sa of conics, mathematically incorrect but whatever
        truncated_area = always_redraw(
            lambda: get_riemann_truncated_cones(
                axes=plane,
                graph=graph2,
                x_min=0,
                x_max=4,
                dx=dx.get_value(),
                theta=t.get_value(),
            )
        )

        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        self.add(axes, graph, surface, conic_approx, num_text, num)
        self.play(
            LaggedStart(
                Create(conic_approx),
                Write(VGroup(num_text, num)),
                DrawBorderThenFill(plane),
                run_time=2,
                lag_ratio=0.25,
            )
        )
        self.wait()
        self.play(ReplacementTransform(conic_approx.copy(), truncated_area), run_time=2)
        self.play(
            dx.animate.set_value(0.1), t.animate.set_value(5), run_time=6
        )  # set dx = 0.1, and t = 5
        self.play(
            LaggedStart(Create(graph2), Write(graph2_lab), run_time=1, lag_ratio=0.3)
        )
        self.wait()


class ThreePers2(ThreeDScene):
    def construct(self):

        axes = ThreeDAxes(
            x_range=[0, 4.1, 1],
            x_length=5,
            y_range=[-4, 4.1, 1],
            y_length=5,
            z_range=[-4, 4, 1],
            z_length=5,
            axis_config={"decimal_number_config": {"num_decimal_places": 0}},
        ).to_edge(LEFT)
        axes.add_coordinates()

        graph = axes.get_graph(lambda x: 0.25 * x ** 2, x_range=[0, 4], color=YELLOW)

        surface = always_redraw(
            lambda: ParametricSurface(
                lambda u, v: axes.c2p(
                    v, 0.25 * v ** 2 * np.cos(u), 0.25 * v ** 2 * np.sin(u)
                ),
                u_min=0,
                u_max=2 * PI,
                v_min=0,
                v_max=4,
                checkerboard_colors=[BLUE_B, BLUE_D],
            )
        )

        dx = ValueTracker(1)
        conic_approx = always_redraw(
            lambda: get_conic_approximations(
                axes=axes, graph=graph, x_min=0, x_max=4, dx=dx.get_value()
            )
        )

        num_text = MathTex("dx=").next_to(axes, UP, buff=0.5)
        num = always_redraw(
            lambda: DecimalNumber()
            .set_value(dx.get_value())
            .next_to(num_text, RIGHT, buff=0.1)
        )

        axes2 = Axes(
            x_range=[0, 4, 1], x_length=5, y_range=[0, 60, 10], y_length=6
        ).to_edge(DR)

        def sa_func(x):
            return 6.2832 * x * (1 + (x ** 2 / 4)) ** 0.5

        graph2 = axes2.get_graph(sa_func, x_range=[0, 4], color=BLUE)
        graph2_lab = Tex("SA Function").next_to(axes2, UP, buff=0.2)

        t = ValueTracker(
            45
        )  # Tracking the bowness in the sa of conics, mathematically incorrect but whatever
        truncated_area = always_redraw(
            lambda: get_riemann_truncated_cones(
                axes=axes2,
                graph=graph2,
                x_min=0,
                x_max=4,
                dx=dx.get_value(),
                theta=t.get_value(),
            )
        )

        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        self.add(axes, graph, surface, conic_approx, num_text, num)
        self.move_camera(phi=30 * DEGREES, theta=-100 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.01)
        self.play(
            LaggedStart(
                Create(conic_approx),
                Write(VGroup(num_text, num)),
                DrawBorderThenFill(axes2),
                run_time=1,
                lag_ratio=0.25,
            )
        )
        self.play(ReplacementTransform(conic_approx.copy(), truncated_area), run_time=1)
        self.play(
            dx.animate.set_value(0.1), t.animate.set_value(5), run_time=3
        )  # set dx = 0.1, and t = 5
        self.add(graph2, graph2_lab)
        self.wait()


class FourArcL(Scene):
    def construct(self):

        axes = Axes(
            x_range=[0, 4.1, 1],
            x_length=5,
            y_range=[-4, 4.1, 1],
            y_length=5,
            axis_config={"decimal_number_config": {"num_decimal_places": 0}},
        ).to_edge(LEFT)
        axes.add_coordinates()

        graph = axes.get_graph(lambda x: 0.25 * x ** 2, x_range=[0, 4], color=YELLOW)

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
            .to_edge(UR, buff=0.5)
        )
        line1 = MathTex("{dL}^{2}=", "{dx}^{2}", "+{dy}^{2}")
        line2 = MathTex("{dL}^{2}=", "{dx}^{2}", "(1+(\\frac{dy}{dx})^{2})")
        line3 = MathTex(
            "dL = \\sqrt{", "{dx}^{2}", "(1+(\\frac{dy}{dx})^{2}) }"
        )  # Then using surds
        line4 = MathTex("dL = \\sqrt{", "1", " + (\\frac{dy}{dx})^{2} } dxx")
        proof = (
            VGroup(line1, line2, line3, line4)
            .scale(0.8)
            .arrange(DOWN, aligned_edge=LEFT)
            .next_to(helper_text, DOWN, buff=0.25)
        )

        box = SurroundingRectangle(helper_text)

        # The actual line integral
        dx_tracker = ValueTracker(1.5)  # Tracking the dx distance of line integral

        line_integral = always_redraw(
            lambda: get_arc_lines(
                graph=graph,
                plane=axes,
                dx=dx_tracker.get_value(),
                x_min=0,
                x_max=4,
                line_color=RED,
                line_width=7,
            )
        )

        self.add(axes, graph)
        self.play(Write(helper_text))
        self.wait()
        self.play(Write(line1))
        self.wait()
        self.play(Write(line2[0]))
        self.play(ReplacementTransform(line1[1].copy(), line2[1]))
        self.play(Write(line2[2]))
        self.wait()
        self.play(Write(line3), run_time=2)
        self.wait()
        self.play(Write(line4))
        self.wait()
        self.add(line_integral)
        self.play(dx_tracker.animate.set_value(0.2), Create(box), run_time=8)
        self.wait()


class FiveSolving(ThreeDScene):  # Need to render
    def construct(self):

        axes = ThreeDAxes(
            x_range=[0, 4, 1],
            x_length=5,
            y_range=[-4, 4, 1],
            y_length=5,
            z_range=[-4, 4, 1],
            z_length=5,
        ).to_edge(LEFT)
        axes.add_coordinates()
        graph = axes.get_graph(lambda x: 0.25 * x ** 2, x_range=[0, 4], color=YELLOW)
        graph_lab = (
            MathTex("y=\\frac{x^2}{4}")
            .scale(0.8)
            .next_to(graph, UP, buff=0.2)
            .set_color(YELLOW)
        )

        surface = always_redraw(
            lambda: ParametricSurface(
                lambda u, v: axes.c2p(
                    v, 0.25 * v ** 2 * np.cos(u), 0.25 * v ** 2 * np.sin(u)
                ),
                u_min=0,
                u_max=2 * PI,
                v_min=0,
                v_max=4,
                checkerboard_colors=[BLUE_B, BLUE_D],
            )
        )
        dx = ValueTracker(0.5)
        truncated_conics = always_redraw(
            lambda: get_conic_approximations(
                axes=axes, graph=graph, x_min=0, x_max=4, dx=dx.get_value()
            )
        )

        self.add(axes, graph, surface, graph_lab)
        solve0 = MathTex(
            "SA = \\int_{a}^{b} 2 \\pi x dL, \\ dL = \\sqrt{ 1+(\\frac{dy}{dx})^{2}) }"
        )
        solve1 = MathTex(
            "SA = \\int_{a}^{b} 2 \\pi x", "\\sqrt{ 1+(\\frac{dy}{dx})^{2}) }"
        )
        solve2 = MathTex("y=\\frac{x^2}{4} , \\", "\\frac{dy}{dx} = \\frac{x}{2}")
        solve3 = MathTex("(\\frac{dy}{dx})^2 = ", "\\frac{x^2}{4}")
        solve4 = MathTex(
            "SA = \\int_{0}^{4} 2 \\pi x \\sqrt{ 1 + ", "\\frac{x^2}{4}", " }"
        )
        solve5 = MathTex("SA = 85.29 \\ units^2").next_to(axes, DOWN, buff=0.3)
        solved = (
            VGroup(solve0, solve1, solve2, solve3, solve4)
            .scale(0.75)
            .arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            .to_edge(UR, buff=0.2)
        )

        self.play(Write(solve0), run_time=0.5)
        self.wait()
        self.play(Write(solve1), run_time=0.5)
        self.play(ReplacementTransform(graph_lab.copy(), solve2[0]), run_time=0.5)
        self.wait()
        self.play(Write(solve2[1]), run_time=0.5)
        self.wait()
        self.play(Write(solve3[0]), run_time=0.5)
        self.play(ReplacementTransform(solve2[1].copy(), solve3[1]), run_time=0.5)
        self.wait()
        self.play(Write(solve4), run_time=0.5)
        self.wait()
        self.move_camera(phi=30 * DEGREES, theta=-90 * DEGREES)
        self.play(FadeIn(truncated_conics), run_time=0.5)
        self.play(dx.animate.set_value(0.1), Write(solve5), run_time=2)
        self.wait()
