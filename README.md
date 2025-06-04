# PyHDLio-dev

This is the **development repository** for PyHDLio. It contains:
- `PyHDLio/` - The main functional repository (standalone)
- `pyVHDLModel/` - A fork of the pyVHDLModel repository with port group support
- `tests/` - Development tests
- `tools/` - Development tools

Read more about PyHDLio [here](PyHDLio/README.md).

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone and setup
git clone <repository-url>
cd PyHDLio-dev

# Run automated setup script
python setup_env.py
```

The setup script will:
- ✅ Initialize git submodules (PyHDLio and pyVHDLModel)
- ✅ Create virtual environment
- ✅ Install all local packages and dependencies
- ✅ Verify installation with tests

### Option 2: Manual Setup

```bash
# Clone and setup
git clone <repository-url>
cd PyHDLio-dev

# Initialize submodules (if not done automatically)
git submodule update --init --recursive

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate.bat  # Windows Command Prompt
# or
.venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate   # Linux/Mac

# Install everything (local packages + dependencies + dev tools)
pip install -r requirements.txt
```

### Run Example

```bash
# After setup, activate environment if not already active
# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate

# Run example
python PyHDLio/examples/vhdl/simple/simple.py
```

## Usage Example

```python
from hdlio.vhdl.parse_vhdl import parse_vhdl
from hdlio.vhdl.reporter import print_report

# Parse VHDL file into AST
module = parse_vhdl("your_file.vhd", mode='ast')

# Generate entity reports
print("=== Flat Ports ===")
print_report(module, group_ports=False)

print("=== Grouped Ports ===")
print_report(module, group_ports=True)
```

## Requirements

This development repository includes everything in one `requirements.txt`:

- **Local Packages (Editable):**
  - ✅ PyHDLio package (`-e ./PyHDLio`)
  - ✅ pyVHDLModel package (`-e ./pyVHDLModel`)

- **Core Dependencies:**
  - `antlr4-python3-runtime>=4.13.2` - ANTLR runtime for parsing
  - `pyTooling>=8.4` - Tooling utilities

- **Development Tools:**
  - `pytest>=6.0` - Testing framework
  - `pytest-cov>=2.12.0` - Test coverage
  - `black>=21.0.0` - Code formatting  
  - `mypy>=0.910` - Type checking
  - `flake8>=3.8` - Linting
  - `sphinx>=4.0` - Documentation
  - `pre-commit>=2.15.0` - Git hooks

## Requirements

- Python 3.8+
- Git (for submodules)
- Everything else installed automatically from `requirements.txt`

## Examples

See comprehensive examples and documentation:

**📁 [PyHDLio/examples/README.md](PyHDLio/examples/README.md)**

## Testing

This project includes a comprehensive test suite to ensure code quality and reliability.

### Quick Test Run

After setup, run tests:

```bash
# Run all integration tests
python tests/run_tests.py

# Or with pytest
python -m pytest tests/ -v
```

### Full Testing Documentation

For complete testing instructions, see:

**📋 [tests/README.md](tests/README.md)**
