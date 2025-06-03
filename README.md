# PyHDLio-dev

This is the **development repository** for PyHDLio. It contains:
- `PyHDLio/` - The main functional repository (standalone)
- `tests/` - Development tests
- `tools/` - Development tools

## Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd PyHDLio-dev

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate   # Linux/Mac

# Install all dependencies (including pytest and development tools)
pip install -r requirements.txt

# Install the hdlio package
pip install -e ./PyHDLio

# Run example
python PyHDLio/examples/vhdl/simple/simple.py
```

## Requirements

- Python 3.8+
- Dependencies are listed in `requirements.txt` including:
  - antlr4-python3-runtime>=4.13.2
  - pytest>=6.0 (for testing)
  - pytest-cov>=2.12.0 (for coverage)
  - flake8>=3.8 (for linting)
  - mypy>=0.910 (for type checking)
  - black>=21.0.0 (for code formatting)

Install all dependencies with:
```bash
pip install -r requirements.txt
```

## Testing

This project includes a comprehensive test suite to ensure code quality and reliability.

### Quick Test Run

After following the Quick Start setup above, simply run:

```bash
# Run all tests
python -m pytest tests/ -v
```

### Full Testing Documentation

For complete testing instructions, see:

**📋 [tests/README.md](tests/README.md)**
