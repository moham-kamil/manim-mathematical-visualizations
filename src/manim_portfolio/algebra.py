"""Exact arithmetic used to generate displayed values, independent of Manim."""

from dataclasses import dataclass
from fractions import Fraction
from typing import Literal, Sequence

Scalar = int | Fraction
Matrix = tuple[tuple[Fraction, ...], ...]

MULTIPLICAND = ((2, 1, 5), (1, 3, 2))
MULTIPLIER = ((3, 4, 0), (-1, 2, 1), (2, 1, 4))
TRANSPOSE_INPUT = ((1, -2, 3), (4, 0, 5))
INVERSE_INPUT = ((0, 1, 2), (1, 1, 0), (0, 0, 1))


def exact_matrix(values: Sequence[Sequence[Scalar]]) -> Matrix:
    """Reject empty/ragged arrays before laying out an animation."""
    if not values or not values[0]:
        raise ValueError("A matrix must have at least one row and column.")
    width = len(values[0])
    if any(len(row) != width for row in values):
        raise ValueError("Every row must have the same length.")
    return tuple(tuple(Fraction(value) for value in row) for row in values)


def multiply(
    left: Sequence[Sequence[Scalar]], right: Sequence[Sequence[Scalar]]
) -> Matrix:
    a, b = exact_matrix(left), exact_matrix(right)
    if len(a[0]) != len(b):
        raise ValueError("Inner matrix dimensions must agree.")
    return tuple(
        tuple(
            sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0))
            for j in range(len(b[0]))
        )
        for i in range(len(a))
    )


def transpose(values: Sequence[Sequence[Scalar]]) -> Matrix:
    matrix = exact_matrix(values)
    return tuple(tuple(column) for column in zip(*matrix, strict=True))


def augment_identity(values: Sequence[Sequence[Scalar]]) -> Matrix:
    matrix = exact_matrix(values)
    n = len(matrix)
    if len(matrix[0]) != n:
        raise ValueError("Inverse construction requires a square matrix.")
    return tuple(
        row + tuple(Fraction(i == j) for j in range(n)) for i, row in enumerate(matrix)
    )


@dataclass(frozen=True)
class RowOperation:
    """A row swap or target <- target + factor * donor (zero-based indices)."""

    kind: Literal["swap", "add"]
    target: int
    donor: int
    factor: Fraction = Fraction(1)

    def __post_init__(self) -> None:
        if self.kind not in {"swap", "add"}:
            raise ValueError("Unknown row operation.")
        if self.target == self.donor:
            raise ValueError("Select distinct rows.")

    @property
    def tex(self) -> str:
        target, donor = self.target + 1, self.donor + 1
        if self.kind == "swap":
            return rf"R_{{{target}}}\leftrightarrow R_{{{donor}}}"
        sign = "+" if self.factor >= 0 else "-"
        magnitude = "" if abs(self.factor) == 1 else scalar_tex(abs(self.factor))
        return rf"R_{{{target}}}\leftarrow R_{{{target}}}{sign}{magnitude}R_{{{donor}}}"

    def apply(self, values: Sequence[Sequence[Scalar]]) -> Matrix:
        rows = [list(row) for row in exact_matrix(values)]
        if not (0 <= self.target < len(rows) and 0 <= self.donor < len(rows)):
            raise IndexError("Row index out of range.")
        if self.kind == "swap":
            rows[self.target], rows[self.donor] = rows[self.donor], rows[self.target]
        else:
            rows[self.target] = [
                value + self.factor * donor
                for value, donor in zip(
                    rows[self.target], rows[self.donor], strict=True
                )
            ]
        return exact_matrix(rows)


INVERSE_OPERATIONS = (
    RowOperation("swap", 0, 1),
    RowOperation("add", 1, 2, Fraction(-2)),
    RowOperation("add", 0, 1, Fraction(-1)),
)


def inverse_states() -> tuple[Matrix, ...]:
    states = [augment_identity(INVERSE_INPUT)]
    for operation in INVERSE_OPERATIONS:
        states.append(operation.apply(states[-1]))
    return tuple(states)


def scalar_tex(value: Scalar) -> str:
    number = Fraction(value)
    if number.denominator == 1:
        return str(number.numerator)
    sign = "-" if number < 0 else ""
    return rf"{sign}\frac{{{abs(number.numerator)}}}{{{number.denominator}}}"
