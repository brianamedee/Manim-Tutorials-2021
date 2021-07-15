from manim import *


class Tute1(ThreeDScene):
    def construct(self):

        axes = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            z_range=[-6, 6, 1],
            x_length=8,
            y_length=6,
            z_length=6,
        )

        graph = axes.get_graph(lambda x: x ** 2, x_range=[-2, 2, 1], color=YELLOW)
        rects = axes.get_riemann_rectangles(
            graph=graph, x_range=[-2, 2], dx=0.1, stroke_color=WHITE
        )

        graph2 = axes.get_parametric_curve(
            lambda t: np.array([np.cos(t), np.sin(t), t]),
            t_range=[-2 * PI, 2 * PI],
            color=RED,
        )

        self.add(axes, graph)
        self.wait()

        ##THE CAMERA IS AUTO SET TO PHI = 0 and THETA = -90

        self.move_camera(phi=60 * DEGREES)
        self.wait()
        self.move_camera(theta=-45 * DEGREES)

        self.begin_ambient_camera_rotation(
            rate=PI / 10, about="theta"
        )  # Rotates at a rate of radians per second
        self.wait()
        self.play(Create(rects), run_time=3)
        self.play(Create(graph2))
        self.wait()
        self.stop_ambient_camera_rotation()

        self.wait()
        self.begin_ambient_camera_rotation(
            rate=PI / 10, about="phi"
        )  # Rotates at a rate of radians per second
        self.wait(2)
        self.stop_ambient_camera_rotation()


class Tute2(ThreeDScene):
    def construct(self):

        code = (
            Code(
                "Tute4Code1.py",
                style=Code.styles_list[12],
                background="window",
                language="python",
                insert_line_no=True,
                tab_width=2,
                line_spacing=0.3,
                scale_factor=0.5,
                font="Monospace",
            )
            .set(width=5)
            .to_edge(UR, buff=0)
        )

        axes = ThreeDAxes()

        graph = axes.get_graph(lambda x: x ** 2, x_range=[-2, 2], color=YELLOW)

        surface = ParametricSurface(
            lambda u, v: axes.c2p(v * np.cos(u), v * np.sin(u), 0.5 * v ** 2),
            u_min=0,
            u_max=2 * PI,
            v_min=0,
            v_max=3,
            checkerboard_colors=[GREEN, RED],
        )

        three_d_stuff = VGroup(axes, graph, surface)

        self.play(Write(code), run_time=5)
        self.wait()
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        self.add(axes, graph)
        self.begin_ambient_camera_rotation(rate=PI / 20)
        self.play(Create(surface))
        self.play(three_d_stuff.animate.shift(LEFT * 5))


class Tute3(ThreeDScene):
    def construct(self):

        self.set_camera_orientation(phi=45 * DEGREES, theta=-45 * DEGREES)

        axes = ThreeDAxes(y_range=[-3, 10, 3], y_length=7).add_coordinates()

        graph = axes.get_graph(lambda x: x, x_range=[0, 3], color=RED_B)

        area = axes.get_area(graph=graph, x_range=[0, 3])

        e = ValueTracker(0)

        surface = always_redraw(
            lambda: ParametricSurface(
                lambda u, v: axes.c2p(v, v * np.cos(u), v * np.sin(u)),
                u_min=0,
                u_max=e.get_value(),
                v_min=0,
                v_max=3,
                checkerboard_colors=[GREEN, PURPLE],
            )
        )
        self.add(axes, surface)
        self.begin_ambient_camera_rotation(rate=PI / 15)
        self.play(LaggedStart(Create(graph), Create(area)))
        self.play(
            Rotating(area, axis=RIGHT, radians=2 * PI, about_point=axes.c2p(0, 0, 0)),
            e.animate.set_value(2 * PI),
            run_time=6,
            rate_func=linear,
        )
        self.stop_ambient_camera_rotation()
        self.wait()
