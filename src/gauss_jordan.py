"""An exact [A | I] -> [I | A^-1] sequence, including row arithmetic."""

from manim import (
    LEFT,
    PI,
    UP,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    Transform,
    TransformFromCopy,
    VGroup,
)

from manim_portfolio.algebra import INVERSE_OPERATIONS, RowOperation, inverse_states
from manim_portfolio.visuals import (
    ACCENT,
    WARM,
    EntryMatrix,
    PortfolioScene,
    calculation_panel,
    formula,
    outline,
)


class GaussJordanInverse(PortfolioScene):
    def operate(
        self, source: EntryMatrix, final: EntryMatrix, operation: RowOperation
    ) -> None:
        """Copy the whole augmented matrix before modifying both row blocks."""
        arrow = Arrow(
            [-0.82, 0.15, 0], [0.82, 0.15, 0], buff=0, stroke_width=1.5, tip_length=0.13
        )
        caption = formula(operation.tex, 25, WARM).next_to(arrow, UP, buff=0.15)
        work = source.copy().move_to(final)
        self.play(Create(arrow), FadeIn(caption), run_time=0.3)
        self.play(TransformFromCopy(source, work), run_time=0.8)
        rows = (operation.target, operation.donor)
        source_guides = VGroup(source.row_box(rows[0]), source.row_box(rows[1], ACCENT))
        work_guides = VGroup(work.row_box(rows[0]), work.row_box(rows[1], ACCENT))
        self.play(Create(source_guides), Create(work_guides), run_time=0.4)
        if operation.kind == "swap":
            animations = []
            for i in range(work.nrows):
                destination = (
                    operation.donor
                    if i == operation.target
                    else operation.target
                    if i == operation.donor
                    else i
                )
                for j in range(work.ncols):
                    animations.append(
                        Transform(
                            work.cell(i, j), final.cell(destination, j), path_arc=PI / 3
                        )
                    )
            swapped = VGroup(final.row_box(rows[1]), final.row_box(rows[0], ACCENT))
            self.play(
                *animations,
                Transform(work.brackets, final.brackets),
                Transform(work.divider, final.divider),
                Transform(work_guides, swapped),
                run_time=1.05,
            )
        else:
            factor = abs(operation.factor)
            donor = work.row(operation.donor)
            moving = donor.copy().set_color(ACCENT)
            panel = label = None
            if factor != 1:
                # The multiple is a temporary vector, not a scaled donor row in A.
                ghost = EntryMatrix(
                    (source.values[operation.donor],), size=29, h_gap=0.32
                )
                ghost.move_to([0.4, -2.45, 0])
                ghost.remove(ghost.brackets)
                label = formula(rf"R_{{{operation.donor + 1}}}", 25, ACCENT)
                label.next_to(ghost, LEFT, buff=0.35)
                panel = calculation_panel(VGroup(label, ghost), min_width=5.2)
                self.play(
                    Create(panel),
                    TransformFromCopy(donor, ghost.entries),
                    FadeIn(label),
                    run_time=0.65,
                )
                scaled = EntryMatrix(
                    (tuple(factor * x for x in source.values[operation.donor]),),
                    size=29,
                    h_gap=0.32,
                )
                scaled.entries.move_to(ghost.entries)
                scaled_label = formula(
                    rf"{factor}R_{{{operation.donor + 1}}}", 25, ACCENT
                ).move_to(label)
                self.play(
                    Transform(ghost.entries, scaled.entries),
                    Transform(label, scaled_label),
                    run_time=0.65,
                )
                moving = ghost.entries.copy()
                self.add(moving)
            else:
                self.add(moving)
            self.play(
                *[
                    moving[j]
                    .animate.move_to(final.cell(operation.target, j))
                    .set_opacity(0)
                    for j in range(work.ncols)
                ],
                *[
                    Transform(work.cell(i, j), final.cell(i, j))
                    for i in range(work.nrows)
                    for j in range(work.ncols)
                ],
                Transform(work.brackets, final.brackets),
                Transform(work.divider, final.divider),
                Transform(
                    work_guides,
                    VGroup(final.row_box(rows[0]), final.row_box(rows[1], ACCENT)),
                ),
                run_time=0.95,
            )
            self.remove(moving)
            if panel is not None:
                self.play(
                    FadeOut(ghost.entries), FadeOut(label), FadeOut(panel), run_time=0.3
                )
        # Replace the working copy after a swap: row objects have changed positions.
        self.remove(work)
        self.add(final)
        self.play(FadeOut(source_guides), FadeOut(work_guides), run_time=0.25)
        self.play(FadeOut(source), FadeOut(arrow), FadeOut(caption), run_time=0.3)

    def construct(self) -> None:
        self.heading("GAUSS–JORDAN / MATRIX INVERSE")
        states = inverse_states()
        source = EntryMatrix(states[0], size=33, h_gap=0.32, v_gap=0.33, split=3)
        source.move_to([-3.45, 0.15, 0])
        self.play(FadeIn(source), run_time=0.65)
        for operation, values in zip(INVERSE_OPERATIONS, states[1:], strict=True):
            final = EntryMatrix(values, size=33, h_gap=0.32, v_gap=0.33, split=3)
            final.move_to([3.4, 0.15, 0])
            self.operate(source, final, operation)
            self.play(final.animate.move_to([-3.45, 0.15, 0]), run_time=0.6)
            source = final
        self.play(source.animate.move_to([-2.6, 0.15, 0]), run_time=0.6)
        self.play(
            Create(outline(source.block(0, 3), ACCENT, 0.13)),
            Create(outline(source.block(3, 6), WARM, 0.13)),
            run_time=0.55,
        )
        inverse = EntryMatrix(
            tuple(row[3:] for row in states[-1]), size=40, h_gap=0.32, v_gap=0.33
        )
        inverse.move_to([3.5, 0.15, 0])
        label = formula("A^{-1}=", 33).next_to(inverse, LEFT, buff=0.2)
        self.play(Create(inverse.brackets), FadeIn(label), run_time=0.35)
        for i in range(3):
            self.play(
                *[
                    TransformFromCopy(source.cell(i, j + 3), inverse.cell(i, j))
                    for j in range(3)
                ],
                run_time=0.4,
            )
        self.result(VGroup(label, inverse))
