# PyHDLio-dev

This is the **development repository** for PyHDLio. It contains:
- `PyHDLio/` - The main functional repository (standalone)
- `PyHDLioVHDLModel/` - A fork of the pyVHDLModel project with port group support
- `tests/` - Development tests
- `tools/` - Development tools

Read more about what PyHDLio is and what it can do [here](PyHDLio/README.md).

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

### Running an Example

```bash
# After setup, activate environment if not already active
.venv\Scripts\activate.bat  # Windows Command Prompt
# or
.venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate   # Linux/Mac

# Run VHDL input example
cd PyHDLio/examples/vhdl_in/
python vhdl_in.py sample.vhd
```

## Requirements

- Python 3.8+
- Git (for submodules)
- Packages (in `requirements.txt`):
  - **Local Packages (Editable):**
    - `PyHDLio`
    - `PyHDLioVHDLModel`
  - **Core Dependencies:**
    - `antlr4-python3-runtime>=4.13.2` - ANTLR runtime for parsing
    - `pyTooling>=8.5` - tooling for PyHDLioVHDLModel
  - **Development Tools:**
    - `pytest>=6.0` - Testing framework
    - `pytest-cov>=2.12.0` - Test coverage
    - `black>=21.0.0` - Code formatting
    - `mypy>=0.910` - Type checking
    - `flake8>=3.8` - Linting
    - `sphinx>=4.0` - Documentation
    - `pre-commit>=2.15.0` - Git hooks

## Examples

For information on examples, see [PyHDLio/examples/README.md](PyHDLio/examples/README.md).

## Testing

For testing instructions, see [tests/README.md](tests/README.md).
