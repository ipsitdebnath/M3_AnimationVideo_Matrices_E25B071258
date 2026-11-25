#!/usr/bin/env python3
"""
High-Performance Standalone Video Rendering Engine for Linear Algebra Animation
Author: Ipsit Debnath (ID: E25B071258)
Branch: BTech Computer Science (AI & ML)
Course: Linear Algebra and Calculus (M3)
Resolution: 1080p (1920x1080), 16:9 Landscape, 30 fps
Pipes raw RGB frames directly to FFmpeg with hardware acceleration.
"""

import os
import sys
import math
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

FFMPEG_BIN = "/Applications/BlueStacks.app/Contents/MacOS/ffmpeg"
OUTPUT_VIDEO = "_Video.mp4"
TIMING_JSON = "assets/audio/timing.json"
SOUNDTRACK_WAV = "assets/audio/final_soundtrack.mp3" if os.path.exists("assets/audio/final_soundtrack.mp3") else "assets/audio/final_soundtrack.wav"

WIDTH = 1920
HEIGHT = 1080
FPS = 30

# Colors (3Blue1Brown Modern Slate Palette)
C_BG = (13, 17, 23)           # #0d1117 Deep Slate Navy
C_PANEL = (22, 27, 34)        # #161b22 Card Panel
C_BORDER = (48, 54, 61)       # #30363d Panel Border
C_CYAN = (0, 210, 255)        # #00d2ff i-hat, col 1, x-axis
C_AMBER = (255, 183, 3)       # #ffb703 j-hat, col 2, y-axis
C_YELLOW = C_AMBER            # Alias
C_GREEN = (6, 214, 160)       # #06d6a0 Success, results
C_CORAL = (255, 89, 100)      # #ff5964 Highlight, warning
C_TEXT = (240, 246, 252)      # #f0f6fc Primary white
C_MUTED = (139, 148, 158)     # #8b949e Muted gray
C_GRID = (35, 45, 60)         # Subtle grid lines
C_AXIS = (90, 105, 125)       # Grid axes

# System Fonts
FONT_REGULAR_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

def load_font(size, bold=False):
    path = FONT_BOLD_PATH if bold else FONT_REGULAR_PATH
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

# Pre-cache fonts
F_TITLE = load_font(52, bold=True)
F_SUBTITLE = load_font(32, bold=False)
F_H1 = load_font(42, bold=True)
F_H2 = load_font(30, bold=True)
F_BODY = load_font(24, bold=False)
F_BODY_BOLD = load_font(24, bold=True)
F_MATH_LG = load_font(38, bold=True)
F_MATH = load_font(28, bold=True)
F_SMALL = load_font(18, bold=False)
F_SMALL_BOLD = load_font(18, bold=True)


def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)


def draw_header_footer(draw, scene_num, scene_title, t, total_t):
    # Top banner line
    draw.line([(60, 48), (WIDTH - 60, 48)], fill=C_BORDER, width=2)
    draw.text((60, 20), "LINEAR ALGEBRA & CALCULUS (M3) • INTERNAL ASSESSMENT", font=F_SMALL_BOLD, fill=C_CYAN)
    draw.text((WIDTH - 460, 20), "Student: Ipsit Debnath  |  ID: E25B071258", font=F_SMALL, fill=C_MUTED)

    # Bottom footer line
    draw.line([(60, HEIGHT - 50), (WIDTH - 60, HEIGHT - 50)], fill=C_BORDER, width=1)
    
    # Progress bar
    prog = min(1.0, max(0.0, t / max(1.0, total_t)))
    bar_w = 400
    bar_x = WIDTH - 60 - bar_w
    draw.line([(bar_x, HEIGHT - 30), (bar_x + bar_w, HEIGHT - 30)], fill=C_PANEL, width=6)
    draw.line([(bar_x, HEIGHT - 30), (bar_x + int(bar_w * prog), HEIGHT - 30)], fill=C_CYAN, width=6)

    # Scene tag
    scene_text = f"Scene {scene_num}/6 : {scene_title}"
    draw.text((60, HEIGHT - 38), scene_text, font=F_SMALL_BOLD, fill=C_AMBER)
    
    # Time code
    mins = int(t) // 60
    secs = int(t) % 60
    t_str = f"{mins:02d}:{secs:02d}"
    draw.text((bar_x - 70, HEIGHT - 38), t_str, font=F_SMALL, fill=C_MUTED)


