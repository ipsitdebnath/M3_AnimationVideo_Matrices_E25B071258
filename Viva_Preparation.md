# Individual Viva & Q&A Preparation Master Guide
## Linear Algebra and Calculus (M3) • Internal Assessment: Animation Video Project
**Student Name:** Ipsit Debnath  
**Student ID / Roll No:** E25B071258  
**Branch:** BTech Computer Science (AI & ML)  
**Topic:** Matrices & Matrix Operations: Geometry, Algebra & Intuition  
**Deliverable Focus:** Mathematical Derivations, Visual Choices & Animation Code Justification  

---

## Part 1: Core Mathematical Concepts & Derivations

### Q1. What is the fundamental difference between viewing a matrix as a table of numbers versus viewing it as a linear transformation?
**Answer:**
- **Algebraic / Data View:** A matrix $A \in \mathbb{R}^{m \times n}$ is a rectangular array of scalars representing discrete, multi-dimensional data—such as pixel color channels, system of linear equations coefficients, or adjacency graphs.
- **Geometric / Transformation View:** A matrix $A$ represents a mapping $T: \mathbb{R}^n \to \mathbb{R}^m$ where $\mathbf{x} \mapsto A\mathbf{x}$. 
- Under the geometric view, the matrix columns are not random numbers; they are the **coordinates of the transformed standard basis vectors**. In 2D:
  $$A = \begin{bmatrix} | & | \\ T(\hat{i}) & T(\hat{j}) \\ | & | \end{bmatrix}$$
  Because $T$ is linear, any vector $\mathbf{v} = x\hat{i} + y\hat{j}$ maps to:
  $$T(\mathbf{v}) = x T(\hat{i}) + y T(\hat{j})$$
  Therefore, tracking where $\hat{i}$ and $\hat{j}$ land completely defines the transformation for all points in the plane!

---

### Q2. What are the two rigorous mathematical axioms of a "Linear Transformation"? How are they visually manifested in the video?
**Answer:**
A transformation $T: V \to W$ is linear if and only if it satisfies two axioms for all $\mathbf{u}, \mathbf{v} \in V$ and scalar $c \in \mathbb{R}$:
1. **Additivity:** $T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v})$
2. **Homogeneity (Scalar Multiplication):** $T(c\mathbf{u}) = c T(\mathbf{u})$

**Visual Manifestation in the Animation:**
- In Scene 3, linearity is demonstrated geometrically by the fact that:
  1. **The origin remains fixed at $(0, 0)$:** $T(\mathbf{0}) = T(0 \cdot \mathbf{v}) = 0 \cdot T(\mathbf{v}) = \mathbf{0}$.
  2. **Grid lines remain straight and parallel:** If grid lines curved or bent, additivity would be violated.
  3. **Grid lines remain evenly spaced:** Proves that scalar multiples scale distances uniformly along any line.

---

### Q3. Explain the strict dimensional compatibility rules for matrix addition and matrix multiplication.
**Answer:**
- **Matrix Addition ($A + B$):**
  - **Rule:** $A$ and $B$ must have the exact same dimensions $m \times n$.
  - **Formula:** $(A + B)_{ij} = a_{ij} + b_{ij}$ for all $1 \le i \le m$ and $1 \le j \le n$.
  - **Reason:** Addition is defined component-wise. If dimensions differ, there are unmatched elements, rendering the operation undefined.
- **Matrix Multiplication ($AB$):**
  - **Rule:** If $A$ is $m \times k$, $B$ MUST be $k \times n$. The inner dimensions must match!
  - **Resulting Dimension:** The product $C = AB$ is $m \times n$.
  - **Formula:** 
    $$C_{ij} = \sum_{r=1}^k a_{ir} b_{rj} = a_{i1}b_{1j} + a_{i2}b_{2j} + \dots + a_{ik}b_{kj}$$
  - **Reason:** Multiplying $AB$ evaluates transformation $A$ on the columns of $B$. The output space of $B$ ($\mathbb{R}^k$) must match the input domain of $A$ ($\mathbb{R}^k$).

---

