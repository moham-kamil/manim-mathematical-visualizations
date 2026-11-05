"""Only the shared visual primitives needed by the four standalone scenes."""

from typing import Sequence

import numpy as np
from manim import (
    DOWN,
    LEFT,
    UL,
    UP,
    WHITE,
    Create,
    FadeIn,
    Line,
    MathTex,
    Mobject,
    RoundedRectangle,
    Scene,
    SurroundingRectangle,
    Text,
    VGroup,
    VMobject,
)

from manim_portfolio.algebra import Scalar, exact_matrix, scalar_tex

BACKGROUND = "#0B0D10"
ACCENT = "#58C4DD"
WARM = "#F0B47A"
HIGHLIGHT = "#E9CE79"
GREEN = "#9DD7AE"
MUTED = "#9FA6B2"


def formula(tex: str, size: float = 36, color: str = WHITE) -> MathTex:
    return MathTex(tex, font_size=size, color=color)


def outline(
    mobject: Mobject, color: str = ACCENT, buff: float = 0.10
) -> SurroundingRectangle:
    return SurroundingRectangle(mobject, buff=buff, color=color, stroke_width=1.6)


def calculation_panel(contents: Mobject, min_width: float = 7.3) -> RoundedRectangle:
    return (
        RoundedRectangle(
            width=max(min_width, contents.width + 0.65),
            height=max(0.62, contents.height + 0.40),
            corner_radius=0.12,
            stroke_color=ACCENT,
            stroke_width=1.1,
            stroke_opacity=0.55,
            fill_color=ACCENT,
            fill_opacity=0.045,
        )
        .move_to(contents)
        .set_z_index(-1)
    )


class EntryMatrix(VGroup):
    """Addressable entries and hand-built brackets, with a fixed augmented lane.

    Positions depend on measured column widths, rather than TeX glyph indices.
    Values remain exact and separate from animated glyphs.
    """

    def __init__(
        self,
        values: Sequence[Sequence[Scalar]],
        size: float = 40,
        h_gap: float = 0.40,
        v_gap: float = 0.36,
        split: int | None = None,
    ) -> None:
        super().__init__()
        self.values = exact_matrix(values)
        self.nrows, self.ncols = len(self.values), len(self.values[0])
        if split is not None and not 0 < split < self.ncols:
            raise ValueError("An augmented divider must lie between columns.")
        self.cells = [
            [formula(scalar_tex(value), size) for value in row] for row in self.values
        ]
        widths = [max(row[j].width for row in self.cells) for j in range(self.ncols)]
        heights = [max(cell.height for cell in row) for row in self.cells]
        xs = [0.0]
        for j in range(1, self.ncols):
            xs.append(xs[-1] + widths[j - 1] + h_gap + (0.24 if j == split else 0))
        ys = -np.cumsum([0.0] + [height + v_gap for height in heights[:-1]])
        self.entries = VGroup()
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                cell.move_to([xs[j] + widths[j] / 2, ys[i] - heights[i] / 2, 0])
                self.entries.add(cell)
        self.entries.move_to([0, 0, 0])
        left, right = (
            self.entries.get_left()[0] - 0.19,
            self.entries.get_right()[0] + 0.19,
        )
        bottom, top = (
            self.entries.get_bottom()[1] - 0.17,
            self.entries.get_top()[1] + 0.17,
        )
        self.brackets = VGroup()
        for x, direction in [(left, 1), (right, -1)]:
            bracket = VMobject(color=WHITE, stroke_width=2.1)
            bracket.set_points_as_corners(
                [
                    [x + direction * 0.13, top, 0],
                    [x, top, 0],
                    [x, bottom, 0],
                    [x + direction * 0.13, bottom, 0],
                ]
            )
            self.brackets.add(bracket)
        self.add(self.entries, self.brackets)
        self.divider = VGroup()
        if split is not None:
            x = (self.col(split - 1).get_right()[0] + self.col(split).get_left()[0]) / 2
            self.divider.add(
                Line([x, bottom, 0], [x, top, 0], color=WHITE, stroke_width=1.8)
            )
            self.add(self.divider)

    def cell(self, row: int, column: int) -> MathTex:
        return self.cells[row][column]

    def row(self, index: int) -> VGroup:
        return VGroup(*self.cells[index])

    def col(self, index: int) -> VGroup:
        return VGroup(*[row[index] for row in self.cells])

    def block(self, first_column: int, last_column: int) -> VGroup:
        return VGroup(
            *[
                self.cell(i, j)
                for i in range(self.nrows)
                for j in range(first_column, last_column)
            ]
        )

    def row_box(self, index: int, color: str = WARM) -> SurroundingRectangle:
        # Equal row-guide widths keep the selection rectangle from pulsing.
        guide = outline(self.row(index), color, 0.10)
        guide.stretch_to_fit_width(self.entries.width + 0.18)
        guide.set_x(self.entries.get_x())
        return guide

    def col_box(self, index: int, color: str = ACCENT) -> SurroundingRectangle:
        guide = outline(self.col(index), color, 0.10)
        guide.stretch_to_fit_height(self.entries.height + 0.18)
        guide.set_y(self.entries.get_y())
        return guide


class PortfolioScene(Scene):
    """A plain Manim scene: no slide controls, assets, signature or lecture state."""

    def setup(self) -> None:
        self.camera.background_color = BACKGROUND

    def heading(self, title: str) -> None:
        label = Text(title, font="DejaVu Sans", font_size=21, color=MUTED)
        label.to_corner(UL, buff=0.55).set_y(3.35)
        mark = Line(
            label.get_left() + LEFT * 0.17 + DOWN * 0.12,
            label.get_left() + LEFT * 0.17 + UP * 0.12,
            color=ACCENT,
            stroke_width=3,
        )
        self.play(FadeIn(label, shift=UP * 0.08), Create(mark), run_time=0.45)

    def result(self, mobject: Mobject) -> None:
        self.play(Create(outline(mobject)), run_time=0.4)
        self.wait(0.9)
