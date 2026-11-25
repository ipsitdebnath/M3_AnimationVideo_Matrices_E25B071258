"""
=============================================================================
Linear Algebra and Calculus (M3) • Internal Assessment: Animation Video
Topic: Matrices & Matrix Operations: Geometry, Algebra & Intuition
Student: Ipsit Debnath (ID: E25B071258)
Branch: BTech Computer Science (AI & ML)
Script: manim_matrix_operations.py
Framework: Manim Community Edition (v0.18+)
Target: 1080p 16:9 Landscape, 30fps / 60fps
=============================================================================
This production script implements the complete 6-Scene storyboard:
  Scene 1: Hook / Context (Digital data to geometric motion)
  Scene 2: Concept Introduction & Dimensions (m x n, entry a_ij)
  Scene 3: Visual Intuition (Matrices as Space Transformers, i-hat and j-hat)
  Scene 4: Step-by-Step Worked Example (Addition, Scalar, Matrix Multiplication)
  Scene 5: Geometric Interpretation (Composition BA vs AB, Non-commutativity)
  Scene 6: Summary, Takeaways & Credits
=============================================================================
"""

from manim import *
import numpy as np

# Global Color Palette (Modern Dark High-Contrast Aesthetic)
COLOR_BG = "#0d1117"
COLOR_CYAN = "#00d2ff"       # Basis vector i-hat, column 1, x-axis
COLOR_YELLOW = "#ffb703"     # Basis vector j-hat, column 2, y-axis
COLOR_GREEN = "#06d6a0"      # Success, results, matching dimensions
COLOR_CORAL = "#ff5964"      # Dimension mismatch, warnings, highlights
COLOR_TEXT = "#f0f6fc"       # Primary text
COLOR_MUTED = "#8b949e"      # Secondary annotations


class Scene1_HookContext(Scene):
    """
    Scene 1: Hook and Motivation.
    Connects real-world data (pixels, 3D graphics) to matrix mathematical representations.
    """
    def construct(self):
        self.camera.background_color = COLOR_BG

        # Title Card
        title = Text("Matrices & Matrix Operations", font_size=44, color=COLOR_CYAN, weight=BOLD)
        subtitle = Text("Geometry, Algebra & Intuition", font_size=30, color=COLOR_TEXT)
        author = Text("Linear Algebra & Calculus (M3) • Ipsit Debnath", font_size=20, color=COLOR_MUTED)

        title_group = VGroup(title, subtitle, author).arrange(DOWN, buff=0.35)
        self.play(FadeIn(title_group, shift=UP * 0.5), run_time=2.0)
        self.wait(1.5)
        self.play(FadeOut(title_group, shift=UP * 0.5), run_time=1.0)

        # Motivating Question
        question = Text("What is a Matrix?", font_size=42, color=COLOR_TEXT)
        sub_q = Text("A sterile table of numbers... or something far more powerful?", font_size=24, color=COLOR_MUTED)
        q_group = VGroup(question, sub_q).arrange(DOWN, buff=0.3)
        self.play(Write(q_group), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(q_group), run_time=0.8)

        # Visual: Pixel Grid to Matrix
        grid_label = Text("Digital Image (Pixel Intensity Grid)", font_size=24, color=COLOR_CYAN).to_edge(UP)
        pixel_matrix = Matrix(
            [[255, 128, 45],
             [180, 220, 90],
             [30,  85, 240]],
            element_to_mobject_config={"font_size": 28, "color": COLOR_TEXT}
        ).scale(1.1)

        self.play(FadeIn(grid_label), Create(pixel_matrix), run_time=1.5)
        self.wait(1.5)

        # Transition: Geometric Motion Equation
        geom_label = Text("Computer Graphics & Robotics (Transformations)", font_size=24, color=COLOR_YELLOW).to_edge(UP)
        equation = MathTex(
            r"\mathbf{x}' = A \mathbf{x}",
            font_size=48,
            color=COLOR_GREEN
        ).next_to(pixel_matrix, DOWN, buff=0.8)

        self.play(Transform(grid_label, geom_label), Write(equation), run_time=1.5)
        self.wait(2.0)
        self.play(FadeOut(grid_label), FadeOut(pixel_matrix), FadeOut(equation), run_time=1.0)