### Q4. Walk through the exact numerical calculations used in Scene 4 of your video.
**Answer:**
Let matrices $A$ and $B$ be:
$$A = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}, \quad B = \begin{bmatrix} 1 & 2 \\ 4 & 5 \end{bmatrix}$$

1. **Matrix Addition:**
   $$A + B = \begin{bmatrix} 3+1 & 1+2 \\ 0+4 & 2+5 \end{bmatrix} = \begin{bmatrix} 4 & 3 \\ 4 & 7 \end{bmatrix}$$
2. **Scalar Multiplication ($k = 3$):**
   $$3A = 3 \cdot \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix} = \begin{bmatrix} 3(3) & 3(1) \\ 3(0) & 3(2) \end{bmatrix} = \begin{bmatrix} 9 & 3 \\ 0 & 6 \end{bmatrix}$$
3. **Matrix Multiplication ($C = AB$):**
   - $C_{11} = (\text{Row } 1 \text{ of } A) \cdot (\text{Col } 1 \text{ of } B) = (3)(1) + (1)(4) = 3 + 4 = 7$
   - $C_{12} = (\text{Row } 1 \text{ of } A) \cdot (\text{Col } 2 \text{ of } B) = (3)(2) + (1)(5) = 6 + 5 = 11$
   - $C_{21} = (\text{Row } 2 \text{ of } A) \cdot (\text{Col } 1 \text{ of } B) = (0)(1) + (2)(4) = 0 + 8 = 8$
   - $C_{22} = (\text{Row } 2 \text{ of } A) \cdot (\text{Col } 2 \text{ of } B) = (0)(2) + (2)(5) = 0 + 10 = 10$
   $$C = AB = \begin{bmatrix} 7 & 11 \\ 8 & 10 \end{bmatrix}$$

---

### Q5. Why is matrix multiplication not commutative ($AB \neq BA$)? Give both an algebraic and a geometric justification.
**Answer:**
- **Algebraic Proof:**
  Using the matrices above:
  $$BA = \begin{bmatrix} 1 & 2 \\ 4 & 5 \end{bmatrix} \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}$$
  - $(BA)_{11} = (1)(3) + (2)(0) = 3 \neq 7 = (AB)_{11}$
  - $(BA)_{12} = (1)(1) + (2)(2) = 1 + 4 = 5 \neq 11 = (AB)_{12}$
  - $(BA)_{21} = (4)(3) + (5)(0) = 12 \neq 8 = (AB)_{21}$
  - $(BA)_{22} = (4)(1) + (5)(2) = 4 + 10 = 14 \neq 10 = (AB)_{22}$
  $$BA = \begin{bmatrix} 3 & 5 \\ 12 & 14 \end{bmatrix} \neq \begin{bmatrix} 7 & 11 \\ 8 & 10 \end{bmatrix} = AB$$
- **Geometric Meaning:**
  Matrix multiplication represents the **composition of functions**: $(AB)(\mathbf{x}) = A(B(\mathbf{x}))$, meaning transformation $B$ is applied first, followed by transformation $A$.
  In physical space, sequential operations depend on order. For example, rotating a book 90° about the z-axis and then 90° about the x-axis yields a completely different orientation than performing those operations in reverse order.

---

### Q6. What does the determinant of a $2 \times 2$ matrix represent geometrically?
**Answer:**
- For matrix $M = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$, the determinant is $\det(M) = ad - bc$.
- **Geometric Meaning:** $|\det(M)|$ represents the **factor by which areas scale** under the transformation.
- The unit square bounded by $\hat{i} = [1,0]^T$ and $\hat{j} = [0,1]^T$ has an initial area of $1$. After transformation, the unit square becomes a parallelogram spanned by $[a, c]^T$ and $[b, d]^T$, whose area is exactly $|ad - bc|$.
- **Sign of Determinant:** If $\det(M) < 0$, the orientation of space has been reversed (like flipping a pancake or viewing space in a mirror). If $\det(M) = 0$, space has collapsed into a line or single point, meaning the transformation is non-invertible (singular).

---

## Part 2: Visual Choices & Animation Design Decisions

