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

# Install the hdlio package
pip install -e ./PyHDLio

# Run example
python PyHDLio/examples/vhdl/simple/simple.py
```

## Requirements

- Python 3.8+
- antlr4-python3-runtime>=4.13.2

Install dependencies with:
```bash
pip install -r requirements.txt
```
