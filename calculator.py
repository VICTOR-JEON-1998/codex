"""Simple command-line calculator implementation.

This module exposes a :class:`Calculator` class capable of safely evaluating
basic arithmetic expressions composed of numbers and the operators ``+``, ``-``,
``*``, ``/``, ``%``, ``//`` and ``**``. Parentheses and unary plus/minus are
also supported. In addition a small command line interface is provided to allow
users to run interactive calculations from the terminal.
"""
from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from typing import Union

Number = Union[int, float]


class CalculatorError(Exception):
    """Raised when an invalid expression is passed to :class:`Calculator`."""


@dataclass
class Calculator:
    """A simple arithmetic expression evaluator."""

    def evaluate(self, expression: str) -> Number:
        """Evaluate a mathematical *expression* and return the numeric result.

        Parameters
        ----------
        expression:
            A string containing a mathematical expression using the supported
            operators. Whitespace is ignored.

        Returns
        -------
        int | float
            The result of the calculation.

        Raises
        ------
        CalculatorError
            If *expression* contains unsupported syntax or cannot be parsed.
        """

        if expression is None:
            raise CalculatorError("Expression cannot be None")

        stripped = expression.strip()
        if not stripped:
            raise CalculatorError("Expression cannot be empty")

        try:
            parsed = ast.parse(stripped, mode="eval")
        except SyntaxError as exc:  # pragma: no cover - defensive branch
            raise CalculatorError("Invalid syntax") from exc

        return self._evaluate_node(parsed.body)

    def _evaluate_node(self, node: ast.AST) -> Number:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise CalculatorError(f"Unsupported constant: {node.value!r}")
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            operand = self._evaluate_node(node.operand)
            return operand if isinstance(node.op, ast.UAdd) else -operand
        if isinstance(node, ast.BinOp):
            left = self._evaluate_node(node.left)
            right = self._evaluate_node(node.right)
            return self._apply_operator(node.op, left, right)

        raise CalculatorError(f"Unsupported expression: {ast.dump(node, include_attributes=False)}")

    @staticmethod
    def _apply_operator(op: ast.AST, left: Number, right: Number) -> Number:
        if isinstance(op, ast.Add):
            return left + right
        if isinstance(op, ast.Sub):
            return left - right
        if isinstance(op, ast.Mult):
            return left * right
        if isinstance(op, ast.Div):
            return left / right
        if isinstance(op, ast.FloorDiv):
            return left // right
        if isinstance(op, ast.Mod):
            return left % right
        if isinstance(op, ast.Pow):
            return left ** right
        raise CalculatorError(f"Unsupported operator: {op.__class__.__name__}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate simple mathematical expressions.")
    parser.add_argument("expression", nargs="?", help="Expression to evaluate. If omitted an interactive prompt is shown.")
    return parser


def repl(calculator: Calculator) -> None:
    print("Simple Calculator. Type 'quit' or 'exit' to stop.")
    while True:
        try:
            expression = input("calc> ")
        except EOFError:  # pragma: no cover - depends on terminal
            print()
            break
        if expression.strip().lower() in {"quit", "exit"}:
            break
        try:
            result = calculator.evaluate(expression)
        except CalculatorError as exc:
            print(f"Error: {exc}")
        else:
            print(result)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    calc = Calculator()

    if args.expression:
        try:
            result = calc.evaluate(args.expression)
        except CalculatorError as exc:
            parser.error(str(exc))
        else:
            print(result)
    else:
        repl(calc)

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