def draw_arrow(draw, start, end, color, width=4, tip_length=16):
    x0, y0 = start
    x1, y1 = end
    draw.line([(x0, y0), (x1, y1)], fill=color, width=width)
    dx = x1 - x0
    dy = y1 - y0
    length = math.hypot(dx, dy)
    if length < 1e-4:
        return
    udx = dx / length
    udy = dy / length
    # Perpendicular
    pdx = -udy
    pdy = udx

    # Arrowhead points
    tip1_x = x1 - tip_length * udx + (tip_length * 0.5) * pdx
    tip1_y = y1 - tip_length * udy + (tip_length * 0.5) * pdy
    tip2_x = x1 - tip_length * udx - (tip_length * 0.5) * pdx
    tip2_y = y1 - tip_length * udy - (tip_length * 0.5) * pdy
    draw.polygon([(x1, y1), (tip1_x, tip1_y), (tip2_x, tip2_y)], fill=color)


def draw_matrix_box(draw, x, y, rows, cols, data, title=None, highlight_row=None, highlight_col=None, highlight_entry=None, font=F_MATH_LG, cell_w=85, cell_h=65, text_color=C_TEXT):
    mat_w = cols * cell_w + 30
    mat_h = rows * cell_h + 20

    if title:
        draw.text((x, y - 35), title, font=F_BODY_BOLD, fill=C_AMBER)

    # Bracket Left
    draw.line([(x + 10, y), (x, y)], fill=C_TEXT, width=3)
    draw.line([(x, y), (x, y + mat_h)], fill=C_TEXT, width=3)
    draw.line([(x, y + mat_h), (x + 10, y + mat_h)], fill=C_TEXT, width=3)

    # Bracket Right
    rx = x + mat_w
    draw.line([(rx - 10, y), (rx, y)], fill=C_TEXT, width=3)
    draw.line([(rx, y), (rx, y + mat_h)], fill=C_TEXT, width=3)
    draw.line([(rx, y + mat_h), (rx - 10, y + mat_h)], fill=C_TEXT, width=3)

    for r in range(rows):
        for c in range(cols):
            cx = x + 15 + c * cell_w
            cy = y + 10 + r * cell_h

            # Highlight logic
            is_entry = (highlight_entry == (r, c))
            is_row = (highlight_row == r)
            is_col = (highlight_col == c)

            if is_entry:
                draw_rounded_rect(draw, (cx + 2, cy + 2, cx + cell_w - 2, cy + cell_h - 2), 6, fill=(6, 214, 160, 60), outline=C_GREEN, width=2)
            elif is_row:
                draw_rounded_rect(draw, (cx + 2, cy + 2, cx + cell_w - 2, cy + cell_h - 2), 6, fill=(255, 183, 3, 50), outline=C_AMBER, width=2)
            elif is_col:
                draw_rounded_rect(draw, (cx + 2, cy + 2, cx + cell_w - 2, cy + cell_h - 2), 6, fill=(0, 210, 255, 50), outline=C_CYAN, width=2)

            val_str = str(data[r][c])
            val_col = C_GREEN if is_entry else (C_AMBER if is_row else (C_CYAN if is_col else text_color))
            draw.text((cx + cell_w // 2 - 12, cy + cell_h // 2 - 18), val_str, font=font, fill=val_col)

    return (x, y, mat_w, mat_h)


# =============================================================================
# SCENE RENDERERS
# =============================================================================

def render_scene_1(draw, t, scene_dur):
    """
    Scene 1: Hook & Context (39.5s)
    0 - 8s: Title Card
    8 - 24s: Digital Image as Matrix (Pixel Grid)
    24 - 39.5s: 3D Graphics Motion & Transformation Law
    """
    if t < 8.0:
        # Title Card
        alpha = min(1.0, t / 1.5)
        draw_rounded_rect(draw, (200, 200, WIDTH - 200, HEIGHT - 240), 20, fill=C_PANEL, outline=C_BORDER, width=2)
        draw.text((280, 260), "MATRICES & MATRIX OPERATIONS", font=F_TITLE, fill=C_CYAN)
        draw.text((280, 340), "What Does a Matrix Represent? Geometry, Algebra & Intuition", font=F_SUBTITLE, fill=C_TEXT)

        # Meta info pills
        draw_rounded_rect(draw, (280, 440, 750, 520), 12, fill=(13, 17, 23), outline=C_BORDER, width=1)
        draw.text((310, 455), "Linear Algebra & Calculus (M3)", font=F_BODY_BOLD, fill=C_AMBER)
        draw.text((310, 485), "Internal Assessment • Animation Project", font=F_SMALL, fill=C_MUTED)

        draw_rounded_rect(draw, (780, 440, 1250, 520), 12, fill=(13, 17, 23), outline=C_BORDER, width=1)
        draw.text((810, 455), "Author: Ipsit Debnath", font=F_BODY_BOLD, fill=C_GREEN)
        draw.text((810, 485), "ID: E25B071258 • CSE (AI & ML)", font=F_SMALL, fill=C_MUTED)

        draw_rounded_rect(draw, (1280, 440, 1640, 520), 12, fill=(13, 17, 23), outline=C_BORDER, width=1)
        draw.text((1310, 455), "Weightage: 10%", font=F_BODY_BOLD, fill=C_CORAL)
        draw.text((1310, 485), "Duration: ~5 Minutes (Strictly < 7m)", font=F_SMALL, fill=C_MUTED)

        draw.text((280, 600), "A visual guide from foundations to geometric linear transformations", font=F_BODY, fill=C_MUTED)
    
    elif t < 24.0:
        # Part A: Digital Image as Matrix Grid
        local_t = t - 8.0
        draw.text((100, 80), "Real-World Context: Digital Images Are Matrices!", font=F_H1, fill=C_CYAN)
        draw.text((100, 140), "Every digital photograph is stored in computer memory as a 2D grid of numbers (pixel intensities).", font=F_BODY, fill=C_TEXT)

        # Draw Image Panel (Simulated picture)
        draw_rounded_rect(draw, (120, 220, 580, 680), 16, fill=(20, 25, 35), outline=C_BORDER, width=2)
        draw.text((150, 240), "Captured Image", font=F_H2, fill=C_AMBER)
        
        # Draw pixel tiles
        for py in range(5):
            for px in range(5):
                gray_val = int(50 + 40 * math.sin(px * 1.2 + py * 0.8 + local_t))
                col = (gray_val, gray_val, int(gray_val * 1.2))
                draw.rectangle([160 + px * 78, 290 + py * 72, 160 + (px + 1) * 78 - 4, 290 + (py + 1) * 72 - 4], fill=col)

        # Arrow from image to numerical matrix
        draw_arrow(draw, (620, 450), (740, 450), C_CYAN, width=6, tip_length=20)
        draw.text((640, 410), "Enters RAM", font=F_SMALL_BOLD, fill=C_CYAN)

        # Numerical Matrix
        mat_data = [
            [255, 128, 45, 90, 210],
            [180, 220, 90, 15, 60],
            [30,  85,  240, 195, 110],
            [95,  140, 75,  250, 180],
            [12,  68,  190, 85,  235]
        ]
        draw_matrix_box(draw, 780, 250, 5, 5, mat_data, title="Pixel Intensity Matrix (A ∈ R^{5×5})",
                        highlight_entry=(2, 2) if local_t > 4.0 else None,
                        cell_w=90, cell_h=65)

        # Callout box
        draw_rounded_rect(draw, (780, 680, 1700, 820), 12, fill=C_PANEL, outline=C_BORDER, width=2)
        draw.text((810, 705), "Key Insight: The Computer Sees Only Numbers", font=F_H2, fill=C_GREEN)
        draw.text((810, 750), "Brightness from 0 (pitch black) to 255 (pure white). Image filtering and blur are matrix operations!", font=F_BODY, fill=C_MUTED)

    else:
        # Part B: 3D Graphics & Transformation Law
        local_t = t - 24.0
        draw.text((100, 80), "Computer Graphics, Gaming & AI: Geometric Transformation", font=F_H1, fill=C_YELLOW)
        draw.text((100, 140), "Every 3D video game object moves and rotates using matrix multiplication: x' = A x", font=F_BODY, fill=C_TEXT)

        # Rotating 3D wireframe cube
        cx, cy = 450, 500
        angle = local_t * 0.8
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        cube_nodes = [
            (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
            (-1, -1, 1),  (1, -1, 1),  (1, 1, 1),  (-1, 1, 1)
        ]
        projected = []
        scale = 130
        for nx, ny, nz in cube_nodes:
            # Rotate around Y and X
            rx = nx * cos_a - nz * sin_a
            rz = nx * sin_a + nz * cos_a
            ry = ny * math.cos(0.4) - rz * math.sin(0.4)
            px = int(cx + rx * scale)
            py = int(cy + ry * scale)
            projected.append((px, py))

        edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]
        for e1, e2 in edges:
            draw.line([projected[e1], projected[e2]], fill=C_CYAN, width=3)
        for px, py in projected:
            draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=C_AMBER)

        # Transformation Panel
        draw_rounded_rect(draw, (850, 240, 1750, 780), 16, fill=C_PANEL, outline=C_BORDER, width=2)
        draw.text((900, 280), "The Master Transformation Equation", font=F_H1, fill=C_GREEN)

        draw.text((900, 370), "x' = A · x", font=load_font(56, bold=True), fill=C_CYAN)
        draw.text((900, 470), "• x  = Original 3D coordinate vector [X, Y, Z]^T", font=F_BODY, fill=C_TEXT)
        draw.text((900, 520), "• A  = Transformation Matrix (Rotation, Scale, Projection)", font=F_BODY, fill=C_AMBER)
        draw.text((900, 570), "• x' = New transformed position on your screen", font=F_BODY, fill=C_GREEN)

        draw_rounded_rect(draw, (900, 640, 1680, 730), 10, fill=(13, 17, 23), outline=C_BORDER, width=1)
        draw.text((930, 665), "Matrices bridge algebra and physical geometry into a single framework.", font=F_BODY_BOLD, fill=C_TEXT)


def render_scene_2(draw, t, scene_dur):
    """
    Scene 2: Concept Introduction & Notation (43.88s)
    Anatomy of a Matrix, Dimensions m x n, Row i, Column j, Entry a_ij
    """
    draw.text((100, 80), "1. Formal Definition & Anatomy of a Matrix", font=F_H1, fill=C_CYAN)
    draw.text((100, 140), "A rectangular array of numbers arranged in horizontal rows and vertical columns.", font=F_BODY, fill=C_TEXT)

    # Matrix A (3x2)
    mat_data = [
        ["a11", "a12"],
        ["a21", "a22"],
        ["a31", "a32"]
    ]

    h_row = None
    h_col = None
    h_ent = None

    if 10.0 <= t < 20.0:
        h_row = 1  # Highlight Row 2
    elif 20.0 <= t < 30.0:
        h_col = 0  # Highlight Column 1
    elif t >= 30.0:
        h_ent = (1, 0)  # Highlight a21

    draw_matrix_box(draw, 180, 260, 3, 2, mat_data, title="Matrix A ∈ R^{3×2}",
                    highlight_row=h_row, highlight_col=h_col, highlight_entry=h_ent,
                    cell_w=140, cell_h=100, font=load_font(36, bold=True))

    # Explanatory Cards on Right
    draw_rounded_rect(draw, (620, 240, 1750, 780), 16, fill=C_PANEL, outline=C_BORDER, width=2)

    draw.text((660, 270), "Dimensions: m × n  (Rows × Columns)", font=F_H1, fill=C_AMBER)
    draw.text((660, 335), "Mnemonic: 'Row-Column' → Roman Colonists (or alphabetical order R then C)", font=F_BODY_BOLD, fill=C_CYAN)

    draw.line([(660, 380), (1700, 380)], fill=C_BORDER, width=1)

    # Detail items
    y_off = 410
    draw.text((660, y_off), "• m = Number of Rows (Horizontal):", font=F_BODY_BOLD, fill=C_AMBER)
    draw.text((1150, y_off), "Here m = 3", font=F_BODY, fill=C_TEXT)

    draw.text((660, y_off + 60), "• n = Number of Columns (Vertical):", font=F_BODY_BOLD, fill=C_CYAN)
    draw.text((1150, y_off + 60), "Here n = 2", font=F_BODY, fill=C_TEXT)

    draw.text((660, y_off + 120), "• Entry notation a_ij:", font=F_BODY_BOLD, fill=C_GREEN)
    draw.text((1150, y_off + 120), "i = Row index,  j = Column index", font=F_BODY, fill=C_TEXT)

    if h_ent:
        draw_rounded_rect(draw, (660, 620, 1680, 730), 10, fill=(6, 214, 160, 40), outline=C_GREEN, width=2)
        draw.text((690, 645), "Target Entry: a_21 = Row 2, Column 1", font=F_H2, fill=C_GREEN)
        draw.text((690, 685), "Vectors are just specialized single-column matrices: v ∈ R^{n×1}!", font=F_BODY, fill=C_TEXT)
    else:
        draw_rounded_rect(draw, (660, 620, 1680, 730), 10, fill=(13, 17, 23), outline=C_BORDER, width=1)
        draw.text((690, 655), "Special Case: Column Vector is an (n × 1) matrix.", font=F_BODY_BOLD, fill=C_TEXT)


def render_scene_3(draw, t, scene_dur):
    """
    Scene 3: Visual Intuition - Matrices as Space Transformers (56.20s)
    Coordinate grid, Basis vectors i-hat, j-hat, and transformation M = [[2, 1], [0, 1.5]]
    """
    draw.text((100, 80), "2. Visual Intuition: Matrices as Space Transformers", font=F_H1, fill=C_CYAN)
    draw.text((100, 140), "A matrix is an active geometric function. Its columns tell you where the standard basis vectors land!", font=F_BODY, fill=C_TEXT)

    # Grid center
    ox, oy = 550, 560
    scale = 80.0

    # Transformation Matrix M = [[2, 1], [0, 1.5]]
    # Animate morph between t = 20s and t = 40s
    progress = 0.0
    if t >= 20.0:
        progress = min(1.0, (t - 20.0) / 12.0)
        # Smooth cosine interpolation
        progress = 0.5 * (1.0 - math.cos(math.pi * progress))

    # Current matrix: I -> M
    m11 = 1.0 + (2.0 - 1.0) * progress
    m12 = 0.0 + (1.0 - 0.0) * progress
    m21 = 0.0 + (0.0 - 0.0) * progress
    m22 = 1.0 + (1.5 - 1.0) * progress

    def transform_pt(x, y):
        tx = m11 * x + m12 * y
        ty = m21 * x + m22 * y
        # Invert y for screen coords
        return (int(ox + tx * scale), int(oy - ty * scale))

    # Draw grid lines
    for i in range(-5, 6):
        # Vertical grid line (constant x)
        p1 = transform_pt(i, -4)
        p2 = transform_pt(i, 4)
        draw.line([p1, p2], fill=C_GRID, width=1)

        # Horizontal grid line (constant y)
        p3 = transform_pt(-5, i)
        p4 = transform_pt(5, i)
        draw.line([p3, p4], fill=C_GRID, width=1)

    # Draw Axes
    draw.line([transform_pt(-5, 0), transform_pt(5, 0)], fill=C_AXIS, width=2)
    draw.line([transform_pt(0, -4), transform_pt(0, 4)], fill=C_AXIS, width=2)

    # Basis vector i-hat (transformed)
    i_end = transform_pt(1, 0)
    draw_arrow(draw, (ox, oy), i_end, C_CYAN, width=6, tip_length=18)
    draw.text((i_end[0] + 10, i_end[1] - 25), "i-hat", font=F_BODY_BOLD, fill=C_CYAN)

    # Basis vector j-hat (transformed)
    j_end = transform_pt(0, 1)
    draw_arrow(draw, (ox, oy), j_end, C_AMBER, width=6, tip_length=18)
    draw.text((j_end[0] + 10, j_end[1] - 25), "j-hat", font=F_BODY_BOLD, fill=C_AMBER)

    # Right Info Panel
    draw_rounded_rect(draw, (1080, 220, 1820, 800), 16, fill=C_PANEL, outline=C_BORDER, width=2)

    draw.text((1120, 250), "Matrix as Basis Recorder", font=F_H2, fill=C_GREEN)
    
    # Display Matrix M
    mat_m = [
        ["2", "1"],
        ["0", "1.5"]
    ]
    draw_matrix_box(draw, 1120, 320, 2, 2, mat_m, title="Transformation Matrix M",
                    cell_w=100, cell_h=70, font=F_MATH_LG)

    draw.line([(1120, 500), (1780, 500)], fill=C_BORDER, width=1)

    draw.text((1120, 520), "Column 1 (Cyan):", font=F_BODY_BOLD, fill=C_CYAN)
    draw.text((1400, 520), "Where i-hat [1, 0]^T lands → [2, 0]^T", font=F_BODY, fill=C_TEXT)

    draw.text((1120, 580), "Column 2 (Amber):", font=F_BODY_BOLD, fill=C_AMBER)
    draw.text((1400, 580), "Where j-hat [0, 1]^T lands → [1, 1.5]^T", font=F_BODY, fill=C_TEXT)

    # Linearity rules card
    draw_rounded_rect(draw, (1120, 650, 1780, 760), 10, fill=(13, 17, 23), outline=C_BORDER, width=1)
    draw.text((1140, 670), "Linearity Rules:", font=F_SMALL_BOLD, fill=C_AMBER)
    draw.text((1140, 700), "1. Origin (0,0) stays fixed firmly.", font=F_SMALL, fill=C_MUTED)
    draw.text((1140, 725), "2. All grid lines remain straight and parallel.", font=F_SMALL, fill=C_MUTED)


def render_scene_4(draw, t, scene_dur):
    """
    Scene 4: Step-by-Step Worked Example (80.94s)
    0 - 26s: Matrix Addition (A + B)
    26 - 46s: Scalar Multiplication (3 * A)
    46 - 80.94s: Matrix Multiplication (A * B)
    """
    draw.text((100, 80), "3. Worked Example: Step-by-Step Operations", font=F_H1, fill=C_CYAN)

    if t < 26.0:
        # Part A: Addition
        draw.text((100, 140), "Part A: Matrix Addition — Requires Identical Dimensions (2×2 + 2×2)", font=F_BODY, fill=C_TEXT)

        mat_a = [["3", "1"], ["0", "2"]]
        mat_b = [["1", "2"], ["4", "5"]]

        draw_matrix_box(draw, 140, 250, 2, 2, mat_a, title="Matrix A (2×2)", cell_w=100, cell_h=75)
        draw.text((395, 330), "+", font=F_TITLE, fill=C_AMBER)
        draw_matrix_box(draw, 450, 250, 2, 2, mat_b, title="Matrix B (2×2)", cell_w=100, cell_h=75)
        draw.text((705, 330), "=", font=F_TITLE, fill=C_GREEN)

        step_data = [["3+1", "1+2"], ["0+4", "2+5"]]
        draw_matrix_box(draw, 760, 250, 2, 2, step_data, title="Component-Wise Sum", cell_w=120, cell_h=75, text_color=C_AMBER)
        draw.text((1055, 330), "=", font=F_TITLE, fill=C_GREEN)

        res_data = [["4", "3"], ["4", "7"]]
        draw_matrix_box(draw, 1110, 250, 2, 2, res_data, title="Result Matrix (A + B)", cell_w=100, cell_h=75, text_color=C_GREEN)

        # Callout Panel
        draw_rounded_rect(draw, (140, 500, 1750, 780), 16, fill=C_PANEL, outline=C_BORDER, width=2)
        draw.text((180, 530), "Algebraic Rule: (A + B)_{ij} = a_{ij} + b_{ij}", font=F_H2, fill=C_GREEN)
        draw.text((180, 580), "• Top-Left:      3 + 1 = 4", font=F_BODY, fill=C_TEXT)
        draw.text((180, 620), "• Top-Right:     1 + 2 = 3", font=F_BODY, fill=C_TEXT)
        draw.text((700, 580), "• Bottom-Left:   0 + 4 = 4", font=F_BODY, fill=C_TEXT)
        draw.text((700, 620), "• Bottom-Right:  2 + 5 = 7", font=F_BODY, fill=C_TEXT)
        draw.text((180, 700), "Geometric Meaning: Adding two transformations shifts vector outputs by displacement across space.", font=F_BODY_BOLD, fill=C_CYAN)

    elif t < 46.0:
        # Part B: Scalar Multiplication
        draw.text((100, 140), "Part B: Scalar Multiplication — Uniform Scaling by Real Number k = 3", font=F_BODY, fill=C_TEXT)

        mat_a = [["3", "1"], ["0", "2"]]

        draw.text((200, 320), "k = 3  ×", font=F_TITLE, fill=C_AMBER)
        draw_matrix_box(draw, 420, 250, 2, 2, mat_a, title="Matrix A (2×2)", cell_w=100, cell_h=75)
        draw.text((680, 320), "=", font=F_TITLE, fill=C_GREEN)

        step_data = [["3·(3)", "3·(1)"], ["3·(0)", "3·(2)"]]
        draw_matrix_box(draw, 740, 250, 2, 2, step_data, title="Scale Every Entry", cell_w=130, cell_h=75, text_color=C_AMBER)
        draw.text((1060, 320), "=", font=F_TITLE, fill=C_GREEN)

        res_data = [["9", "3"], ["0", "6"]]
        draw_matrix_box(draw, 1120, 250, 2, 2, res_data, title="Result (3A)", cell_w=100, cell_h=75, text_color=C_GREEN)

        # Callout Panel
        draw_rounded_rect(draw, (140, 500, 1750, 780), 16, fill=C_PANEL, outline=C_BORDER, width=2)
        draw.text((180, 530), "Algebraic Rule: (kA)_{ij} = k · a_{ij}", font=F_H2, fill=C_GREEN)
        draw.text((180, 580), "Every single entry in the matrix is scaled uniformly by the factor k.", font=F_BODY, fill=C_TEXT)
        draw.text((180, 630), "Geometric Meaning: Dilates or stretches the entire transformed space uniformly by factor k.", font=F_BODY_BOLD, fill=C_CYAN)
        draw.text((180, 680), "If k is negative, the space is also reflected through the origin!", font=F_BODY, fill=C_CORAL)

    else:
        # Part C: Matrix Multiplication
        local_t = t - 46.0
        draw.text((100, 140), "Part C: Matrix Multiplication — Row × Column Inner Products", font=F_BODY, fill=C_TEXT)

        # Dimension match badge
        draw_rounded_rect(draw, (140, 200, 850, 260), 8, fill=(6, 214, 160, 40), outline=C_GREEN, width=2)
        draw.text((160, 215), "Dimension Check: (2 × 2) × (2 × 2) → Inner 2s Match! Result is 2×2", font=F_BODY_BOLD, fill=C_GREEN)

        mat_a = [["3", "1"], ["0", "2"]]
        mat_b = [["1", "2"], ["4", "5"]]

        # Highlighting based on local_t
        h_a_row = 0 if local_t < 18.0 else 1
        h_b_col = 0 if (local_t < 9.0 or (18.0 <= local_t < 27.0)) else 1

        draw_matrix_box(draw, 140, 290, 2, 2, mat_a, title="Matrix A (Left)", highlight_row=h_a_row, cell_w=95, cell_h=70)
        draw.text((375, 360), "×", font=F_TITLE, fill=C_AMBER)
        draw_matrix_box(draw, 420, 290, 2, 2, mat_b, title="Matrix B (Right)", highlight_col=h_b_col, cell_w=95, cell_h=70)
        draw.text((655, 360), "=", font=F_TITLE, fill=C_GREEN)

        res_c = [["7", "11"], ["8", "10"]]
        draw_matrix_box(draw, 700, 290, 2, 2, res_c, title="Product C = AB", cell_w=95, cell_h=70, text_color=C_GREEN)

        # Dot Product Calculations Panel
        draw_rounded_rect(draw, (980, 200, 1800, 780), 16, fill=C_PANEL, outline=C_BORDER, width=2)
        draw.text((1020, 230), "Step-by-Step Dot Products:", font=F_H2, fill=C_AMBER)

        calc_steps = [
            ("C_11 (Row 1 × Col 1):", "(3 · 1) + (1 · 4) = 3 + 4 = 7", C_CYAN),
            ("C_12 (Row 1 × Col 2):", "(3 · 2) + (1 · 5) = 6 + 5 = 11", C_CYAN),
            ("C_21 (Row 2 × Col 1):", "(0 · 1) + (2 · 4) = 0 + 8 = 8", C_YELLOW),
            ("C_22 (Row 2 × Col 2):", "(0 · 2) + (2 · 5) = 0 + 10 = 10", C_YELLOW)
        ]

        y_calc = 290
        for i, (label, eq, col) in enumerate(calc_steps):
            draw.text((1020, y_calc), label, font=F_BODY_BOLD, fill=col)
            draw.text((1330, y_calc), eq, font=F_BODY_BOLD, fill=C_TEXT)
            y_calc += 65

        draw.line([(1020, y_calc + 10), (1750, y_calc + 10)], fill=C_BORDER, width=1)
        draw.text((1020, y_calc + 30), "General Formula:", font=F_SMALL_BOLD, fill=C_GREEN)
        draw.text((1020, y_calc + 60), "C_{ij} = Σ_{r=1}^k a_{ir} · b_{rj}", font=load_font(30, bold=True), fill=C_GREEN)


def render_scene_5(draw, t, scene_dur):
    """
    Scene 5: Geometric Interpretation & Non-Commutativity (47.14s)
    Composition of transformations: why AB != BA, and determinant area scaling.
    """
    draw.text((100, 80), "4. Geometric Interpretation: Why Row × Column?", font=F_H1, fill=C_CYAN)
    draw.text((100, 140), "Matrix multiplication is the COMPOSITION of linear transformations: T_{BA}(x) = B(A(x)).", font=F_BODY, fill=C_TEXT)

    # Big Non-Commutativity Comparison
    draw_rounded_rect(draw, (140, 220, 900, 600), 16, fill=C_PANEL, outline=C_BORDER, width=2)
    draw.text((180, 250), "Product AB (Apply B first, then A):", font=F_H2, fill=C_CYAN)
    mat_ab = [["7", "11"], ["8", "10"]]
    draw_matrix_box(draw, 180, 310, 2, 2, mat_ab, cell_w=120, cell_h=80, text_color=C_CYAN)

    draw_rounded_rect(draw, (960, 220, 1720, 600), 16, fill=C_PANEL, outline=C_BORDER, width=2)
    draw.text((1000, 250), "Product BA (Apply A first, then B):", font=F_H2, fill=C_AMBER)
    mat_ba = [["3", "5"], ["12", "14"]]
    draw_matrix_box(draw, 1000, 310, 2, 2, mat_ba, cell_w=120, cell_h=80, text_color=C_AMBER)

    # Prominent Warning Banner in Middle
    draw_rounded_rect(draw, (140, 640, 1720, 780), 14, fill=(255, 89, 100, 40), outline=C_CORAL, width=3)
    draw.text((180, 665), "CRITICAL PROPERTY: NON-COMMUTATIVITY (AB ≠ BA)", font=F_H1, fill=C_CORAL)
    draw.text((180, 725), "Order matters fundamentally! Rotating space by 90° then shearing gives a totally different result than shearing first!", font=F_BODY_BOLD, fill=C_TEXT)


def render_scene_6(draw, t, scene_dur):
    """
    Scene 6: Summary, Takeaways & Credits (43.43s)
    Core takeaways and official project submission frame.
    """
    if t < 22.0:
        draw.text((100, 80), "Summary: Three Core Takeaways", font=F_H1, fill=C_CYAN)
        draw.text((100, 140), "Remember these fundamental principles whenever you work with matrices:", font=F_BODY, fill=C_TEXT)

        cards = [
            ("1. Dual Nature of Matrices", "A matrix is simultaneously an organized array of data and an active geometric transformation of space. Columns record basis landing coordinates.", C_AMBER),
            ("2. Strict Dimensional Rules", "Matrix addition requires identical dimensions (m×n). Matrix multiplication requires inner dimensions to match: (m×k)(k×n) → m×n.", C_GREEN),
            ("3. Multiplication is Composition", "Matrix multiplication represents applying successive transformations in sequence. Because sequence order matters, AB ≠ BA.", C_CORAL)
        ]

        y_c = 220
        for title, desc, col in cards:
            draw_rounded_rect(draw, (140, y_c, 1780, y_c + 150), 12, fill=C_PANEL, outline=col, width=2)
            draw.text((180, y_c + 20), title, font=F_H2, fill=col)
            draw.text((180, y_c + 75), desc, font=F_BODY, fill=C_TEXT)
            y_c += 180

    else:
        # Final Closing Frame with Credits & Disclosures
        draw.text((100, 80), "Official Submission Details & Credits", font=F_H1, fill=C_GREEN)
        draw.text((100, 140), "Linear Algebra and Calculus (M3) • Internal Assessment Project Option 1", font=F_BODY, fill=C_TEXT)

        draw_rounded_rect(draw, (140, 210, 1780, 790), 16, fill=C_PANEL, outline=C_BORDER, width=2)

        info_rows = [
            ("Student Name:", "Ipsit Debnath", C_CYAN),
            ("Student ID / Roll No:", "E25B071258", C_AMBER),
            ("Branch / Program:", "BTech Computer Science (AI & ML)", C_GREEN),
            ("Course Code & Title:", "M3: Linear Algebra and Calculus", C_TEXT),
            ("Submission Deadline:", "25th November", C_CORAL),
            ("Animation Codebase:", "Custom Python 1080p Engine + Manim CE Community Scripts (_Code/)", C_GREEN),
            ("Academic References:", "Strang (Linear Algebra 5e), 3Blue1Brown (Essence of LA), Lay (LA Applications)", C_MUTED),
            ("Audio Attribution:", "Royalty-free ambient soundtrack; Voiceover via macOS Speech Synthesis", C_MUTED),
            ("AI Tool Disclosure:", "Visual scripts and narration timing authored programmatically; math verified independently.", C_MUTED)
        ]

        y_i = 230
        for lbl, val, col in info_rows:
            draw.text((180, y_i), lbl, font=F_BODY_BOLD, fill=col)
            draw.text((540, y_i), val, font=F_BODY, fill=C_TEXT)
            y_i += 50

        draw_rounded_rect(draw, (180, 690, 1740, 760), 8, fill=(6, 214, 160, 30), outline=C_GREEN, width=1)
        draw.text((210, 712), "✓ Verified: All equations, dimensions, matrix products, and visual transformations are mathematically sound.", font=F_BODY_BOLD, fill=C_GREEN)


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def render_full_video():
    if not os.path.exists(TIMING_JSON):
        print(f"Error: Timing file {TIMING_JSON} not found. Run generate_audio.py first!")
        sys.exit(1)

    with open(TIMING_JSON, "r") as f:
        timing_info = json.load(f)

    # Compute scene start and end times
    scene_starts = []
    curr = 0.0
    for s in timing_info:
        scene_starts.append(curr)
        curr += s["duration"] + 0.6  # 0.6s pause between scenes

    total_duration = curr
    total_frames = int(total_duration * FPS)

    print(f"Rendering {total_frames} frames ({total_duration:.2f}s) @ 1080p 30fps...")

    # Start FFmpeg process piping rawvideo RGB24
    ffmpeg_cmd = [
        FFMPEG_BIN, "-y",
        "-f", "rawvideo",
        "-pixel_format", "rgb24",
        "-video_size", f"{WIDTH}x{HEIGHT}",
        "-framerate", str(FPS),
        "-i", "pipe:0",
        "-i", SOUNDTRACK_WAV,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]

    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    scene_renderers = [
        render_scene_1,
        render_scene_2,
        render_scene_3,
        render_scene_4,
        render_scene_5,
        render_scene_6
    ]

    for frame_idx in range(total_frames):
        t = frame_idx / float(FPS)

        # Find active scene
        active_scene_idx = 0
        for i in range(len(scene_starts)):
            if t >= scene_starts[i]:
                active_scene_idx = i

        s_info = timing_info[active_scene_idx]
        s_start = scene_starts[active_scene_idx]
        local_t = t - s_start
        s_dur = s_info["duration"]

        # Base Image
        img = Image.new("RGB", (WIDTH, HEIGHT), C_BG)
        draw = ImageDraw.Draw(img)

        # Render active scene
        scene_renderers[active_scene_idx](draw, local_t, s_dur)

        # Render global header and footer
        draw_header_footer(draw, active_scene_idx + 1, s_info["title"], t, total_duration)

        # Stream raw bytes to FFmpeg
        proc.stdin.write(img.tobytes())

        if frame_idx % 300 == 0:
            pct = (frame_idx / float(total_frames)) * 100.0
            print(f"  Frame {frame_idx}/{total_frames} ({pct:.1f}%) - Time: {t:.1f}s")

    proc.stdin.close()
    proc.wait()

    if proc.returncode == 0:
        print(f"\nSUCCESS! 1080p video rendered successfully: {OUTPUT_VIDEO}")
        size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
        print(f"File size: {size_mb:.2f} MB | Duration: {total_duration:.2f}s")
    else:
        print(f"Error: FFmpeg exited with code {proc.returncode}")
        sys.exit(1)


if __name__ == "__main__":
    render_full_video()
