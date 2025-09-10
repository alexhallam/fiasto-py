# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2024-12-09

### Changed
- Bumped version to 0.1.2 for PyPI publishing

## [0.1.1] - 2024-12-09

### Changed
- Updated fiasto dependency from 0.2.4 to 0.2.5
- Enhanced OLS regression example with improved intercept handling
- Updated README with better examples and documentation

### Added
- Support for intercept detection from formula metadata
- Tidy DataFrame output format for regression coefficients
- Comprehensive usage examples with expected outputs

## [0.1.0] - 2024-12-09

### Added
- Initial release of fiasto-py
- Python bindings for fiasto formula parser and lexer
- `parse_formula()` function returning structured JSON metadata
- `lex_formula()` function returning tokenized formula information
- PyO3 integration for high-performance Rust-Python bindings
- Support for Python 3.8+ with forward compatibility for Python 3.13
- Comprehensive documentation and examples
- PyPI publishing infrastructure
