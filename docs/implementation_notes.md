# Implementation notes

## Scope and provenance

These are independent English-language adaptations of four animations from
Mohamed Kamil's GS203 linear-algebra project. The original project is preserved.
No course framework, source sheets, slides controls, timers, paid lecture text,
private fonts, signatures or lesson videos are part of this repository.

| Standalone scene | Original animation | Preserved behavior |
| --- | --- | --- |
| `MatrixMultiplication` | Chapter 1 matrix product example; `product_grid` | Row/column guides slide; operands are copied into a calculation panel; each result lands in its cell. |
| `MatrixTranspose` | Chapter 1 transpose example; `transpose_entries` | A row becomes a column through copies of individual upright entries. |
| `GaussJordanInverse` | Chapter 4 inverse application | All three original row operations on the full augmented matrix, followed by inverse extraction. |
| `PlaneIntersection` | Chapter 3 geometric systems; coordinate-plane diagram | Three finite plane windows, a computed common point, translation and an orthographic orbit. |

Only the necessary layout and selection ideas were extracted and rewritten as
small helpers. The standalone scenes import Manim, NumPy and `manim_portfolio`,
not the original course. All data required for the examples is in source code.

## Mathematical state versus rendered state

`algebra.py` contains immutable `Fraction` matrices, shape checks, products and
row operations. Scene values are computed from these objects; displayed answers
are not independently hard-coded. `EntryMatrix` owns individually addressable
glyphs, but animated geometry never serves as the source of numeric truth.

This separation matters during a row swap: glyph objects trade screen positions.
After the motion finishes, the temporary working copy is replaced by the exact
next state so that subsequent row indexing remains correct.

## Animation decisions

- **Multiplication:** `TransformFromCopy` keeps both operands intact. Every
  result uses an actual dot product. A persistent `Transform` moves the guides;
  the arithmetic panel is cleared between entries.
- **Transpose:** the source matrix stays visible. The destination cell is `(j,i)`
  for source `(i,j)`; glyphs translate without rotating their outlines.
- **Gauss–Jordan:** the current state is copied before modification. Both halves
  of `[A | I]` are operated on. Swaps follow arcs, a non-unit row multiple appears
  in a temporary panel, and the donor remains unchanged. Operation captions occupy
  a reserved central lane, separate from matrix entries.
- **Planes:** `ValueTracker` drives angle, reveal opacity and translation;
  `always_redraw` rebuilds the projected geometry from model coordinates. Only
  geometry orbits; the title and `Ax=b` stay fixed. The point is computed using
  `numpy.linalg.solve`, rather than inferred from projected crossings.

Other animation classes are deliberately not added just to demonstrate API
coverage. The simplest transformation that preserves correspondence is used.

## Geometry and projection

Each displayed plane is an orthogonal rectangular window on `n · p = d`.
Finite boundaries are drawing windows, not mathematical boundaries. Two
orthogonal in-plane basis vectors determine the patch; world-axis stretching
would distort a tilted plane, so the window scale is applied in that basis.

The projected axes have no perspective foreshortening. All sampled orbit poses
and both translation endpoints are fitted before rendering. The final system
has `z = 0.45`, `y = 0.65`, `x = 0.8`, hence the common point `(0.8, 0.65, 0.45)`.

## Timing, renders and previews

The native final videos use the Cairo renderer, 1920 x 1080, 60 fps, and no audio.
GIFs run at the same elapsed speed at 640 x 360 and 15 fps; they are previews,
not the quality reference for motion. Read `validation.json` for actual video
durations and checks. `scripts/build_previews.py` reproduces the included GIFs.

## Tests and practical limits

Unit tests verify hand-computed intermediate rows, both inverse identities,
all six product entries, transpose involution, exact fractional operations,
shape/index failures, plane incidence, orthogonality and the common point across
101 translation samples. Formatting and lint checks use Ruff.

All four scenes were rendered locally. Final-frame decoding, metadata checks and
sampled visual review are recorded in `validation.json` and `repository_review.md`.
The GitHub Actions workflow is provided for future runs; it has not been executed
on a remote GitHub repository. Windows and macOS have not been tested locally.
