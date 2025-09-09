# PyPI Publishing Guide for fiasto-py

This guide explains how to publish the fiasto-py package to PyPI.

## 📋 Prerequisites

1. **PyPI Account**: Create an account at [pypi.org](https://pypi.org) and [test.pypi.org](https://test.pypi.org)
2. **API Tokens**: Generate API tokens for both Test PyPI and PyPI
3. **Package Name**: Ensure `fiasto-py` is available on PyPI (check at [pypi.org/project/fiasto-py](https://pypi.org/project/fiasto-py))

## 🔧 Setup

### 1. Install Required Tools

```bash
pip install maturin twine
```

### 2. Configure API Tokens

Create a `.pypirc` file in your home directory:

```ini
[distutils]
index-servers = pypi testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

**Security Note**: Never commit API tokens to version control!

## 🚀 Publishing Process

### Step 1: Test Build

First, test the build process:

```bash
python publish.py --test --skip-check
```

This will:
- Clean previous builds
- Build the package with maturin
- Copy wheels to `dist/` directory
- Skip the upload (since we're not providing credentials)

### Step 2: Test Package Quality

Check the built package:

```bash
python publish.py --test --skip-build
```

This will:
- Use existing `dist/` directory
- Run `twine check` to validate the package
- Skip the upload

### Step 3: Publish to Test PyPI

Publish to Test PyPI first:

```bash
python publish.py --test
```

This will:
- Build the package
- Check the package
- Upload to Test PyPI
- Prompt for API token if not configured

### Step 4: Test Installation from Test PyPI

```bash
pip install --index-url https://test.pypi.org/simple/ fiasto-py
```

### Step 5: Publish to PyPI

Once you're satisfied with the Test PyPI version:

```bash
python publish.py
```

This will:
- Build the package
- Check the package
- Ask for confirmation
- Upload to PyPI

## 📝 Manual Publishing (Alternative)

If you prefer to use maturin directly:

### Build

```bash
PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin build --release
```

### Copy to dist

```bash
mkdir -p dist
cp target/wheels/*.whl dist/
```

### Check

```bash
twine check dist/*
```

### Upload to Test PyPI

```bash
twine upload --repository testpypi dist/*
```

### Upload to PyPI

```bash
twine upload dist/*
```

## 🔍 Troubleshooting

### Common Issues

1. **403 Forbidden**: Check your API token and permissions
2. **Package already exists**: The package name might be taken
3. **Build failures**: Ensure Rust and maturin are properly installed
4. **Python 3.13 compatibility**: Use the forward compatibility flag

### Version Management

To update the package:

1. Update version in `pyproject.toml`
2. Update version in `Cargo.toml` (if different)
3. Rebuild and republish

### Package Validation

The package includes:
- ✅ Proper metadata in `pyproject.toml`
- ✅ MIT License
- ✅ Comprehensive README
- ✅ Python 3.8+ compatibility
- ✅ Cross-platform wheels (built on your platform)

## 📦 Package Contents

The published package includes:

- **fiasto_py module**: The main Python extension
- **parse_formula()**: Parse Wilkinson's formulas
- **lex_formula()**: Tokenize formulas
- **Documentation**: Complete README and examples

## 🎯 Post-Publication

After successful publication:

1. **Test installation**: `pip install fiasto-py`
2. **Update documentation**: Ensure README reflects PyPI installation
3. **Monitor downloads**: Check PyPI statistics
4. **Handle issues**: Monitor GitHub issues and PyPI comments

## 🔄 CI/CD Integration

For automated publishing, consider:

1. **GitHub Actions**: Automate builds and publishing
2. **Version tags**: Use git tags for version management
3. **Conditional publishing**: Only publish on main branch
4. **Test matrix**: Test on multiple Python versions

## 📚 Additional Resources

- [PyPI Documentation](https://packaging.python.org/tutorials/packaging-projects/)
- [Maturin Documentation](https://maturin.rs/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [PyO3 Documentation](https://pyo3.rs/)

## ⚠️ Important Notes

- **Package names are permanent**: Choose carefully
- **Version numbers**: Follow semantic versioning
- **API tokens**: Keep them secure and rotate regularly
- **Test first**: Always test on Test PyPI before production
- **Documentation**: Keep README and examples up to date
