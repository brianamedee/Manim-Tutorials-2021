from manim import *

class GraphingIntro(Scene):
    def construct(self):

        backg_plane = NumberPlane(x_range=[-7,7,1], y_range=[-4,4,1]).add_coordinates()
        code = Code("Tute2Intro.py", style=Code.styles_list[12], background ="window", language = "python", insert_line_no = True,
        tab_width = 2, line_spacing = 0.3, scale_factor = 0.5, font="Monospace").set_width(7).to_edge(UL, buff=0)

        axes = Axes(x_range = [0,5,1], y_range = [0,3,1], 
        x_length = 5, y_length = 3,
        axis_config = {"include_tip": True, "numbers_to_exclude": [0]}
        ).add_coordinates()

        axes.to_edge(UR)
        axis_labels = axes.get_axis_labels(x_label = "x", y_label = "f(x)")

        graph = axes.get_graph(lambda x : x**0.5, x_range = [0,4], color = YELLOW)

        graphing_stuff = VGroup(axes, graph, axis_labels)

        self.play(FadeIn(backg_plane), Write(code), run_time=6)
        self.play(backg_plane.animate.set_opacity(0.3))
        self.wait()
        self.play(DrawBorderThenFill(axes), Write(axis_labels), run_time = 2)
        self.wait()
        self.play(Create(graph), run_time = 2)
        self.play(graphing_stuff.animate.shift(DOWN*4), run_time = 3)
        self.wait()
        self.play(axes.animate.shift(LEFT*3), run_time = 3)
        self.wait()

class Tute1(Scene): #ILLUSTRATING HOW TO PUT A NUMBER PLANE ON SCENE WITH A GRAPH, and a line using c2p
    def construct(self):

        backg_plane = NumberPlane(x_range=[-7,7,1], y_range=[-4,4,1])
        backg_plane.add_coordinates()
        code = Code("Tute2Code2.py", style=Code.styles_list[12], background ="window", language = "python", insert_line_no = True,
        tab_width = 2, line_spacing = 0.3, scale_factor = 0.5, font="Monospace").set_width(7).to_edge(UL, buff=0)

        my_plane = NumberPlane(x_range = [-6,6], x_length = 5,
        y_range = [-10,10], y_length=5)
        my_plane.add_coordinates()
        my_plane.shift(RIGHT*3)

        my_function = my_plane.get_graph(lambda x : 0.1*(x-5)*x*(x+5), 
        x_range=[-6,6], color = GREEN_B)

        label = MathTex("f(x)=0.1x(x-5)(x+5)").next_to(
            my_plane, UP, buff=0.2)

        area = my_plane.get_area(graph = my_function, 
        x_range = [-5,5], color = [BLUE,YELLOW])

        horiz_line = Line(
            start = my_plane.c2p(0, my_function.underlying_function(-2)),
        end = my_plane.c2p(-2, my_function.underlying_function(-2)),
        stroke_color = YELLOW, stroke_width = 10)

        self.play(FadeIn(backg_plane), Write(code), run_time=6)
        self.play(backg_plane.animate.set_opacity(0.2))
        self.wait()
        self.play(DrawBorderThenFill(my_plane), run_time=2)
        self.wait()
        self.play(Create(my_function), Write(label), run_time=2)
        self.wait()
        self.play(FadeIn(area), run_time = 2)
        self.wait()
        self.play(Create(horiz_line), run_time = 2)
        self.wait()

