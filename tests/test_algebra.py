"""Independent numeric expectations and algebraic invariants for rendered data."""

from fractions import Fraction

import pytest

from manim_portfolio.algebra import (
    INVERSE_INPUT,
    INVERSE_OPERATIONS,
    MULTIPLICAND,
    MULTIPLIER,
    TRANSPOSE_INPUT,
    RowOperation,
    augment_identity,
    exact_matrix,
    inverse_states,
    multiply,
    scalar_tex,
    transpose,
)


def test_product_and_every_dot_product() -> None:
    expected = ((15, 15, 21), (4, 12, 11))
    assert multiply(MULTIPLICAND, MULTIPLIER) == expected
    for i, row in enumerate(expected):
        for j, entry in enumerate(row):
            assert (
                sum(a * b[j] for a, b in zip(MULTIPLICAND[i], MULTIPLIER, strict=True))
                == entry
            )


def test_transpose_correspondence_and_involution() -> None:
    expected = ((1, 4), (-2, 0), (3, 5))
    assert transpose(TRANSPOSE_INPUT) == expected
    assert transpose(expected) == TRANSPOSE_INPUT


def test_inverse_states_against_hand_computed_augmented_rows() -> None:
    states = inverse_states()
    assert states[0] == ((0, 1, 2, 1, 0, 0), (1, 1, 0, 0, 1, 0), (0, 0, 1, 0, 0, 1))
    assert states[1] == ((1, 1, 0, 0, 1, 0), (0, 1, 2, 1, 0, 0), (0, 0, 1, 0, 0, 1))
    assert states[2] == ((1, 1, 0, 0, 1, 0), (0, 1, 0, 1, 0, -2), (0, 0, 1, 0, 0, 1))
    assert states[3] == ((1, 0, 0, -1, 1, 2), (0, 1, 0, 1, 0, -2), (0, 0, 1, 0, 0, 1))
    identity = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    inverse = tuple(row[3:] for row in states[-1])
    assert multiply(INVERSE_INPUT, inverse) == identity
    assert multiply(inverse, INVERSE_INPUT) == identity


def test_row_operations_are_reversible_and_leave_input_immutable() -> None:
    original = augment_identity(INVERSE_INPUT)
    for operation in INVERSE_OPERATIONS:
        result = operation.apply(original)
        reverse = (
            operation
            if operation.kind == "swap"
            else RowOperation(
                "add", operation.target, operation.donor, -operation.factor
            )
        )
        assert reverse.apply(result) == original
    assert original == augment_identity(INVERSE_INPUT)


def test_fractional_operation_does_not_round() -> None:
    result = RowOperation("add", 0, 1, Fraction(1, 3)).apply(((1, 0), (1, 1)))
    assert result == ((Fraction(4, 3), Fraction(1, 3)), (1, 1))
    assert scalar_tex(result[0][0]) == r"\frac{4}{3}"
    assert scalar_tex(Fraction(-2, 3)) == r"-\frac{2}{3}"


@pytest.mark.parametrize("values", [(), ((),), ((1, 2), (3,))])
def test_invalid_matrix_shape(values: tuple) -> None:
    with pytest.raises(ValueError):
        exact_matrix(values)


def test_invalid_operation_dimensions() -> None:
    with pytest.raises(ValueError):
        multiply(((1, 2),), ((3, 4),))
    with pytest.raises(ValueError):
        augment_identity(((1, 2),))
    with pytest.raises(ValueError):
        RowOperation("add", 0, 0)
    with pytest.raises(IndexError):
        RowOperation("swap", -1, 1).apply(((1,), (2,)))
