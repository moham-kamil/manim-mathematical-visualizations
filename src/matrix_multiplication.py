"""Entry-by-entry multiplication with sliding row/column correspondence."""

from manim import (
    RIGHT,
    Create,
    FadeIn,
    FadeOut,
    MathTex,
    Transform,
    TransformFromCopy,
    VGroup,
    Write,
)

from manim_portfolio.algebra import MULTIPLICAND, MULTIPLIER, multiply, scalar_tex
from manim_portfolio.visuals import (
    ACCENT,
    HIGHLIGHT,
    EntryMatrix,
    PortfolioScene,
    calculation_panel,
    formula,
    outline,
)


class MatrixMultiplication(PortfolioScene):
    """Every result entry is computed from the same operands that animate."""

    def construct(self) -> None:
        self.heading("ROW × COLUMN")
        values = multiply(MULTIPLICAND, MULTIPLIER)
        a = EntryMatrix(MULTIPLICAND, size=39)
        b = EntryMatrix(MULTIPLIER, size=39, v_gap=0.35)
        c = EntryMatrix(values, size=39, h_gap=0.32, v_gap=0.26)
        equals = formula("=", 39)
        VGroup(a, b, equals, c).arrange(RIGHT, buff=0.44).move_to([0, 0.3, 0])
        self.play(FadeIn(a), FadeIn(b), FadeIn(equals), run_time=0.65)
        self.play(Create(c.brackets), run_time=0.3)
        guides = None
        for i in range(c.nrows):
            for j in range(c.ncols):
                selection = VGroup(
                    a.row_box(i), b.col_box(j), outline(c.cell(i, j), HIGHLIGHT, 0.06)
                )
                if guides is None:
                    guides = selection
                    self.play(Create(guides), run_time=0.25)
                else:
                    self.play(Transform(guides, selection), run_time=0.25)
                tokens = []
                for k in range(a.ncols):
                    if k:
                        tokens.append("+")
                    tokens.extend(
                        [
                            f"({scalar_tex(a.values[i][k])})",
                            r"\cdot",
                            f"({scalar_tex(b.values[k][j])})",
                        ]
                    )
                tokens.extend(["=", scalar_tex(values[i][j])])
                calculation = MathTex(*tokens, font_size=27).move_to([0, -2.35, 0])
                panel = calculation_panel(calculation)
                animations = [Create(panel)]
                cursor = 0
                for k in range(a.ncols):
                    if k:
                        animations.append(FadeIn(calculation[cursor]))
                        cursor += 1
                    animations.extend(
                        [
                            TransformFromCopy(a.cell(i, k), calculation[cursor]),
                            FadeIn(calculation[cursor + 1]),
                            TransformFromCopy(b.cell(k, j), calculation[cursor + 2]),
                        ]
                    )
                    cursor += 3
                self.play(*animations, run_time=0.55)
                self.play(FadeIn(calculation[-2:]), run_time=0.22)
                self.play(
                    TransformFromCopy(calculation[-1], c.cell(i, j)), run_time=0.45
                )
                self.play(FadeOut(calculation), FadeOut(panel), run_time=0.18)
        self.play(FadeOut(guides), run_time=0.25)
        rule = formula(r"c_{ij}=\sum_k a_{ik}b_{kj}", 35, ACCENT).move_to([0, -2.45, 0])
        self.play(Write(rule), run_time=0.7)
        self.result(c)
