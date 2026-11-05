"""The geometry of Ax=b, using the original course's orthographic plane model."""

import numpy as np
from manim import (
    RIGHT,
    UP,
    WHITE,
    Arrow,
    Dot,
    FadeIn,
    Line,
    Polygon,
    ValueTracker,
    VGroup,
    Write,
    always_redraw,
)

from manim_portfolio.geometry import (
    FINAL_OFFSETS,
    NORMALS,
    intersection,
    plane_patch,
    project,
)
from manim_portfolio.visuals import ACCENT, GREEN, MUTED, WARM, PortfolioScene, formula


class PlaneIntersection(PortfolioScene):
    """One computed intersection point follows the moving planes and camera."""

    def construct(self) -> None:
        self.heading("THE GEOMETRY OF A SYSTEM")
        azimuth = ValueTracker(-35)
        offset_progress = ValueTracker(0)
        reveals = [ValueTracker(0) for _ in range(3)]
        point_opacity = ValueTracker(0)
        axis_names = [formula(name, 23, MUTED) for name in ("x", "y", "z")]
        point_name = formula("(x,y,z)", 27)
        scale, anchor = self.fit_projection()

        def screen(point: np.ndarray) -> np.ndarray:
            return anchor + scale * project(point, azimuth.get_value())

        def diagram() -> VGroup:
            body = VGroup()
            for i in range(3):
                start, end = np.zeros(3), np.zeros(3)
                start[i] = -0.85 if i == 2 else -2.15
                end[i] = 2.3 if i == 2 else 3.0
                body.add(
                    Arrow(
                        screen(start),
                        screen(end),
                        buff=0,
                        color=MUTED,
                        stroke_width=1.15,
                        max_tip_length_to_length_ratio=0.035,
                    )
                )
                body.add(axis_names[i].copy().move_to(screen(end) + [0.12, 0.1, 0]))
            offsets = offset_progress.get_value() * FINAL_OFFSETS
            for i, color in enumerate((ACCENT, WARM, GREEN)):
                opacity = reveals[i].get_value()
                center, u, v, corners = plane_patch(NORMALS[i], offsets[i])
                face = Polygon(
                    *[screen(p) for p in corners],
                    fill_color=color,
                    fill_opacity=0.16 * opacity,
                    stroke_color=color,
                    stroke_width=1.8,
                    stroke_opacity=0.95 * opacity,
                )
                body.add(face)
                for k in np.linspace(-2, 2, 7)[1:-1]:
                    for a, b in [
                        (center + k * u - 2 * v, center + k * u + 2 * v),
                        (center + k * v - 2 * u, center + k * v + 2 * u),
                    ]:
                        body.add(
                            Line(
                                screen(a),
                                screen(b),
                                color=color,
                                stroke_width=0.55,
                                stroke_opacity=0.22 * opacity,
                            )
                        )
            p = screen(intersection(NORMALS, offsets))
            label = point_name.copy().move_to(p + [1.55, -0.85, 0])
            leader = Line(
                p + [0.1, -0.06, 0],
                label.get_left() - RIGHT * 0.08,
                color=WHITE,
                stroke_width=1,
            )
            annotation = VGroup(Dot(p, radius=0.08, color=WHITE), leader, label)
            annotation.set_opacity(point_opacity.get_value()).set_z_index(12)
            return body.add(annotation)

        view = always_redraw(diagram)
        self.add(view)
        law = formula("Ax=b", 42, ACCENT).move_to([0, -3.05, 0])
        self.play(Write(law), run_time=0.75)
        for reveal in reveals:
            self.play(reveal.animate.set_value(1), run_time=0.75)
        self.play(point_opacity.animate.set_value(1), run_time=0.45)
        self.play(azimuth.animate.set_value(-12), run_time=2.7)
        self.play(offset_progress.animate.set_value(1), run_time=2.7)
        result = formula(r"p=(0.8,\,0.65,\,0.45)", 34).next_to(law, UP, buff=0.24)
        self.play(FadeIn(result), run_time=0.8)
        self.play(azimuth.animate.set_value(-28), run_time=2.5)
        view.clear_updaters()
        self.wait(0.9)

    @staticmethod
    def fit_projection() -> tuple[float, np.ndarray]:
        """Fit all camera poses and both endpoint offsets before animation starts."""
        points = []
        for offsets in (np.zeros(3), FINAL_OFFSETS):
            for normal, offset in zip(NORMALS, offsets, strict=True):
                points.extend(plane_patch(normal, offset)[3])
        for i in range(3):
            for value in (-0.85 if i == 2 else -2.15, 2.3 if i == 2 else 3.0):
                p = np.zeros(3)
                p[i] = value
                points.append(p)
        samples = np.array(
            [project(p, angle) for angle in np.linspace(-35, -7, 29) for p in points]
        )
        low, high = samples.min(axis=0), samples.max(axis=0)
        scale = min(
            (11.0 - 0.45) / (high[0] - low[0]), (4.85 - 0.45) / (high[1] - low[1])
        )
        anchor = np.array([0.0, 0.175, 0.0]) - scale * (low + high) / 2
        return scale, anchor
