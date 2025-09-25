# Simple Calculator

A minimal command-line calculator that safely evaluates arithmetic expressions.

## Features

- Support for addition, subtraction, multiplication, division, modulus, floor division, and exponentiation
- Parentheses and unary operators (`+` and `-`)
- Interactive REPL mode or single-expression evaluation
- Safe parsing via Python's `ast` module instead of `eval`

## Usage

Install Python 3.10+ and run:

```bash
python calculator.py "2 * (3 + 4)"
```

To launch the interactive prompt:

```bash
python calculator.py
```

Type `quit` or `exit` to leave the prompt.

## Development

Run the unit tests with:

```bash
python -m unittest discover -s tests
```
