"""Model-space plane construction and orthographic projection (no Manim)."""

import numpy as np
from numpy.typing import ArrayLike, NDArray

NORMALS = np.array([[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]])
FINAL_OFFSETS = np.array([0.45, 0.65, 0.8])


def plane_patch(normal: ArrayLike, offset: float, bound: float = 2.0) -> tuple:
    """Return an orthogonal finite window on n.p = offset, plus its basis."""
    normal = np.asarray(normal, dtype=float)
    length = np.linalg.norm(normal)
    if normal.shape != (3,) or length == 0 or bound <= 0:
        raise ValueError("Use a nonzero 3-vector and a positive patch bound.")
    unit = normal / length
    trial = np.array([0.0, 0.0, 1.0] if abs(unit[2]) < 0.95 else [0.0, 1.0, 0.0])
    u = np.cross(unit, trial)
    u /= np.linalg.norm(u)
    v = np.cross(unit, u)
    center = normal * offset / (normal @ normal)
    # Original rectangular-window proportions, scaled in the plane's own basis.
    window_scale = np.array([1.35, 1.35, 0.75])
    u *= np.linalg.norm(u * window_scale)
    v *= np.linalg.norm(v * window_scale)
    corners = np.array(
        [
            center + bound * (a * u + b * v)
            for a, b in [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        ]
    )
    return center, u, v, corners


def project(
    point: ArrayLike, azimuth: float, elevation: float = 24.0
) -> NDArray[np.float64]:
    a, e = np.deg2rad([azimuth, elevation])
    right = np.array([np.cos(a), np.sin(a), 0.0])
    up = np.array([-np.sin(a) * np.sin(e), np.cos(a) * np.sin(e), np.cos(e)])
    p = np.asarray(point, dtype=float)
    return np.array([p @ right, p @ up, 0.0])


def intersection(normals: ArrayLike, offsets: ArrayLike) -> NDArray[np.float64]:
    normals, offsets = (
        np.asarray(normals, dtype=float),
        np.asarray(offsets, dtype=float),
    )
    if (
        normals.shape != (3, 3)
        or offsets.shape != (3,)
        or np.linalg.matrix_rank(normals) != 3
    ):
        raise ValueError("A unique point requires three independent plane equations.")
    return np.linalg.solve(normals, offsets)
