# fiasto-py

[![PyPI version](https://badge.fury.io/py/fiasto-py.svg)](https://badge.fury.io/py/fiasto-py)
[![Python versions](https://img.shields.io/pypi/pyversions/fiasto-py.svg)](https://pypi.org/project/fiasto-py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<h1 align="center">fiasto-py</h1>

<p align="center">
  <img src="img/mango_pixle2_py.png" alt="logo" width="240">
</p>

---

<p align="center">Pronouned like <strong>fiasco</strong>, but with a <strong>t</strong> instead of a <strong>c</strong></p>

---

<p align="center">(F)ormulas (I)n (AST) (O)ut</p>

Python bindings for [fiasto](https://github.com/alexhallam/fiasto) - A language-agnostic modern Wilkinson's formula parser and lexer.

## 🎯 Features

- **Parse Wilkinson's Formulas**: Convert formula strings into structured JSON metadata
- **Tokenize Formulas**: Break down formulas into individual tokens with detailed information
- **Python Dictionaries**: Returns native Python dictionaries for easy integration

## 🚀 Quick Start

### Installation

**Install from PyPI** (recommended):
```bash
pip install fiasto-py
```

### Usage

```python
import fiasto_py

# Parse a formula into structured metadata
result = fiasto_py.parse_formula("y ~ x1 + x2 + (1|group)")
print(result)

# Tokenize a formula
tokens = fiasto_py.lex_formula("y ~ x1 * x2 + s(z)")
print(tokens)
```

### Example

```python
import fiasto_py
import json

# Parse a complex mixed-effects formula
formula = "y ~ x1 * x2 + s(z) + (1+x1|group)"
parsed = fiasto_py.parse_formula(formula)

# Pretty print the result
print(json.dumps(parsed, indent=2))

# Tokenize the same formula
tokens = fiasto_py.lex_formula(formula)
print(json.dumps(tokens, indent=2))
```

## 📋 Supported Formula Syntax

`fiasto` supports comprehensive Wilkinson's notation including:

- **Basic formulas**: `y ~ x1 + x2`
- **Interactions**: `y ~ x1 * x2`
- **Smooth terms**: `y ~ s(z)`
- **Random effects**: `y ~ x + (1|group)`
- **Complex random effects**: `y ~ x + (1+x|group)`

### Supported Formulas (Coming Soon)

- **Multivariate models**: `mvbind(y1, y2) ~ x + (1|g)`
- **Non-linear models**: `y ~ a1 - a2^x, a1 ~ 1, a2 ~ x + (x|g), nl = TRUE`

For the complete reference, see the [fiasto documentation](https://docs.rs/fiasto/latest/fiasto/).

## 📦 PyPI Package

The package is available on PyPI and can be installed with:

```bash
pip install fiasto-py
```

- **PyPI Page**: [pypi.org/project/fiasto-py](https://pypi.org/project/fiasto-py/)
- **Source Code**: [github.com/alexhallam/fiasto-py](https://github.com/alexhallam/fiasto-py)
- **Documentation**: This README and inline docstrings


## 📚 API Reference

### `parse_formula(formula: str) -> dict`

Parse a Wilkinson's formula string and return structured JSON metadata.

**Parameters:**
- `formula` (str): The formula string to parse

**Returns:**
- `dict`: Structured metadata describing the formula

**Raises:**
- `ValueError`: If the formula is invalid or parsing fails

### `lex_formula(formula: str) -> dict`

Tokenize a formula string and return JSON describing each token.

**Parameters:**
- `formula` (str): The formula string to tokenize

**Returns:**
- `dict`: Token information for each element in the formula

**Raises:**
- `ValueError`: If the formula is invalid or lexing fails

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- [fiasto](https://github.com/alexhallam/fiasto) - The underlying Rust library
- [PyO3](https://pyo3.rs/) - Python-Rust bindings
- [maturin](https://maturin.rs/) - Build system for Python extensions
- [PyPI](https://pypi.org/) - Python Package Index for distribution

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
