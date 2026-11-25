# M3 Animation Video Project: Matrices & Matrix Operations
### Linear Algebra and Calculus (M3) • Internal Assessment (10% Weightage)
**Student Name:** Ipsit Debnath  
**Student ID / Roll No:** E25B071258  
**Branch / Program:** BTech Computer Science (AI & ML)  
**Repository Name:** `M3_AnimationVideo_Matrices_E25B071258`  
**Submission Deadline:** 25th November  

[![Video Resolution](https://img.shields.io/badge/Resolution-1080p%20FHD%20(1920x1080)-00d2ff?style=for-the-badge&logo=youtube)](_Video.mp4)
[![Video Duration](https://img.shields.io/badge/Duration-5m%2014s%20(Ideal%205m)-ffb703?style=for-the-badge&logo=clock)](_Video.mp4)
[![Storyboard](https://img.shields.io/badge/Storyboard-3--Page%20PDF%20Included-06d6a0?style=for-the-badge&logo=adobeacrobatreader)](Storyboard/Storyboard.pdf)
[![Codebase](https://img.shields.io/badge/Code-Manim%20%2B%20Python%20Engine-8b949e?style=for-the-badge&logo=python)](_Code/)

---

## 1. Project Overview & Learning Objective

This project turns an abstract mathematical concept into a visual, intuitive, and rigorous educational video designed for fellow M3 undergraduate engineering students. Moving far beyond static formulas, the animation demystifies what a matrix truly represents by pairing real-world computational data with dynamic geometric transformations of space.

### One-Sentence Learning Objective:
> *"By the end of this video, the viewer will be able to interpret any matrix both as an organized multi-dimensional data structure and as a geometric linear transformation of space, and confidently calculate and visualize matrix addition, scalar multiplication, and matrix multiplication."*

---

## 2. Submission Deliverables Summary

| Deliverable | Location in Repository | Description & Specification |
| :--- | :--- | :--- |
| **Final Video** | [`_Video.mp4`](_Video.mp4) | **1080p Full HD (1920×1080), 16:9 Landscape, 30 fps, H.264 / AAC**. Duration: **5 minutes 14 seconds** (within the recommended 5 min / strictly < 7 min limit). Includes Opening Title Frame and Closing Credits Frame with AI disclosure. |
| **Animation Source Code** | [`_Code/`](_Code/) | **Complete, fully commented, runnable source code**: <br>1. `manim_matrix_operations.py`: Full Manim Community Edition (CE) scripts.<br>2. `render_video_engine.py`: Standalone Python 1080p rendering engine with frame-by-frame vector graphics.<br>3. `generate_audio.py`: Audio synthesis and background score pipeline. |
| **Storyboard Document** | [`Storyboard/Storyboard.pdf`](Storyboard/Storyboard.pdf) & [`Storyboard/Storyboard.md`](Storyboard/Storyboard.md) | Official **6-Scene Storyboard** submitted as both a publication-quality **3-Page PDF** and formatted Markdown file with visual directions, word-for-word narration scripts, and mathematical derivations. |
| **Viva & Q&A Guide** | [`Viva_Preparation.md`](Viva_Preparation.md) | In-depth question-and-answer preparation sheet covering mathematical proofs, linearity axioms, step-by-step arithmetic justifications, and code walkthroughs. |

---

## 3. The 6-Scene Storyboard Architecture

```
00:00 ── Scene 1: Hook & Motivation (Photo pixels to 3D gaming transformations)
00:40 ── Scene 2: Concept Introduction (m x n dimensions, entry a_ij, column vectors)
01:24 ── Scene 3: Visual Intuition (Matrices as Space Transformers tracking i-hat & j-hat)
02:20 ── Scene 4: Worked Example (Step-by-step Addition, Scalar Mult, Matrix Mult)
03:41 ── Scene 5: Interpretation (Composition of maps, non-commutativity AB ≠ BA)
04:28 ── Scene 6: Summary & Credits (3 Key Takeaways, credentials, references, AI disclosure)
05:14 ── End of Video
```

| Scene # | Purpose | Duration | Primary Visuals & Animations | Mathematical Formulations |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **Hook / Context** | 39.5s | Opening Title Frame; photo zooming into pixel grayscale matrix; rotating 3D wireframe coordinate cube. | $\mathbf{x}' = A\mathbf{x}$ (Master Graphics Equation); $\text{Image} \in \mathbb{R}^{m \times n}$. |
| **2** | **Concept Introduction** | 43.9s | $3 \times 2$ Matrix anatomy; amber row sweep ($m=3$), cyan column sweep ($n=2$), glowing reticle zooming into entry $a_{21}$. | $A \in \mathbb{R}^{m \times n}$, row index $i$, column index $j$. Column vector $\mathbf{v} \in \mathbb{R}^{n \times 1}$. |
| **3** | **Visual Intuition** | 56.2s | Cartesian coordinate grid; unit vectors $\hat{i}$ (cyan) and $\hat{j}$ (amber); smooth space warping to matrix $M$. | $M = \begin{bmatrix} 2 & 1 \\ 0 & 1.5 \end{bmatrix}$; Col 1 is $T(\hat{i})$, Col 2 is $T(\hat{j})$. Linearity: parallel lines & fixed origin. |
| **4** | **Worked Example** | 80.9s | Step-by-step arithmetic cards showing: 1. Addition, 2. Scalar Mult, 3. Matrix Multiplication with row-col dot products. | $(A+B)_{ij} = a_{ij} + b_{ij}$, $(kA)_{ij} = k a_{ij}$, $C_{ij} = \sum_{r=1}^k a_{ir} b_{rj}$. All calculations fully shown. |
| **5** | **Interpretation** | 47.1s | Split-screen comparing $AB$ vs $BA$; coral warning banner on non-commutativity; shear/rotation order illustration. | $T_{BA}(\mathbf{x}) = B(A(\mathbf{x}))$; $AB \neq BA$ (Order Matters); Area scaling factor $= |\det(M)|$. |
| **6** | **Summary & Credits** | 43.4s | 3 Cascading Takeaway Cards; official closing credentials frame with references, music attribution, and AI disclosure. | Synthesis of dual nature, dimension rules, and composition. |

---

## 4. Mathematical Formulations & Worked Calculations

### Part A: Matrix Addition
- **Dimensional Condition:** Both matrices must have identical dimensions ($m \times n$).
- **Component-Wise Rule:** $(A+B)_{ij} = a_{ij} + b_{ij}$.
- **Worked Calculation:**
  $$A = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}, \quad B = \begin{bmatrix} 1 & 2 \\ 4 & 5 \end{bmatrix} \implies A + B = \begin{bmatrix} 3+1 & 1+2 \\ 0+4 & 2+5 \end{bmatrix} = \begin{bmatrix} 4 & 3 \\ 4 & 7 \end{bmatrix}$$
- **Geometric Meaning:** Adds corresponding vector shifts across the coordinate space.

### Part B: Scalar Multiplication
- **Rule:** $(kA)_{ij} = k \cdot a_{ij}$ for any scalar $k \in \mathbb{R}$.
- **Worked Calculation ($k = 3$):**
  $$3A = 3 \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix} = \begin{bmatrix} 3(3) & 3(1) \\ 3(0) & 3(2) \end{bmatrix} = \begin{bmatrix} 9 & 3 \\ 0 & 6 \end{bmatrix}$$
- **Geometric Meaning:** Uniformly dilates (stretches or compresses) the transformed coordinate space by factor $k$.

### Part C: Matrix Multiplication
- **Dimensional Compatibility:** The inner dimensions must match: $(m \times \mathbf{k}) \times (\mathbf{k} \times n) \to m \times n$.
- **Inner Product Formula:** $C_{ij} = \sum_{r=1}^k a_{ir} b_{rj}$.
- **Step-by-Step Dot Products:**
  $$C_{11} = (3 \cdot 1) + (1 \cdot 4) = 3 + 4 = \mathbf{7}$$
  $$C_{12} = (3 \cdot 2) + (1 \cdot 5) = 6 + 5 = \mathbf{11}$$
  $$C_{21} = (0 \cdot 1) + (2 \cdot 4) = 0 + 8 = \mathbf{8}$$
  $$C_{22} = (0 \cdot 2) + (2 \cdot 5) = 0 + 10 = \mathbf{10}$$
  $$C = AB = \begin{bmatrix} 7 & 11 \\ 8 & 10 \end{bmatrix}$$

### Part D: Composition & Non-Commutativity
- **Function Composition:** Multiplying $BA$ means applying transformation $A$ first, then transformation $B$:
  $$T_{BA}(\mathbf{x}) = B(A(\mathbf{x})) = (BA)\mathbf{x}$$
- **Why $AB \neq BA$:**
  $$BA = \begin{bmatrix} 1 & 2 \\ 4 & 5 \end{bmatrix} \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix} = \begin{bmatrix} 3 & 5 \\ 12 & 14 \end{bmatrix} \neq \begin{bmatrix} 7 & 11 \\ 8 & 10 \end{bmatrix} = AB$$
  In physical space, performing a 90° rotation followed by a horizontal shear results in a completely different geometry than shearing first and rotating second!

---

## 5. Repository File Structure

```
M3_AnimationVideo_Matrices_E25B071258/
├── _Video.mp4                          # Final 1080p 16:9 MP4 video (5m 14s)
├── _Code/
│   ├── manim_matrix_operations.py      # Manim CE production animation script
│   ├── render_video_engine.py          # Standalone Python 1080p rendering engine
│   └── generate_audio.py               # Speech synthesis & ambient soundtrack mixer
├── Storyboard/
│   ├── Storyboard.pdf                  # Official 3-Page PDF Storyboard
│   ├── Storyboard.md                   # Complete Markdown storyboard & script
│   ├── Storyboard.html                 # Publication-styled HTML source
│   └── generate_storyboard_pdf.py      # Script that rendered the PDF
├── Viva_Preparation.md                 # 10+ Detailed Viva Q&A questions & proofs
├── assets/
│   └── audio/                          # Synchronized voiceover tracks & music
└── README.md                           # Master documentation (this file)
```

---

## 6. How to Run Code & Re-render Video

### Option 1: Standalone Python Rendering Engine (Immediate, Zero Dependencies)
The standalone renderer creates the exact 1080p MP4 video using Python and FFmpeg:
```bash
# 1. Generate audio tracks and ambient soundtrack
python3 _Code/generate_audio.py

# 2. Render all 9,441 frames at 1080p 30fps and encode to _Video.mp4
python3 _Code/render_video_engine.py

# 3. Regenerate the Storyboard PDF
python3 Storyboard/generate_storyboard_pdf.py
```

### Option 2: Manim Community Edition (CE)
To render with Manim Community Edition:
```bash
# Install Manim CE
pip install manim

# Render individual scenes or the Master scene in 1080p 30fps
manim -pql _Code/manim_matrix_operations.py Scene3_VisualIntuition
manim -pqh _Code/manim_matrix_operations.py Scene4_WorkedExample
```

---

## 7. Individual Viva / Q&A Preparation

A comprehensive, dedicated Viva preparation document is available in [`Viva_Preparation.md`](Viva_Preparation.md). It includes:
1. **Linearity Axioms:** Rigorous definitions of $T(\mathbf{u}+\mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v})$ and $T(c\mathbf{u}) = cT(\mathbf{u})$ and their visual geometry.
2. **Dimension Mismatches:** Why $(3 \times 2) \times (3 \times 2)$ cannot be multiplied.
3. **Algebraic vs Geometric Viewpoints:** How basis vectors $\hat{i}, \hat{j}$ map to matrix columns.
4. **Determinant Intuition:** Why $|\det(M)|$ equals the area scaling factor of the unit square.
5. **Code Walkthrough:** Step-by-step breakdown of how vectors and matrices are animated.

---

## 8. Academic Honesty, AI Tool Disclosure & Attribution

- **Academic Integrity:** All mathematical derivations, intermediate arithmetic, and visual progression plans were formulated and verified independently against standard university curricula.
- **Academic References:**
  1. Strang, Gilbert. *Introduction to Linear Algebra*, 5th Edition. Wellesley-Cambridge Press.
  2. Sanderson, Grant (3Blue1Brown). *Essence of Linear Algebra* series.
  3. Lay, David C., Lay, Steven R., & McDonald, Judi J. *Linear Algebra and Its Applications*, 5th Edition. Pearson.
- **Audio Attribution:**
  - Ambient harmonic background score generated programmatically via harmonic synthesis algorithms.
  - Narration audio generated using macOS Speech Synthesis (`Samantha`).
- **AI Tool Disclosure:** AI assistance was utilized to assist in writing programmatic animation render scripts, proofreading Markdown documentation, and formatting the HTML/PDF storyboard layout. All calculations and proofs were verified by the student.

---
*Submitted for Linear Algebra and Calculus (M3) • Internal Assessment Project Option 1 • 25th November*
