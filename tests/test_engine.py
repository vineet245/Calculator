from decimal import Decimal

import pytest

from engine.calculator import calculate, format_number


@pytest.mark.parametrize("first,second,operation,expected", [
    ("2", "3", "add", "5"),
    ("2", "3", "subtract", "-1"),
    ("0.1", "0.2", "add", "0.3"),
    ("-5", "-3", "subtract", "-2"),
    ("-5", "3", "add", "-2"),
    ("0", "0", "add", "0"),
    ("1.50", "0.50", "subtract", "1"),
    ("-0", "0", "add", "0"),
    ("999999999999999999999999999999", "1", "add", "1000000000000000000000000000000"),
    ("0.000000000001", "0.000000000001", "add", "0.000000000002"),
])
def test_exact_arithmetic(first, second, operation, expected):
    assert format_number(calculate(Decimal(first), Decimal(second), operation)) == expected


def test_engine_rejects_unknown_operation():
    with pytest.raises(ValueError):
        calculate(Decimal(1), Decimal(2), "multiply")


@pytest.mark.parametrize("value", ["NaN", "Infinity", "-Infinity"])
def test_engine_rejects_nonfinite_values(value):
    with pytest.raises(ValueError):
        calculate(Decimal(value), Decimal(1), "add")
