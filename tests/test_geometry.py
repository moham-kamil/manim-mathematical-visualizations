"""Test true model coordinates; screen-space coincidence is insufficient."""

import numpy as np
import pytest

from manim_portfolio.geometry import (
    FINAL_OFFSETS,
    NORMALS,
    intersection,
    plane_patch,
    project,
)


@pytest.mark.parametrize(
    "normal,offset",
    [([0, 0, 1], 0.45), ([0, 1, 0], 0.65), ([1, 0, 0], 0.8), ([1, 2, -3], 1.7)],
)
def test_patch_lies_on_actual_plane_and_is_rectangular(
    normal: list, offset: float
) -> None:
    center, u, v, corners = plane_patch(normal, offset)
    np.testing.assert_allclose(corners @ normal, offset, atol=1e-12)
    assert abs(u @ v) < 1e-12
    assert abs(center @ normal - offset) < 1e-12
    edges = np.roll(corners, -1, axis=0) - corners
    for i in range(4):
        assert abs(edges[i] @ edges[(i + 1) % 4]) < 1e-12


def test_common_point_throughout_continuous_translation() -> None:
    for progress in np.linspace(0, 1, 101):
        offsets = progress * FINAL_OFFSETS
        point = intersection(NORMALS, offsets)
        np.testing.assert_allclose(NORMALS @ point, offsets, atol=1e-12)
    np.testing.assert_allclose(point, [0.8, 0.65, 0.45], atol=1e-12)


def test_orthographic_projection_is_linear_and_keeps_depth_out_of_screen() -> None:
    a, b = np.array([1, 2, 3]), np.array([-1, 4, 2])
    for angle in [-35, -28, -12]:
        np.testing.assert_allclose(
            project(a + 2 * b, angle),
            project(a, angle) + 2 * project(b, angle),
            atol=1e-12,
        )
        assert project(a, angle)[2] == 0


def test_invalid_geometries_fail_explicitly() -> None:
    with pytest.raises(ValueError):
        plane_patch([0, 0, 0], 1)
    with pytest.raises(ValueError):
        intersection([[1, 0, 0]] * 3, [0, 0, 0])