class Tute2(Scene):  #ILLUSTRATING POLAR PLANE WITH A SINE CURVE
    def construct(self):
        
        
        e = ValueTracker(0.01) #Tracks the end value of both functions

        plane = PolarPlane(radius_max=3).add_coordinates()
        plane.shift(LEFT*2)
        graph1 = always_redraw(lambda : 
        ParametricFunction(lambda t : plane.polar_to_point(2*np.sin(3*t), t), 
        t_range = [0, e.get_value()], color = GREEN)
        )
        dot1 = always_redraw(lambda : Dot(fill_color = GREEN, fill_opacity = 0.8).scale(0.5).move_to(graph1.get_end())
        )

        axes = Axes(x_range = [0, 4, 1], x_length=3, y_range=[-3,3,1], y_length=3).shift(RIGHT*4)
        axes.add_coordinates()
        graph2 = always_redraw(lambda : 
        axes.get_graph(lambda x : 2*np.sin(3*x), x_range = [0, e.get_value()], color = GREEN)
        )
        dot2 = always_redraw(lambda : Dot(fill_color = GREEN, fill_opacity = 0.8).scale(0.5).move_to(graph2.get_end())
        )

        title = MathTex("f(\\theta) = 2sin(3\\theta)", color = GREEN).next_to(axes, UP, buff=0.2)

        self.play(LaggedStart(
            Write(plane), Create(axes), Write(title),
            run_time=3, lag_ratio=0.5)
        )
        self.add(graph1, graph2, dot1, dot2)
        self.play(e.animate.set_value(PI), run_time = 10, rate_func = linear)
        self.wait()

class Tute3(Scene): #Showing how to call 2 planes, put graphs on each and call elements to each
    def construct(self):

        backg_plane = NumberPlane(x_range=[-7,7,1], y_range=[-4,4,1]).add_coordinates()

        plane = NumberPlane(x_range = [-4,4,1], x_length = 4, 
        y_range= [0, 20, 5], y_length=4).add_coordinates()
        plane.shift(LEFT*3+DOWN*1.5)
        plane_graph = plane.get_graph(lambda x : x**2, 
        x_range = [-4,4], color = GREEN)
        area = plane.get_riemann_rectangles(graph = plane_graph, x_range=[-2,2], dx=0.05)

        axes = Axes(x_range = [-4,4,1], x_length = 4, 
        y_range= [-20,20,5], y_length=4).add_coordinates()
        axes.shift(RIGHT*3+DOWN*1.5)
        axes_graph = axes.get_graph(lambda x : 2*x, 
        x_range=[-4,4], color = YELLOW)
        v_lines = axes.get_vertical_lines_to_graph(
            graph = axes_graph, x_range=[-3,3], num_lines = 12)

        code = Code("Tute2Code1.py", style=Code.styles_list[12], background ="window", language = "python", insert_line_no = True,
        tab_width = 2, line_spacing = 0.3, scale_factor = 0.5, font="Monospace").set_width(6).to_edge(UL, buff=0)

        self.play(FadeIn(backg_plane), Write(code), run_time=6)
        self.play(backg_plane.animate.set_opacity(0.3))
        self.play(Write(plane), Create(axes))
        self.wait()
        self.play(Create(plane_graph), Create(axes_graph), run_time = 2)
        self.add(area, v_lines)
        self.wait()

class Tute4(Scene):
    def construct(self):

        plane = ComplexPlane(axis_config = {"include_tip": True, "numbers_to_exclude": [0]}).add_coordinates()

        labels = plane.get_axis_labels(x_label = "Real", y_label="Imaginary")

        quest = MathTex("Plot \\quad 2-3i").add_background_rectangle().to_edge(UL)
        dot = Dot()
        vect1 = plane.get_vector((2,0), stroke_color = YELLOW)
        vect2 = Line(start = plane.c2p(2,0),
        end = plane.c2p(2,-3), stroke_color = YELLOW).add_tip()

        self.play(DrawBorderThenFill(plane), Write(labels))
        self.wait()
        self.play(FadeIn(quest))
        self.play(GrowArrow(vect1), dot.animate.move_to(plane.c2p(2,0)), rate_func = linear, run_time = 2)
        self.wait()
        self.play(GrowFromPoint((vect2), point = vect2.get_start()),
        dot.animate.move_to(plane.c2p(2,-3)), run_time = 2, rate_func = linear)
        self.wait()
