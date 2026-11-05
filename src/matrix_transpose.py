"""Rows become columns; each copied glyph stays upright along its path."""

from manim import (
    UP,
    Create,
    FadeIn,
    FadeOut,
    Transform,
    TransformFromCopy,
    VGroup,
    Write,
)

from manim_portfolio.algebra import TRANSPOSE_INPUT, transpose
from manim_portfolio.visuals import (
    ACCENT,
    HIGHLIGHT,
    EntryMatrix,
    PortfolioScene,
    formula,
    outline,
)


class MatrixTranspose(PortfolioScene):
    def construct(self) -> None:
        self.heading("ROWS BECOME COLUMNS")
        a = EntryMatrix(TRANSPOSE_INPUT, size=45, h_gap=0.55, v_gap=0.45)
        at = EntryMatrix(transpose(TRANSPOSE_INPUT), size=45, h_gap=0.55, v_gap=0.45)
        a.move_to([-3.05, 0.2, 0])
        at.move_to([3.05, 0.2, 0])
        names = VGroup(
            formula("A", 34, ACCENT).next_to(a, UP, buff=0.4),
            formula("A^T", 34, ACCENT).next_to(at, UP, buff=0.4),
        )
        self.play(FadeIn(a), FadeIn(names), Create(at.brackets), run_time=0.7)
        guides = None
        for i in range(a.nrows):
            target_guides = VGroup(a.row_box(i), at.col_box(i))
            if guides is None:
                guides = target_guides
                self.play(Create(guides), run_time=0.35)
            else:
                self.play(Transform(guides, target_guides), run_time=0.45)
            for j in range(a.ncols):
                pair = VGroup(
                    outline(a.cell(i, j), HIGHLIGHT, 0.05),
                    outline(at.cell(j, i), HIGHLIGHT, 0.05),
                )
                self.play(Create(pair), run_time=0.15)
                # Copy, rather than move: the source A remains a complete matrix.
                self.play(TransformFromCopy(a.cell(i, j), at.cell(j, i)), run_time=0.4)
                self.play(FadeOut(pair), run_time=0.15)
        self.play(FadeOut(guides), run_time=0.25)
        relation = formula(r"a_{ij}\longmapsto a_{ji}", 39, ACCENT).move_to(
            [0, -2.1, 0]
        )
        self.play(Write(relation), run_time=0.85)
        self.result(at)
