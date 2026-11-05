# Mathematical Visualizations with Manim

**Mohamed Kamil · Python & Manim · Linear Algebra**

A collection of mathematical visualizations and educational animations created
with Python and Manim, featuring matrix operations, linear algebra, and
procedural mathematical animation. These four standalone scenes focus on making
mathematical correspondence visible: entries travel to their destinations, row
operations preserve exact values, and a solution point follows moving planes.

Each scene runs independently. No private lecture framework, `manim-slides`,
external image assets or bundled fonts are needed.

## Featured animations

GIFs play at original elapsed speed, at 640 × 360 and 15 fps. The linked MP4s are
silent native **1920 × 1080, 60 fps** renders.

### Matrix multiplication — row × column

![Row and column selections animate into each matrix-product entry](previews/matrix_multiplication.gif)

Sliding guides select a row and a column. Their entries are copied into a
calculation panel, evaluated, then placed into the result matrix.

- **Concept:** each entry is the dot product `c_ij = Σ_k a_ik b_kj`.
- **Implementation:** addressable matrix glyphs, persistent `Transform` guides,
  `TransformFromCopy` operand correspondence, computed result values.
- [Source](src/matrix_multiplication.py) · [1080p60 video](videos/matrix_multiplication.mp4)

### Matrix transpose — rows become columns

![Individual upright entries travel from rows of A to columns of its transpose](previews/matrix_transpose.gif)

A rectangular matrix is transposed one entry at a time. The source remains
visible while each row is copied into the corresponding destination column.

- **Concept:** `a_ij → a_ji`, including a change from 2 × 3 to 3 × 2.
- **Implementation:** explicit index mapping, sliding row/column outlines and
  upright glyph motion that preserves entry order.
- [Source](src/matrix_transpose.py) · [1080p60 video](videos/matrix_transpose.mp4)

### Gauss–Jordan — extracting an inverse

![An augmented matrix is reduced through swaps and row combinations, then its inverse is extracted](previews/gauss_jordan.gif)

Three elementary operations transform `[A | I]` into `[I | A⁻¹]`. Each state is
copied before the operation; both blocks change together. The inverse is then
copied from the right block into its own matrix.

- **Concept:** inverse construction by exact elementary row operations.
- **Implementation:** immutable rational states using `fractions.Fraction`,
  curved row-swap paths, a temporary row-multiple panel and explicit block extraction.
- [Source](src/gauss_jordan.py) · [1080p60 video](videos/gauss_jordan.mp4)

### Plane intersection — the geometry of a system

![Three projected planes reveal a common point that moves with their offsets](previews/plane_intersection.gif)

Three planes appear in an orthographic view, then translate while their common
point follows the actual solution. A controlled orbit reveals the geometry
without moving the mathematical labels.

- **Concept:** the unique solution of `Ax = b` as the intersection of three planes.
- **Implementation:** model-space plane bases, `ValueTracker`, `always_redraw`,
  NumPy's linear solver and a precomputed projection fit.
- [Source](src/plane_intersection.py) · [1080p60 video](videos/plane_intersection.mp4)

## Technical stack

| Tool | Version / use |
| --- | --- |
| Python | 3.12; locally tested on 3.12.14 |
| Manim Community | 0.19.0, Cairo renderer |
| NumPy | 2.3.5, plane geometry and projection |
| Python standard library | Exact rational arithmetic, scripts and tests |
| LaTeX + dvisvgm | Mathematical typesetting; TeX Live 2023 used locally |
| FFmpeg | 6.1.1 used for preview encoding and video inspection |
| pytest / Ruff | 8.4.2 / 0.14.3, mathematical tests and code checks |

The project pins the tested Manim version rather than relying on the latest
release. `constraints.txt` records the isolated Python environment used for validation. [Implementation notes](docs/implementation_notes.md) explain the data
model, animation choices and provenance.

## Installation

Use **Python 3.12**. Run commands from the repository root.

On Ubuntu 24.04 / Debian-based Linux, install the system tools first (package
names may differ on other distributions):

```bash
sudo apt-get update
sudo apt-get install -y python3.12-venv python3-dev pkg-config libcairo2-dev libpango1.0-dev fonts-dejavu-core ffmpeg texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-science dvisvgm
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The editable install makes `manim_portfolio` importable when rendering a scene
file directly. Install development tools to run the tests and formatting checks:

```bash
python -m pip install -c constraints.txt -e '.[dev]'
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
```

Check that `ffmpeg`, `latex` and `dvisvgm` are on `PATH`. Titles use the system
DejaVu Sans font, installed by the command above; equations use LaTeX's standard
fonts. No private fonts are distributed. For other operating systems, follow
the [Manim installation documentation](https://docs.manim.community/en/stable/installation.html)
for system dependencies, then install this project's pinned Python packages.
Windows and macOS have not been tested locally.

## Rendering

The following are the actual standalone scene commands used for the final
renders. `-qh` selects 1080p; `--fps 60` explicitly sets the frame rate.

```bash
python -m manim -qh --fps 60 src/matrix_multiplication.py MatrixMultiplication
python -m manim -qh --fps 60 src/matrix_transpose.py MatrixTranspose
python -m manim -qh --fps 60 src/gauss_jordan.py GaussJordanInverse
python -m manim -qh --fps 60 src/plane_intersection.py PlaneIntersection
```

Add `-p` to open a rendered file automatically. For a fast preview:

```bash
python -m manim -ql --fps 30 src/matrix_transpose.py MatrixTranspose
```

Or render all four in sequence:

```bash
python scripts/render_all.py --quality final
python scripts/build_previews.py
```

Manim writes new renders to `media/videos/<module>/1080p60/<Scene>.mp4`.
`build_previews.py` copies only the final clips to `videos/` and regenerates the
GIFs in `previews/`. It never copies caches or partial movie files.

## Validation

All four scenes were rendered locally at native 1080p60. Mathematical tests cover
the full product, transpose mapping, intermediate augmented states, both inverse
identities, and plane geometry throughout translation. Final videos were decoded
and sampled for visual review; GIFs were decoded to check dimensions and elapsed
duration. See [the validation record](docs/validation.json) and
[repository review](docs/repository_review.md) for results and limitations.

```bash
python scripts/validate_exports.py
```

The included GitHub Actions workflow runs lint, tests and a low-resolution render
smoke test. No remote Actions result is claimed before the repository is published.

## About the creator

**Mohamed Kamil** is an Electrical & Electronics Engineer specializing in
Telecommunications, with 5+ years of Python experience and 2 years of Manim
experience. He develops mathematical and scientific educational animations and
teaches university-level mathematics and engineering subjects.

[GitHub — moham-kamil](https://github.com/moham-kamil)

## Rights

Copyright © 2026 Mohamed Kamil. All rights reserved. No open-source reuse license
has been selected. See [RIGHTS.md](RIGHTS.md). This portfolio contains selected
standalone adaptations, not the complete paid course or its framework.
