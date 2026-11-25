#!/usr/bin/env python3
"""
Publication-Quality PDF Generator for Storyboard
Uses Python Pillow to render multi-page A4 PDF document at 150 DPI.
No external network or browser dependencies required.
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_PDF = "Storyboard/Storyboard.pdf"

PAGE_W = 1240
PAGE_H = 1754
MARGIN_X = 70
MARGIN_Y = 60

C_BG = (255, 255, 255)
C_TEXT = (30, 41, 59)         # Slate 800
C_PRIMARY = (3, 105, 161)     # Sky 700
C_SECONDARY = (15, 23, 42)    # Slate 900
C_MUTED = (100, 116, 139)     # Slate 500
C_BORDER = (226, 232, 240)    # Slate 200
C_BOX_BG = (248, 250, 252)    # Slate 50
C_AMBER = (180, 83, 9)        # Amber 700
C_GREEN = (21, 128, 61)       # Emerald 700
C_CORAL = (185, 28, 28)       # Red 700

FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

def get_font(size, bold=False):
    p = FONT_BOLD_PATH if bold else FONT_PATH
    try:
        return ImageFont.truetype(p, size)
    except Exception:
        return ImageFont.load_default()

F_TITLE = get_font(28, bold=True)
F_SUB = get_font(18, bold=True)
F_H2 = get_font(16, bold=True)
F_H3 = get_font(14, bold=True)
F_BODY = get_font(12, bold=False)
F_BODY_BOLD = get_font(12, bold=True)
F_SMALL = get_font(10, bold=False)
F_SMALL_BOLD = get_font(10, bold=True)
F_MONO = get_font(11, bold=False)


def create_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), C_BG)
    draw = ImageDraw.Draw(img)
    return img, draw


def draw_header_banner(draw, page_num, total_pages=3):
    # Top rule
    draw.rectangle([MARGIN_X, MARGIN_Y, PAGE_W - MARGIN_X, MARGIN_Y + 70], fill=(240, 249, 255), outline=C_PRIMARY, width=2)
    draw.text((MARGIN_X + 20, MARGIN_Y + 12), "LINEAR ALGEBRA AND CALCULUS (M3) • INTERNAL ASSESSMENT", font=F_H3, fill=C_PRIMARY)
    draw.text((MARGIN_X + 20, MARGIN_Y + 38), "Animation Video Storyboard | Topic: Matrices & Matrix Operations", font=F_BODY, fill=C_SECONDARY)
    draw.text((PAGE_W - MARGIN_X - 250, MARGIN_Y + 38), "Ipsit Debnath (E25B071258 | AI & ML)", font=F_SMALL_BOLD, fill=C_MUTED)

    # Footer rule
    draw.line([(MARGIN_X, PAGE_H - 45), (PAGE_W - MARGIN_X, PAGE_H - 45)], fill=C_BORDER, width=1)
    draw.text((MARGIN_X, PAGE_H - 35), "M3 Internal Assessment • 6-Scene Storyboard Document • Deadline: 25th November", font=F_SMALL, fill=C_MUTED)
    draw.text((PAGE_W - MARGIN_X - 80, PAGE_H - 35), f"Page {page_num} of {total_pages}", font=F_SMALL_BOLD, fill=C_PRIMARY)


def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    curr = []
    for w in words:
        test = " ".join(curr + [w])
        bbox = draw.textbbox((0, 0), test, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            curr.append(w)
        else:
            if curr:
                lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))
    return lines


def build_page_1():
    img, draw = create_page()
    draw_header_banner(draw, 1)

    y = 155
    # Document Title
    draw.text((MARGIN_X, y), "Official 6-Scene Storyboard & Production Blueprint", font=F_TITLE, fill=C_PRIMARY)
    y += 40

    # Project Metadata Box
    draw.rounded_rectangle([MARGIN_X, y, PAGE_W - MARGIN_X, y + 130], radius=8, fill=C_BOX_BG, outline=C_BORDER, width=1)
    col1_x = MARGIN_X + 20
    col2_x = MARGIN_X + 560

    draw.text((col1_x, y + 15), "• Course:", font=F_BODY_BOLD, fill=C_PRIMARY)
    draw.text((col1_x + 90, y + 15), "M3 - Linear Algebra & Calculus", font=F_BODY, fill=C_TEXT)

    draw.text((col1_x, y + 42), "• Student:", font=F_BODY_BOLD, fill=C_PRIMARY)
    draw.text((col1_x + 90, y + 42), "Ipsit Debnath (ID: E25B071258 | CSE AI & ML)", font=F_BODY, fill=C_TEXT)

    draw.text((col1_x, y + 69), "• Topic:", font=F_BODY_BOLD, fill=C_PRIMARY)
    draw.text((col1_x + 90, y + 69), "Matrices & Matrix Operations: Geometry & Algebra", font=F_BODY, fill=C_TEXT)

    draw.text((col1_x, y + 96), "• Submission:", font=F_BODY_BOLD, fill=C_PRIMARY)
    draw.text((col1_x + 90, y + 96), "Public GitHub Repo + Final 1080p MP4 + Manim Code", font=F_BODY, fill=C_TEXT)

    draw.text((col2_x, y + 15), "• Video Duration:", font=F_BODY_BOLD, fill=C_AMBER)
    draw.text((col2_x + 130, y + 15), "5m 14s (Target: 5m, Max: 7m)", font=F_BODY, fill=C_TEXT)

    draw.text((col2_x, y + 42), "• Resolution:", font=F_BODY_BOLD, fill=C_GREEN)
    draw.text((col2_x + 130, y + 42), "1080p Full HD (1920×1080, 16:9)", font=F_BODY, fill=C_TEXT)

    draw.text((col2_x, y + 69), "• Weightage:", font=F_BODY_BOLD, fill=C_CORAL)
    draw.text((col2_x + 130, y + 69), "10% of Internal Assessment", font=F_BODY, fill=C_TEXT)

    draw.text((col2_x, y + 96), "• Audio Format:", font=F_BODY_BOLD, fill=C_PRIMARY)
    draw.text((col2_x + 130, y + 96), "Voiceover + Ambient Pad (-22dB)", font=F_BODY, fill=C_TEXT)

    y += 150

    # Learning Objective Card
    draw.rounded_rectangle([MARGIN_X, y, PAGE_W - MARGIN_X, y + 75], radius=6, fill=(240, 249, 255), outline=C_PRIMARY, width=2)
    draw.text((MARGIN_X + 16, y + 10), "ONE-SENTENCE LEARNING OBJECTIVE:", font=F_SMALL_BOLD, fill=C_PRIMARY)
    obj_text = '"By the end of this video, the viewer will be able to interpret any matrix both as an organized multi-dimensional data structure and as a geometric linear transformation of space, and confidently calculate and visualize matrix addition, scalar multiplication, and matrix multiplication."'
    lines = wrap_text(obj_text, F_BODY, PAGE_W - 2 * MARGIN_X - 32, draw)
    for i, line in enumerate(lines):
        draw.text((MARGIN_X + 16, y + 30 + i * 18), line, font=F_BODY, fill=C_SECONDARY)

    y += 95

    # 6-Scene Master Table
    draw.text((MARGIN_X, y), "Master 6-Scene Storyboard Architecture", font=F_H2, fill=C_SECONDARY)
    y += 28

    headers = [("Scene #", 100), ("Scene Name & Focus", 250), ("Duration", 130), ("Primary Visuals", 340), ("Mathematical Formula", 280)]
    th_x = MARGIN_X
    draw.rectangle([MARGIN_X, y, PAGE_W - MARGIN_X, y + 28], fill=C_SECONDARY)
    for title, w in headers:
        draw.text((th_x + 8, y + 6), title, font=F_SMALL_BOLD, fill=(255, 255, 255))
        th_x += w
    y += 28

    scenes_summary = [
        ("Scene 1", "Hook & Motivation\nReal-world context", "00:00 - 00:40\n(39.5s)", "Pixel grid array; rotating 3D\nwireframe coordinate cube", "x' = A · x\nImage = [a_ij]_{m×n}"),
        ("Scene 2", "Concept Introduction\nAnatomy & Notation", "00:40 - 01:24\n(43.9s)", "3×2 Matrix, amber row sweep,\ncyan col sweep, a_21 reticle", "A ∈ R^{m×n}, a_ij\nVectors v ∈ R^{n×1}"),
        ("Scene 3", "Visual Intuition\nSpace Transformers", "01:24 - 02:20\n(56.2s)", "2D coordinate grid, i-hat (cyan),\nj-hat (amber), grid warping", "M = [[2, 1], [0, 1.5]]\nCol 1 = T(i-hat), Col 2 = T(j-hat)"),
        ("Scene 4", "Worked Example\nStep-by-Step Operations", "02:20 - 03:41\n(80.9s)", "Addition match card, scalar\ndilation, row×col dot products", "(A+B)_ij = a_ij + b_ij\n(kA)_ij = k·a_ij, C_ij = Σ a_ir b_rj"),
        ("Scene 5", "Interpretation\nComposition & Geometry", "03:41 - 04:28\n(47.1s)", "AB vs BA split-screen;\nwarning banner on order", "T_BA(x) = B(A(x))\nAB ≠ BA, Area = |det(M)|"),
        ("Scene 6", "Summary & Credits\nTakeaways & Disclosure", "04:28 - 05:15\n(43.4s)", "3 Cascade Takeaway Cards;\nofficial closing credentials", "Takeaways: Duality, Dimension\nmatching, Non-commutativity")
    ]

    for row_idx, (sc_id, sc_name, sc_dur, sc_vis, sc_math) in enumerate(scenes_summary):
        row_h = 75
        fill_c = (255, 255, 255) if (row_idx % 2 == 0) else C_BOX_BG
        draw.rectangle([MARGIN_X, y, PAGE_W - MARGIN_X, y + row_h], fill=fill_c, outline=C_BORDER, width=1)

        td_x = MARGIN_X
        # Col 1
        draw.text((td_x + 8, y + 8), sc_id, font=F_BODY_BOLD, fill=C_PRIMARY)
        td_x += 100
        # Col 2
        for i, l in enumerate(sc_name.split("\n")):
            draw.text((td_x + 8, y + 8 + i * 16), l, font=F_BODY_BOLD if i == 0 else F_SMALL, fill=C_SECONDARY if i == 0 else C_MUTED)
        td_x += 250
        # Col 3
        for i, l in enumerate(sc_dur.split("\n")):
            draw.text((td_x + 8, y + 8 + i * 16), l, font=F_BODY_BOLD if i == 0 else F_SMALL, fill=C_AMBER if i == 0 else C_MUTED)
        td_x += 130
        # Col 4
        for i, l in enumerate(sc_vis.split("\n")):
            draw.text((td_x + 8, y + 8 + i * 16), l, font=F_BODY, fill=C_TEXT)
        td_x += 340
        # Col 5
        for i, l in enumerate(sc_math.split("\n")):
            draw.text((td_x + 8, y + 8 + i * 16), l, font=F_MONO, fill=C_PRIMARY)

        y += row_h

    return img


def draw_scene_box(draw, y, scene_num, title, duration, visual_text, math_text, script_text):
    box_h = 240
    draw.rounded_rectangle([MARGIN_X, y, PAGE_W - MARGIN_X, y + box_h], radius=8, fill=(255, 255, 255), outline=C_BORDER, width=2)
    
    # Header bar
    draw.rounded_rectangle([MARGIN_X, y, PAGE_W - MARGIN_X, y + 36], radius=8, fill=C_BOX_BG, outline=C_BORDER, width=1)
    draw.text((MARGIN_X + 14, y + 8), f"Scene {scene_num}: {title}", font=F_H3, fill=C_PRIMARY)
    draw.text((PAGE_W - MARGIN_X - 160, y + 10), duration, font=F_SMALL_BOLD, fill=C_AMBER)

    col_w = (PAGE_W - 2 * MARGIN_X - 40) // 2
    left_x = MARGIN_X + 16
    right_x = MARGIN_X + col_w + 30

    # Left: Visual & Math
    draw.text((left_x, y + 46), "Visual & Mathematical Plan:", font=F_SMALL_BOLD, fill=C_SECONDARY)
    vis_lines = wrap_text(visual_text, F_SMALL, col_w, draw)
    for i, line in enumerate(vis_lines[:5]):
        draw.text((left_x, y + 66 + i * 15), line, font=F_SMALL, fill=C_TEXT)

    draw.rectangle([left_x, y + 155, left_x + col_w - 10, y + 225], fill=C_BOX_BG, outline=C_BORDER, width=1)
    draw.text((left_x + 10, y + 160), "Key Mathematics / Formulas:", font=F_SMALL_BOLD, fill=C_PRIMARY)
    for i, line in enumerate(math_text.split("\n")):
        draw.text((left_x + 10, y + 180 + i * 15), line, font=F_MONO, fill=C_SECONDARY)

    # Right: Narration Script
    draw.text((right_x, y + 46), "Word-for-Word Narration Script:", font=F_SMALL_BOLD, fill=C_GREEN)
    draw.rectangle([right_x, y + 66, right_x + col_w - 10, y + 225], fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    scr_lines = wrap_text(script_text, F_SMALL, col_w - 20, draw)
    for i, line in enumerate(scr_lines[:10]):
        draw.text((right_x + 10, y + 74 + i * 14), line, font=F_SMALL, fill=C_TEXT)

    return y + box_h + 20


def build_page_2():
    img, draw = create_page()
    draw_header_banner(draw, 2)

    y = 155
    draw.text((MARGIN_X, y), "Detailed Scene-by-Scene Breakdown (Scenes 1 - 3)", font=F_TITLE, fill=C_PRIMARY)
    y += 40

    y = draw_scene_box(
        draw, y, 1, "Hook & Context — The Hidden Geometry of Our World",
        "00:00 - 00:40 (39.5s)",
        "Opening Title Card with glowing cyan typography; transition to photo pixel matrix (grayscale intensity grid 255 to 0); rotating 3D wireframe cube demonstrating coordinate transformations in computer games.",
        "x' = A · x  (Transformation Law)\nImage Array = [a_ij]_{5×5} (0 = Black, 255 = White)",
        "Have you ever wondered how your phone rotates a photo in a split second, how computer graphics render lifelike 3D worlds in video games, or how AI models process millions of visual signals? Behind every one of these technological wonders lies a universal mathematical language: the matrix. In this video, we discover what a matrix truly represents and how simple numbers in a grid control the geometry of space itself."
    )

    y = draw_scene_box(
        draw, y, 2, "Concept Introduction — Anatomy of a Matrix & Notation",
        "00:40 - 01:24 (43.9s)",
        "Display 3×2 matrix with bracket geometry; horizontal amber highlight sweeps rows 1 to 3; vertical cyan highlight sweeps cols 1 to 2; glowing reticle highlights entry a_21 with index callouts i and j.",
        "A = [ [a11, a12], [a21, a22], [a31, a32] ] ∈ R^{3×2}\nDimension = m × n (Rows × Cols); Vector v ∈ R^{n×1}",
        "Let us begin with the formal definition. Mathematically, a matrix is a rectangular array of numbers arranged in horizontal rows and vertical columns. We describe any matrix by its dimensions: m by n. An easy memory trick is Row-Column, just like Roman Colonists. Any individual number is called an entry, denoted as a_ij, where i specifies row and j specifies column. When a matrix has only one column, it is a column vector!"
    )

    y = draw_scene_box(
        draw, y, 3, "Visual Intuition — Matrices as Space Transformers",
        "01:24 - 02:20 (56.2s)",
        "2D Cartesian coordinate grid; basis vectors i-hat (cyan) at (1,0) and j-hat (amber) at (0,1); space continuously warps to matrix M = [[2, 1], [0, 1.5]]; grid lines remain straight and parallel; origin fixed.",
        "M = [ [2, 1], [0, 1.5] ]\nT(i-hat) = [2, 0]^T,  T(j-hat) = [1, 1.5]^T",
        "Now comes the profound visual insight: a matrix is not just a passive table of stored numbers; it is an active geometric function that transforms space! In two dimensions, every coordinate is tracked by two unit basis vectors: i-hat and j-hat. When space undergoes a linear transformation, wherever the basis vectors land completely determines where every point lands! A matrix is literally a compact recording of where the basis vectors landed!"
    )

    return img


def build_page_3():
    img, draw = create_page()
    draw_header_banner(draw, 3)

    y = 155
    draw.text((MARGIN_X, y), "Detailed Scene-by-Scene Breakdown (Scenes 4 - 6)", font=F_TITLE, fill=C_PRIMARY)
    y += 40

    y = draw_scene_box(
        draw, y, 4, "Worked Example — Step-by-Step Operations",
        "02:20 - 03:41 (80.9s)",
        "Part A: Addition A+B with matching 2×2 check and component sums (4, 3, 4, 7); Part B: Scalar mult 3A scaling every entry (9, 3, 0, 6); Part C: Matrix mult AB with row-col dot products highlighted.",
        "C_11=(3)(1)+(1)(4)=7; C_12=(3)(2)+(1)(5)=11\nC_21=(0)(1)+(2)(4)=8; C_22=(0)(2)+(2)(5)=10\nAB = [ [7, 11], [8, 10] ]",
        "Now let us master the core operations step-by-step. First: Matrix Addition. Addition is component-wise: 3+1=4, 1+2=3, 0+4=4, 2+5=7. Second: Scalar Multiplication. Multiplying by 3 scales every entry: 9, 3, 0, 6. Third: Matrix Multiplication. Inner dimensions must match! Each entry is computed by row-column dot products. C_11=7, C_12=11, C_21=8, C_22=10. All intermediate arithmetic follows strict, verifiable logic."
    )

    y = draw_scene_box(
        draw, y, 5, "Interpretation — Composition & Non-Commutativity",
        "03:41 - 04:28 (47.1s)",
        "Split-screen comparison: Left panel shows AB = [[7, 11], [8, 10]], right panel shows BA = [[3, 5], [12, 14]]; coral alert banner emphasizes non-commutativity; shear and rotation order illustration.",
        "T_BA(x) = B(A(x))  (Function Composition)\nAB ≠ BA  (Order Matters!)\nArea Scaling Factor = |det(M)| = |ad - bc|",
        "Why is matrix multiplication defined through this row-column rule? Because matrix multiplication represents the composition of linear transformations! Multiplying B times A means applying transformation A first, and then B to the result. This immediately reveals why matrix multiplication is generally non-commutative: A times B does not equal B times A! The order of transformations changes reality!"
    )

    y = draw_scene_box(
        draw, y, 6, "Summary, Takeaways & Official Project Credits",
        "04:28 - 05:15 (43.4s)",
        "Three cascading takeaway cards: 1. Dual Nature, 2. Strict Dimensions, 3. Composition & Order; official closing credentials frame with student ID, course details, references, and AI tool disclosure.",
        "Takeaway 1: Data Table + Geometric Space Transformer\nTakeaway 2: Strict Dimension Constraints\nTakeaway 3: Sequential Transformations (AB ≠ BA)",
        "To summarize our journey, remember these three core principles: First, a matrix is both a structured data container and an engine of linear transformation. Second, operations respect geometry: addition shifts vector spaces, scalar multiplication dilates space, and matrix multiplication composes transformations. Third, order matters: matrix multiplication is non-commutative. Thank you for watching!"
    )

    return img


def generate_pdf():
    print("Generating multi-page publication-quality Storyboard PDF...")
    p1 = build_page_1()
    p2 = build_page_2()
    p3 = build_page_3()

    p1.save(
        OUTPUT_PDF,
        "PDF",
        resolution=150.0,
        save_all=True,
        append_images=[p2, p3]
    )
    print(f"✓ Storyboard PDF generated successfully: {OUTPUT_PDF}")
    size_kb = os.path.getsize(OUTPUT_PDF) / 1024
    print(f"File size: {size_kb:.2f} KB | Pages: 3")


if __name__ == "__main__":
    generate_pdf()
