# PyHDLio Testing Guide

This directory contains the test suite for PyHDLio development.

## Test Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   └── test_vhdl_parser.py  # VHDL parser unit tests
├── fixtures/                # Test fixtures and sample files
│   └── vhdl/
│       └── life_signs.vhd   # Minimal VHDL entity for basic testing
└── README.md                # This file
```

## Prerequisites

Before running tests...

1. **Activate the virtual environment:**
   ```bash
   # Windows PowerShell
   .venv\Scripts\Activate.ps1

   # Linux/Mac
   source .venv/bin/activate
   ```

2. **Install all dependencies (including pytest):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install PyHDLio in development mode:**
   ```bash
   pip install -e ./PyHDLio
   ```

## Running Tests

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Unit Tests Only
```bash
python -m pytest tests/unit/ -v
```

### Run Specific Test File
```bash
python -m pytest tests/unit/test_vhdl_parser.py -v
```

### Run Specific Test Method
```bash
python -m pytest tests/unit/test_vhdl_parser.py::TestVHDLParser::test_parse_life_signs_vhdl -v
```

### Additional Options

- **Show coverage:** `python -m pytest tests/ --cov=hdlio`
- **Stop on first failure:** `python -m pytest tests/ -x`
- **Show detailed output:** `python -m pytest tests/ -vv`
- **Run quietly:** `python -m pytest tests/ -q`

## Test Categories

### Unit Tests (`tests/unit/`)

Unit tests verify individual components in isolation:

- **`test_vhdl_parser.py`** - Tests for VHDL parsing functionality
  - `test_parse_life_signs_vhdl()` - Basic "life signs" test using minimal VHDL fixture
  - `test_parse_nonexistent_file()` - Error handling for missing files
  - `test_parse_vhdl_file_path_handling()` - File path processing tests

### Test Fixtures (`tests/fixtures/`)

Reusable test data and sample files:

- **`vhdl/life_signs.vhd`** - Minimal VHDL entity for basic parser validation

## Writing New Tests

### Adding Unit Tests

1. Create test files in `tests/unit/` following the pattern `test_<module>.py`
2. Use the `TestClassName` convention for test classes
3. Prefix test methods with `test_`
4. Include docstrings explaining what each test validates

Example:
```python
import pytest
from hdlio.module import function_to_test

class TestModuleName:
    """Unit tests for module functionality."""

    def test_specific_behavior(self):
        """Test that specific behavior works correctly."""
        result = function_to_test("input")
        assert result == "expected_output"
```

### Adding Test Fixtures

1. Place reusable test data in appropriate subdirectories under `tests/fixtures/`
2. Use descriptive filenames
3. Keep fixtures minimal but representative
4. Document the purpose of each fixture

### Path Handling in Tests

When referencing fixtures from unit tests:
```python
import os

# Get fixture path from unit test
fixture_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),  # Go up to tests/
    'fixtures',
    'vhdl',
    'your_fixture.vhd'
)
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError for hdlio:**
   - Ensure PyHDLio is installed: `pip install -e ./PyHDLio`

2. **Fixture not found:**
   - Check file paths in test code
   - Verify fixture files exist in `tests/fixtures/`

3. **Tests not discovered:**
   - Ensure test files start with `test_`
   - Ensure test functions start with `test_`
   - Check that pytest.ini configuration is correct

4. **Missing dependencies:**
   - Ensure all requirements are installed: `pip install -r requirements.txt`

### Getting Help

- Check test output for detailed error messages
- Use `python -m pytest tests/ -vv` for verbose output
- Verify virtual environment is activated
- Ensure all dependencies are installed

## Continuous Integration

Tests should pass before merging code changes. The test suite serves as:
- **Regression prevention** - Catch breaking changes
- **Documentation** - Show expected behavior
- **Quality assurance** - Maintain code reliability
