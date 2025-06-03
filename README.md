# PyHDLio-dev

This is the **development repository** for PyHDLio. It contains:
- `PyHDLio/` - The main functional repository (standalone)
- `tests/` - Development tests
- `tools/` - Development tools

## Features

PyHDLio provides VHDL parsing and analysis capabilities including:

- **VHDL Entity Parsing** - Parse VHDL files into structured AST representations
- **Entity Reporting** - Generate formatted reports of entities with their generics and ports
- **Port Grouping** - Display ports in both flat and grouped formats
- **Error Handling** - Robust parsing with meaningful error messages

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

## Examples

See comprehensive examples and documentation:

**📁 [PyHDLio/examples/README.md](PyHDLio/examples/README.md)**

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