### Q7. Why did you choose a 3Blue1Brown-inspired color scheme with cyan and yellow basis vectors?
**Answer:**
- **Cognitive Clarity:** In cognitive science, color persistence aids retention. Cyan (`#00d2ff`) was assigned strictly to the x-axis, basis vector $\hat{i}$, matrix Column 1, and horizontal dimensions. Golden Amber (`#ffb703`) was assigned strictly to the y-axis, basis vector $\hat{j}$, matrix Column 2, and vertical dimensions.
- **Visual Mapping:** When the matrix $\begin{bmatrix} 2 & 1 \\ 0 & 1.5 \end{bmatrix}$ is presented, highlighting the first column in cyan directly mirrors the cyan $\hat{i}$ vector landing at $(2, 0)$, enabling viewers to immediately connect algebra to geometry without mental friction.
- **Accessibility & Contrast:** The dark slate canvas (`#0d1117`) provides a contrast ratio exceeding 12:1 against bright white text (`#f0f6fc`), avoiding eye fatigue across a 5-minute technical presentation.

---

### Q8. Why did you structure the video with a Hook, Geometric Intuition, and Worked Example before concluding?
**Answer:**
- Standard textbook presentations often start with dry, mechanical row-column multiplication rules, which causes cognitive disconnection.
- By starting with **Scene 1 (Hook)**, we establish real-world utility (computer graphics, gaming, machine learning).
- By providing **Scene 3 (Visual Intuition)** before algebraic manipulations, students understand *what* the operations do to space before worrying about *how* to calculate them.
- Finally, **Scene 4 (Worked Example)** and **Scene 5 (Interpretation)** ground the intuition in verifiable, rigorous mathematics.

---

## Part 3: Code Architecture & Implementation Details

### Q9. Explain how your animation scripts render the video.
**Answer:**
- We developed two complementary code implementations in `_Code/`:
  1. `manim_matrix_operations.py`: Built using the standard Manim Community Edition (CE) library, structuring scenes with `Scene`, `LinearTransformationScene`, `Matrix`, `Arrow`, and `Transform`.
  2. `render_video_engine.py`: A self-contained, high-performance Python animation rendering engine that programmatically draws mathematical formulas, vector coordinate planes, smooth easing interpolations, and matrices directly onto 1080p frames, and encodes them with FFmpeg.
- **Audio Synchronization:** The scripts synchronize visual element reveals with precise word timestamps generated from the narration transcript, ensuring formulas highlight exactly when spoken.

---

### Q10. If an evaluator asks: "Can you change the example to a 3x3 matrix right now?", how would you do it?
**Answer:**
- **Algebraically:**
  For $A \in \mathbb{R}^{3 \times 3}$ and $B \in \mathbb{R}^{3 \times 3}$, addition remains component-wise: $(A+B)_{ij} = a_{ij} + b_{ij}$ across 9 entries.
  Multiplication $C = AB$ computes 9 dot products, where each $C_{ij} = \sum_{r=1}^3 a_{ir} b_{rj} = a_{i1}b_{1j} + a_{i2}b_{2j} + a_{i3}b_{3j}$.
- **Geometrically:**
  In 3D, space is spanned by three basis vectors: $\hat{i} = [1,0,0]^T$, $\hat{j} = [0,1,0]^T$, and $\hat{k} = [0,0,1]^T$. The three columns of a $3 \times 3$ matrix represent where these three unit vectors land in 3D space, and the determinant represents the **volume scaling factor** of the unit cube!
- **In Code:**
  In the Manim script, we would extend the coordinate frame to 3D with `ThreeDScene`, define basis vectors $\hat{i}, \hat{j}, \hat{k}$, and pass $3 \times 3$ arrays to `Matrix([[a11, a12, a13], ...])`.

---

## Pre-Viva Checklist & Rehearsal Points
- [x] Defined all dimensions ($m \times n$) before operations.
- [x] Recalculated all worked example products on paper.
- [x] Memorized the linear transformation axioms: $T(u+v) = T(u)+T(v)$ and $T(cu) = cT(u)$.
- [x] Understood why column vectors are $n \times 1$ matrices.
- [x] Mastered the explanation of non-commutativity through function composition.
- [x] Ready to walk through `manim_matrix_operations.py` and `render_video_engine.py` line-by-line.