class Scene2_ConceptIntroduction(Scene):
    """
    Scene 2: Concept Definition & Notation.
    Covers m x n dimensions, entry meaning a_ij, and vector relations.
    """
    def construct(self):
        self.camera.background_color = COLOR_BG

        # Section Header
        header = Text("1. Anatomy of a Matrix", font_size=36, color=COLOR_CYAN).to_edge(UP)
        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.8)

        # 3x2 Matrix Display
        mat_mobj = Matrix(
            [[r"a_{11}", r"a_{12}"],
             [r"a_{21}", r"a_{22}"],
             [r"a_{31}", r"a_{32}"]],
            element_to_mobject_config={"font_size": 36, "color": COLOR_TEXT}
        ).scale(1.2).shift(LEFT * 2)

        self.play(Create(mat_mobj), run_time=1.2)

        # Dimension Breakdown Callout
        dim_box = VGroup(
            Text("Dimensions: m × n", font_size=28, color=COLOR_YELLOW, weight=BOLD),
            Text("m = Rows (Horizontal: 3)", font_size=22, color=COLOR_YELLOW),
            Text("n = Columns (Vertical: 2)", font_size=22, color=COLOR_CYAN),
            Text("Entry: a_ij  (Row i, Column j)", font_size=22, color=COLOR_GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).shift(RIGHT * 3)

        self.play(FadeIn(dim_box, shift=LEFT * 0.5), run_time=1.2)
        self.wait(1.5)

        # Highlight Row 2
        row2_rect = SurroundingRectangle(mat_mobj.get_rows()[1], color=COLOR_YELLOW, buff=0.15)
        row_lbl = Text("Row 2 (i = 2)", font_size=20, color=COLOR_YELLOW).next_to(row2_rect, LEFT)
        self.play(Create(row2_rect), FadeIn(row_lbl), run_time=0.8)
        self.wait(1.0)

        # Highlight Column 1
        col1_rect = SurroundingRectangle(mat_mobj.get_columns()[0], color=COLOR_CYAN, buff=0.15)
        col_lbl = Text("Col 1 (j = 1)", font_size=20, color=COLOR_CYAN).next_to(col1_rect, DOWN)
        self.play(Create(col1_rect), FadeIn(col_lbl), run_time=0.8)
        self.wait(1.0)

        # Highlight entry a_21 intersection
        entry_rect = SurroundingRectangle(mat_mobj.get_entries()[2], color=COLOR_GREEN, buff=0.1)
        self.play(Transform(row2_rect, entry_rect), FadeOut(col1_rect), FadeOut(row_lbl), FadeOut(col_lbl), run_time=0.8)
        self.wait(1.5)

        self.play(FadeOut(mat_mobj), FadeOut(row2_rect), FadeOut(dim_box), FadeOut(header), run_time=1.0)


class Scene3_VisualIntuition(LinearTransformationScene):
    """
    Scene 3: Visual Intuition.
    Demonstrates matrices as linear transformations of space tracking i-hat and j-hat.
    """
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
            basis_vector_stroke_width=6,
            **kwargs
        )

    def construct(self):
        self.camera.background_color = COLOR_BG

        # Title
        title = Text("2. Matrices as Space Transformers", font_size=32, color=COLOR_CYAN).to_corner(UL)
        self.add_transformable_mobject(title)
        self.play(FadeIn(title), run_time=0.8)

        # Introduce Basis Vectors
        i_label = MathTex(r"\hat{i} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}", font_size=26, color=COLOR_CYAN).to_corner(UR).shift(DOWN * 0.5)
        j_label = MathTex(r"\hat{j} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}", font_size=26, color=COLOR_YELLOW).next_to(i_label, DOWN, buff=0.3)

        self.play(FadeIn(i_label), FadeIn(j_label), run_time=1.0)
        self.wait(1.0)

        # Matrix to Apply: M = [[2, 1], [0, 1.5]]
        matrix_tex = MathTex(
            r"M = \begin{bmatrix} 2 & 1 \\ 0 & 1.5 \end{bmatrix}",
            font_size=34,
            color=COLOR_TEXT
        ).next_to(j_label, DOWN, buff=0.4)

        col_explanation = VGroup(
            MathTex(r"\text{Col 1: } T(\hat{i}) = \begin{bmatrix} 2 \\ 0 \end{bmatrix}", font_size=24, color=COLOR_CYAN),
            MathTex(r"\text{Col 2: } T(\hat{j}) = \begin{bmatrix} 1 \\ 1.5 \end{bmatrix}", font_size=24, color=COLOR_YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(matrix_tex, DOWN, buff=0.3)

        self.play(Write(matrix_tex), FadeIn(col_explanation), run_time=1.2)
        self.wait(1.5)

        # Apply Linear Transformation
        transformation_matrix = [[2, 1], [0, 1.5]]
        self.apply_matrix(transformation_matrix, run_time=3.0)
        self.wait(2.5)


class Scene4_WorkedExample(Scene):
    """
    Scene 4: Step-by-Step Worked Example.
    Covers Matrix Addition, Scalar Multiplication, and Matrix Multiplication with full arithmetic.
    """
    def construct(self):
        self.camera.background_color = COLOR_BG

        header = Text("3. Matrix Operations: Step-by-Step", font_size=36, color=COLOR_CYAN).to_edge(UP)
        self.play(FadeIn(header), run_time=0.8)

        # --- Part A: Matrix Addition ---
        add_title = Text("Part A: Matrix Addition (Dimensions Must Match: 2×2)", font_size=24, color=COLOR_YELLOW).next_to(header, DOWN, buff=0.3)
        self.play(FadeIn(add_title), run_time=0.6)

        mat_a = Matrix([[3, 1], [0, 2]], element_to_mobject_config={"font_size": 32})
        mat_plus = MathTex("+", font_size=36)
        mat_b = Matrix([[1, 2], [4, 5]], element_to_mobject_config={"font_size": 32})
        mat_eq = MathTex("=", font_size=36)
        mat_sum_steps = Matrix([[r"3+1", r"1+2"], [r"0+4", r"2+5"]], element_to_mobject_config={"font_size": 28})
        mat_sum_res = Matrix([[4, 3], [4, 7]], element_to_mobject_config={"font_size": 32, "color": COLOR_GREEN})

        add_group_1 = VGroup(mat_a, mat_plus, mat_b, mat_eq, mat_sum_steps).arrange(RIGHT, buff=0.25).shift(UP * 0.5)
        self.play(Create(mat_a), Write(mat_plus), Create(mat_b), Write(mat_eq), Create(mat_sum_steps), run_time=2.0)
        self.wait(1.0)

        mat_sum_res.move_to(mat_sum_steps)
        self.play(Transform(mat_sum_steps, mat_sum_res), run_time=1.0)
        self.wait(1.5)

        self.play(FadeOut(add_title), FadeOut(add_group_1), FadeOut(mat_sum_steps), run_time=0.8)

        # --- Part B: Scalar Multiplication ---
        scalar_title = Text("Part B: Scalar Multiplication (Scale Every Entry by k=3)", font_size=24, color=COLOR_YELLOW).next_to(header, DOWN, buff=0.3)
        self.play(FadeIn(scalar_title), run_time=0.6)

        k_tex = MathTex("3 \cdot", font_size=36)
        mat_scale_steps = Matrix([[r"3(3)", r"3(1)"], [r"3(0)", r"3(2)"]], element_to_mobject_config={"font_size": 28})
        mat_scale_res = Matrix([[9, 3], [0, 6]], element_to_mobject_config={"font_size": 32, "color": COLOR_GREEN})

        scalar_group = VGroup(k_tex, mat_a.copy(), mat_eq.copy(), mat_scale_steps).arrange(RIGHT, buff=0.3).shift(UP * 0.5)
        self.play(Write(k_tex), Create(scalar_group[1]), Write(scalar_group[2]), Create(mat_scale_steps), run_time=1.8)
        self.wait(1.0)

        mat_scale_res.move_to(mat_scale_steps)
        self.play(Transform(mat_scale_steps, mat_scale_res), run_time=1.0)
        self.wait(1.5)

        self.play(FadeOut(scalar_title), FadeOut(scalar_group), FadeOut(mat_scale_steps), run_time=0.8)

        # --- Part C: Matrix Multiplication ---
        mult_title = Text("Part C: Matrix Multiplication (Row × Column Dot Product)", font_size=24, color=COLOR_YELLOW).next_to(header, DOWN, buff=0.3)
        dim_rule = MathTex(r"(2 \times \mathbf{2}) \times (\mathbf{2} \times 2) \implies 2 \times 2", font_size=26, color=COLOR_GREEN).next_to(mult_title, DOWN, buff=0.2)
        self.play(FadeIn(mult_title), FadeIn(dim_rule), run_time=0.8)

        mat_a_mult = Matrix([[3, 1], [0, 2]], element_to_mobject_config={"font_size": 30}).shift(LEFT * 3.5 + DOWN * 0.5)
        mat_b_mult = Matrix([[1, 2], [4, 5]], element_to_mobject_config={"font_size": 30}).next_to(mat_a_mult, RIGHT, buff=0.4)
        c_label = MathTex("C = AB =", font_size=30).next_to(mat_b_mult, RIGHT, buff=0.4)

        self.play(Create(mat_a_mult), Create(mat_b_mult), Write(c_label), run_time=1.2)

        # Explicit Step-by-Step Dot Products
        calc_steps = VGroup(
            MathTex(r"C_{11} = (3 \cdot 1) + (1 \cdot 4) = 3 + 4 = \mathbf{7}", font_size=24, color=COLOR_CYAN),
            MathTex(r"C_{12} = (3 \cdot 2) + (1 \cdot 5) = 6 + 5 = \mathbf{11}", font_size=24, color=COLOR_CYAN),
            MathTex(r"C_{21} = (0 \cdot 1) + (2 \cdot 4) = 0 + 8 = \mathbf{8}", font_size=24, color=COLOR_YELLOW),
            MathTex(r"C_{22} = (0 \cdot 2) + (2 \cdot 5) = 0 + 10 = \mathbf{10}", font_size=24, color=COLOR_YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).shift(RIGHT * 3.2 + DOWN * 0.5)

        for step in calc_steps:
            self.play(Write(step), run_time=0.9)
            self.wait(0.3)

        mat_c_final = Matrix([[7, 11], [8, 10]], element_to_mobject_config={"font_size": 30, "color": COLOR_GREEN}).next_to(c_label, RIGHT, buff=0.3)
        self.play(Create(mat_c_final), run_time=1.0)
        self.wait(2.5)

        self.play(
            FadeOut(header), FadeOut(mult_title), FadeOut(dim_rule),
            FadeOut(mat_a_mult), FadeOut(mat_b_mult), FadeOut(c_label),
            FadeOut(calc_steps), FadeOut(mat_c_final),
            run_time=1.0
        )


class Scene5_GeometricInterpretation(Scene):
    """
    Scene 5: Geometric Interpretation & Non-Commutativity.
    Explains matrix multiplication as composition of transformations: why AB != BA.
    """
    def construct(self):
        self.camera.background_color = COLOR_BG

        title = Text("4. Why Row × Column? Composition & Order", font_size=36, color=COLOR_CYAN).to_edge(UP)
        self.play(FadeIn(title), run_time=0.8)

        # Concept Formulation
        composition_formula = MathTex(
            r"T_{BA}(\mathbf{x}) = B\Big(A(\mathbf{x})\Big) = (BA)\mathbf{x}",
            font_size=36,
            color=COLOR_YELLOW
        ).shift(UP * 1.5)

        comp_desc = Text(
            "Matrix Multiplication represents performing consecutive geometric transformations!\nTransformation A is applied first, then B is applied to the result.",
            font_size=22,
            color=COLOR_TEXT,
            t2c={"Transformation A": COLOR_CYAN, "B": COLOR_YELLOW}
        ).next_to(composition_formula, DOWN, buff=0.3)

        self.play(Write(composition_formula), FadeIn(comp_desc), run_time=1.5)
        self.wait(2.0)

        # Non-Commutativity Revelation
        box_nc = RoundedRectangle(corner_radius=0.2, height=2.2, width=8.5, color=COLOR_CORAL, fill_color="#161b22", fill_opacity=0.9).shift(DOWN * 1.2)
        nc_title = Text("Non-Commutativity: Order Matters!", font_size=26, color=COLOR_CORAL, weight=BOLD).next_to(box_nc.get_top(), DOWN, buff=0.2)
        nc_formula = MathTex(
            r"AB = \begin{bmatrix} 7 & 11 \\ 8 & 10 \end{bmatrix} \quad \neq \quad BA = \begin{bmatrix} 3 & 5 \\ 12 & 14 \end{bmatrix}",
            font_size=30,
            color=COLOR_TEXT
        ).next_to(nc_title, DOWN, buff=0.25)

        self.play(Create(box_nc), FadeIn(nc_title), Write(nc_formula), run_time=1.5)
        self.wait(2.5)

        self.play(FadeOut(title), FadeOut(composition_formula), FadeOut(comp_desc), FadeOut(box_nc), FadeOut(nc_title), FadeOut(nc_formula), run_time=1.0)


class Scene6_SummaryCredits(Scene):
    """
    Scene 6: Summary, Takeaways, References & AI Disclosure.
    """
    def construct(self):
        self.camera.background_color = COLOR_BG

        header = Text("Key Takeaways & Summary", font_size=38, color=COLOR_CYAN, weight=BOLD).to_edge(UP)
        self.play(FadeIn(header), run_time=0.8)

        card1 = VGroup(
            Text("1. Dual Nature", font_size=24, color=COLOR_YELLOW, weight=BOLD),
            Text("A matrix is both a table of numbers and an active geometric transformation.", font_size=20, color=COLOR_TEXT)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        card2 = VGroup(
            Text("2. Strict Dimensions", font_size=24, color=COLOR_GREEN, weight=BOLD),
            Text("Addition needs identical sizes (m×n). Multiplication needs inner match (m×k)(k×n).", font_size=20, color=COLOR_TEXT)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        card3 = VGroup(
            Text("3. Multiplication is Composition", font_size=24, color=COLOR_CORAL, weight=BOLD),
            Text("Multiplying matrices applies sequential transformations: order matters (AB ≠ BA).", font_size=20, color=COLOR_TEXT)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        takeaways = VGroup(card1, card2, card3).arrange(DOWN, buff=0.4, aligned_edge=LEFT).shift(LEFT * 0.5 + UP * 0.2)
        for card in takeaways:
            self.play(FadeIn(card, shift=RIGHT * 0.4), run_time=0.9)
            self.wait(0.5)

        self.wait(2.0)
        self.play(FadeOut(takeaways), FadeOut(header), run_time=1.0)

        # Credits & Disclosures Frame
        credits_title = Text("Project Submission & Credits", font_size=36, color=COLOR_CYAN, weight=BOLD).to_edge(UP)
        
        info_block = VGroup(
            Text("Course: Linear Algebra and Calculus (M3) • Internal Assessment", font_size=22, color=COLOR_TEXT),
            Text("Student: Ipsit Debnath | Student ID: E25B071258 | CSE (AI & ML)", font_size=22, color=COLOR_YELLOW),
            Text("Topic: Matrices & Matrix Operations", font_size=22, color=COLOR_GREEN),
            Text("References: Strang (Linear Algebra 5e), 3Blue1Brown (Essence of LA)", font_size=18, color=COLOR_MUTED),
            Text("Audio: Royalty-free ambient background score; macOS Speech Synthesizer", font_size=18, color=COLOR_MUTED),
            Text("AI Disclosure: Visuals and scripts authored and rendered programmatically with Python & Manim", font_size=18, color=COLOR_MUTED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).shift(DOWN * 0.2)

        self.play(FadeIn(credits_title), FadeIn(info_block), run_time=1.5)
        self.wait(3.0)


class MasterVideo(Scene):
    """
    Combined sequential scene to render the complete unified animation.
    """
    def construct(self):
        Scene1_HookContext.construct(self)
        Scene2_ConceptIntroduction.construct(self)
        # Note: LinearTransformationScene logic can be chained or exported per scene
        Scene4_WorkedExample.construct(self)
        Scene5_GeometricInterpretation.construct(self)
        Scene6_SummaryCredits.construct(self)
