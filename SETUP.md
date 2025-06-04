# PyHDLio-dev Setup Guide

This guide shows how to set up the PyHDLio development environment with **zero manual steps** using the automated requirements system.

## 🚀 One-Command Setup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd PyHDLio-dev

# Run automated setup
python setup_env.py
```

That's it! The script automatically:
- ✅ Initializes git submodules (PyHDLio + pyVHDLModel)
- ✅ Creates virtual environment
- ✅ Installs all local packages in editable mode
- ✅ Installs all dependencies and development tools
- ✅ Verifies installation with tests

## 📋 What Gets Installed

All packages are installed from a single `requirements.txt` file:

### Local Packages (Editable Mode)
- **PyHDLio** (`-e ./PyHDLio`) - Main VHDL parsing library
- **pyVHDLModel** (`-e ./pyVHDLModel`) - Enhanced VHDL model with port groups

### Core Dependencies
- `antlr4-python3-runtime>=4.13.2` - ANTLR runtime for parsing
- `pyTooling>=8.4` - Tooling utilities

### Development Tools
- `pytest>=6.0` - Testing framework
- `pytest-cov>=2.12.0` - Test coverage
- `black>=21.0.0` - Code formatting
- `mypy>=0.910` - Type checking
- `flake8>=3.8` - Linting
- `sphinx>=4.0` - Documentation
- `pre-commit>=2.15.0` - Git hooks

## 🛠️ Manual Setup (Alternative)

If you prefer manual control:

```bash
# Clone and initialize
git clone <repository-url>
cd PyHDLio-dev
git submodule update --init --recursive

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install everything (one command)
pip install -r requirements.txt
```

## 📁 Requirements File Structure

### `requirements.txt` - Everything in One Place
```
# PyHDLio-dev Requirements
# Complete development environment setup

# Local packages (editable installs)
-e ./PyHDLio
-e ./pyVHDLModel

# Core dependencies
antlr4-python3-runtime>=4.13.2
pyTooling>=8.4

# Testing and development tools
pytest>=6.0
pytest-cov>=2.12.0
black>=21.0.0
mypy>=0.910
flake8>=3.8

# Optional development tools
sphinx>=4.0  # For documentation
pre-commit>=2.15.0  # For git hooks
```

## 🧪 Verification

After setup, verify everything works:

```bash
# Activate environment (if not already active)
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Run comprehensive tests
python tests/run_tests.py

# Expected output:
# 🧪 PyHDLio Integration Test Suite
# ==================================================
# ✅ pyVHDLModel available - full test suite will run
# ✅ Test VHDL files found
#
# ..............................
# ----------------------------------------------------------------------
# Ran 29 tests in 0.115s
#
# OK
#
# ==================================================
# 🎯 Test Results Summary:
#    Tests run: 29
#    Failures: 0
#    Errors: 0
#    Skipped: 0
#
# 🎉 All tests passed!
```

## 🎯 Key Benefits

### ✅ Simplified Setup
- Single `requirements.txt` file for everything
- No confusion about which file to use
- Perfect for development-only repository

### ✅ Zero Manual Steps
- No need to manually install PyHDLio with `pip install -e ./PyHDLio`
- No need to manually install pyVHDLModel with `pip install -e ./pyVHDLModel`
- Everything automated in one requirements file

### ✅ Editable Installs
- Changes to PyHDLio code immediately available
- Changes to pyVHDLModel code immediately available
- No need to reinstall after code changes

### ✅ Development Ready
- All testing tools included
- Code formatting and linting ready
- Documentation tools available

## 🔄 Workflow Examples

### Daily Development
```bash
# Activate environment
.venv\Scripts\activate

# Work on code (changes are immediately available due to editable installs)
# Edit files in PyHDLio/ or pyVHDLModel/

# Run tests
python tests/run_tests.py

# Format code
black PyHDLio/ pyVHDLModel/

# Type check
mypy PyHDLio/
```

### CI/Testing
```bash
# Single install command
pip install -r requirements.txt

# Run tests
python tests/run_tests.py
```

### Additional Tools
```bash
# Setup pre-commit hooks
pre-commit install

# Generate documentation
sphinx-build -b html doc/ doc/_build/

# Run linting
flake8 PyHDLio/ pyVHDLModel/
```

## 🚨 Troubleshooting

### Git Submodules Not Initialized
```bash
git submodule update --init --recursive
```

### Import Errors
Ensure packages are installed in editable mode:
```bash
pip list | grep -E "(hdlio|pyVHDL)"
# Should show:
# hdlio         0.1.0   /path/to/PyHDLio-dev/PyHDLio
# pyVHDLModel   0.31.2  /path/to/PyHDLio-dev/pyVHDLModel
```

### Test Failures
Check that all components are working:
```bash
python -c "import hdlio.vhdl.parse_vhdl"
python -c "import pyVHDLModel.DesignUnit"
python -c "from hdlio.vhdl.converters.pyvhdlmodel_converter import convert_to_pyvhdlmodel"
```

### Unicode Issues (Windows)
Our scripts handle Windows encoding automatically, but if you see Unicode errors:
```bash
# Set UTF-8 encoding
set PYTHONIOENCODING=utf-8
python tests/run_tests.py
```

## 📚 Additional Resources

- **[PyHDLio Documentation](PyHDLio/README.md)** - Core library documentation
- **[Test Suite Documentation](tests/README.md)** - Comprehensive testing guide
- **[Examples](PyHDLio/examples/README.md)** - Usage examples and tutorials

This setup provides a clean, simple development environment for the PyHDLio + pyVHDLModel integration project.