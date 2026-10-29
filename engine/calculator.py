"""Pure Python arithmetic; no web or UI dependencies."""

from decimal import Decimal, localcontext
from typing import Literal


def calculate(first: Decimal, second: Decimal, operation: Literal["add", "subtract"]) -> Decimal:
    if not first.is_finite() or not second.is_finite():
        raise ValueError("Please enter finite numbers.")
    # API inputs allow 30 digits each. Leave room for an exact result.
    with localcontext() as context:
        context.prec = 64
        if operation == "add":
            return first + second
        if operation == "subtract":
            return first - second
    raise ValueError("Choose addition or subtraction.")


def format_number(value: Decimal) -> str:
    if value == 0:
        return "0"
    text = format(value, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text
