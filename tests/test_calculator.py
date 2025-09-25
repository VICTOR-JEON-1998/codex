import unittest

from calculator import Calculator, CalculatorError


class TestCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = Calculator()

    def test_basic_operations(self):
        self.assertEqual(self.calc.evaluate("1 + 2"), 3)
        self.assertEqual(self.calc.evaluate("5 - 7"), -2)
        self.assertEqual(self.calc.evaluate("3 * 4"), 12)
        self.assertEqual(self.calc.evaluate("8 / 2"), 4)

    def test_advanced_operations(self):
        self.assertEqual(self.calc.evaluate("2 ** 3"), 8)
        self.assertEqual(self.calc.evaluate("7 % 3"), 1)
        self.assertEqual(self.calc.evaluate("7 // 3"), 2)

    def test_parentheses_and_unary(self):
        self.assertEqual(self.calc.evaluate("-(1 + 2) * 3"), -9)
        self.assertAlmostEqual(self.calc.evaluate("(1 + 2) / (3 + 4)"), 3 / 7)

    def test_invalid_input(self):
        with self.assertRaises(CalculatorError):
            self.calc.evaluate("")
        with self.assertRaises(CalculatorError):
            self.calc.evaluate("1 + spam")


if __name__ == "__main__":
    unittest.main()
