# fiasto-py

Python bindings for [fiasto](https://github.com/alexhallam/fiasto) - A language-agnostic modern Wilkinson's formula parser and lexer.

## 🎯 Features

- **Parse Wilkinson's Formulas**: Convert formula strings into structured JSON metadata
- **Tokenize Formulas**: Break down formulas into individual tokens with detailed information
- **High Performance**: Built with Rust and PyO3 for maximum speed
- **Python Dictionaries**: Returns native Python dictionaries for easy integration

## 🚀 Quick Start

### Installation

1. **Install from PyPI** (recommended):
   ```bash
   pip install fiasto-py
   ```

2. **Build from source** (for development):
   ```bash
   # Install maturin if you haven't already
   pip install maturin
   
   # Build and install in development mode
   # Note: For Python 3.13, use the forward compatibility flag
   PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin develop
   ```

3. **Or use the build script**:
   ```bash
   python build.py
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

fiasto supports comprehensive Wilkinson's notation including:

- **Basic formulas**: `y ~ x1 + x2`
- **Interactions**: `y ~ x1 * x2`
- **Smooth terms**: `y ~ s(z)`
- **Random effects**: `y ~ x + (1|group)`
- **Complex random effects**: `y ~ x + (1+x|group)`
- **Multivariate models**: `mvbind(y1, y2) ~ x + (1|g)`
- **Non-linear models**: `y ~ a1 - a2^x, a1 ~ 1, a2 ~ x + (x|g), nl = TRUE`

For the complete syntax reference, see the [fiasto documentation](https://github.com/alexhallam/fiasto).

## 🛠️ Development

### Prerequisites

- Python 3.8+
- Rust (latest stable)
- maturin

### Building

```bash
# Development build (with Python 3.13 compatibility)
PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin develop

# Release build
PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin build --release

# Run tests
python example.py
```

### Project Structure

```
fiasto-py/
├── src/
│   └── lib.rs          # PyO3 module definition
├── Cargo.toml          # Rust dependencies
├── pyproject.toml      # Python package configuration
├── build.py            # Build script
├── example.py          # Usage examples
└── README.md           # This file
```

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

## 📄 License

This project is licensed under the MIT License - see the [fiasto repository](https://github.com/alexhallam/fiasto) for details.

## 🙏 Acknowledgments

- [fiasto](https://github.com/alexhallam/fiasto) - The underlying Rust library
- [PyO3](https://pyo3.rs/) - Python-Rust bindings
- [maturin](https://maturin.rs/) - Build system for Python extensions
