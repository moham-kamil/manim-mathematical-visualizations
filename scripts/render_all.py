"""Run the same scene commands documented in README, without a shell wrapper."""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENES = (
    ("matrix_multiplication", "MatrixMultiplication"),
    ("matrix_transpose", "MatrixTranspose"),
    ("gauss_jordan", "GaussJordanInverse"),
    ("plane_intersection", "PlaneIntersection"),
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quality", choices=("preview", "final"), default="final")
    args = parser.parse_args()
    final = args.quality == "final"
    for module, scene in SCENES:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "manim",
                "-qh" if final else "-ql",
                "--fps",
                "60" if final else "30",
                f"src/{module}.py",
                scene,
            ],
            cwd=ROOT,
            check=True,
        )


if __name__ == "__main__":
    main()
