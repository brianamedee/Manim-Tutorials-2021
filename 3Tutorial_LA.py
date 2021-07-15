from re import L
from manim import *
import random


class Matrix(LinearTransformationScene):
    def __init__(self):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
            show_basis_vectors=True,
        )

    def construct(self):

        matrix = [[1, 2], [2, 1]]

        matrix_tex = (
            MathTex("A = \\begin{bmatrix} 1 & 2 \\\ 2 & 1 \\end{bmatrix}")
            .to_edge(UL)
            .add_background_rectangle()
        )

        unit_square = self.get_unit_square()
        text = always_redraw(
            lambda: Tex("Det(A)").set(width=0.7).move_to(unit_square.get_center())
        )

        vect = self.get_vector([1, -2], color=PURPLE_B)

        rect1 = Rectangle(
            height=2, width=1, stroke_color=BLUE_A, fill_color=BLUE_D, fill_opacity=0.6
        ).shift(UP * 2 + LEFT * 2)

        circ1 = Circle(
            radius=1, stroke_color=BLUE_A, fill_color=BLUE_D, fill_opacity=0.6
        ).shift(DOWN * 2 + RIGHT * 1)

        self.add_transformable_mobject(vect, unit_square, rect1, circ1)
        self.add_background_mobject(matrix_tex, text)
        self.apply_matrix(matrix)

        self.wait()


class Vectors(VectorScene):
    def construct(self):

        code = (
            Code(
                "Tute3Vectors.py",
                style=Code.styles_list[12],
                background="window",
                language="python",
                insert_line_no=True,
                tab_width=2,
                line_spacing=0.3,
                scale_factor=0.5,
                font="Monospace",
            )
            .set_width(6)
            .to_edge(UL, buff=0)
        )

        plane = self.add_plane(animate=True).add_coordinates()
        self.play(Write(code), run_time=6)
        self.wait()
        vector = self.add_vector([-3, -2], color=YELLOW)

        basis = self.get_basis_vectors()
        self.add(basis)
        self.vector_to_coords(vector=vector)

        vector2 = self.add_vector([2, 2])
        self.write_vector_coordinates(vector=vector2)


class Tute1(Scene):
    def construct(self):

        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-4, 4, 1], x_length=10, y_length=7
        )
        plane.add_coordinates()
        plane.shift(RIGHT * 2)

        vect1 = Line(
            start=plane.coords_to_point(0, 0),
            end=plane.coords_to_point(3, 2),
            stroke_color=YELLOW,
        ).add_tip()
        vect1_name = (
            MathTex("\\vec{v}").next_to(vect1, RIGHT, buff=0.1).set_color(YELLOW)
        )

        vect2 = Line(
            start=plane.coords_to_point(0, 0),
            end=plane.coords_to_point(-2, 1),
            stroke_color=RED,
        ).add_tip()
        vect2_name = MathTex("\\vec{w}").next_to(vect2, LEFT, buff=0.1).set_color(RED)

        vect3 = Line(
            start=plane.coords_to_point(3, 2),
            end=plane.coords_to_point(1, 3),
            stroke_color=RED,
        ).add_tip()

        vect4 = Line(
            start=plane.coords_to_point(0, 0),
            end=plane.coords_to_point(1, 3),
            stroke_color=GREEN,
        ).add_tip()
        vect4_name = (
            MathTex("\\vec{v} + \\vec{w}")
            .next_to(vect4, LEFT, buff=0.1)
            .set_color(GREEN)
        )

        stuff = VGroup(
            plane, vect1, vect1_name, vect2, vect2_name, vect3, vect4, vect4_name
        )

        box = RoundedRectangle(
            height=1.5, width=1.5, corner_radius=0.1, stroke_color=PINK
        ).to_edge(DL)

        self.play(DrawBorderThenFill(plane), run_time=2)
        self.wait()
        self.play(
            GrowFromPoint(vect1, point=vect1.get_start()), Write(vect1_name), run_time=2
        )
        self.wait()
        self.play(
            GrowFromPoint(vect2, point=vect2.get_start()), Write(vect2_name), run_time=2
        )
        self.wait()
        self.play(
            Transform(vect2, vect3),
            vect2_name.animate.next_to(vect3, UP, buff=0.1),
            run_time=2,
        )
        self.wait()
        self.play(
            LaggedStart(GrowFromPoint(vect4, point=vect4.get_start())),
            Write(vect4_name),
            run_time=3,
            lag_ratio=1,
        )
        self.wait()
        self.add(box)
        self.wait()
        self.play(stuff.animate.move_to(box.get_center()).set(width=1.2), run_time=3)
        self.wait()
