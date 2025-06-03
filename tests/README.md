# PyHDLio Testing Guide

This directory contains the test suite for PyHDLio development.

## Test Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   └── test_vhdl_parser.py  # VHDL parser unit tests
├── fixtures/                # Test fixtures and sample files
│   └── vhdl/
│       ├── life_signs.vhd   # Minimal VHDL entity for basic testing
│       └── entity_with_ports.vhd  # Complex entity with generics and ports
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
  - `test_parse_life_signs_vhdl_ast_mode()` - AST mode parsing test for minimal entity
  - `test_entity_reporting()` - Entity reporting functionality test
  - `test_entity_with_ports_and_generics()` - Comprehensive test for complex entities with ports and generics
  - `test_parse_nonexistent_file()` - Error handling for missing files
  - `test_parse_vhdl_file_path_handling()` - File path processing tests

### Test Fixtures (`tests/fixtures/`)

Reusable test data and sample files:

- **`vhdl/life_signs.vhd`** - Minimal VHDL entity for basic parser validation
  - Contains simple entity declaration with no generics or ports
  - Used for "life signs" testing to verify basic parsing functionality

- **`vhdl/entity_with_ports.vhd`** - Complex VHDL entity for comprehensive testing  
  - Contains entity with both generics and ports
  - Demonstrates generic parameters with default values
  - Includes ports with different directions and complex types
  - Used for testing AST extraction and entity reporting features

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

### Testing AST Functionality

For testing AST parsing and entity extraction:

```python
def test_ast_parsing(self):
    """Test AST parsing extracts entity information correctly."""
    # Parse in AST mode
    result = parse_vhdl(fixture_path, mode='ast')
    
    # Verify module structure
    assert isinstance(result, VHDLModule)
    assert len(result.entities) == 1
    
    # Verify entity details
    entity = result.entities[0]
    assert entity.name == "expected_name"
    
    # Verify generics
    assert len(entity.generics) == expected_count
    for generic in entity.generics:
        assert generic.name
        assert generic.type
        # Check default_value if applicable
    
    # Verify ports
    assert len(entity.ports) == expected_count
    for port in entity.ports:
        assert port.name
        assert port.direction in ["in", "out", "inout"]
        assert port.type
```

### Testing Entity Reporting

For testing the reporting functionality:

```python
def test_entity_reporting(self):
    """Test entity reporting generates expected output."""
    result = parse_vhdl(fixture_path, mode='ast')
    
    # Test basic reporting
    report = report_entities(result)
    assert "Entity:" in report
    assert "Generics:" in report
    assert "Ports:" in report
    
    # Test grouped reporting
    grouped_report = report_entities(result, group_ports=True)
    assert "Group" in grouped_report
```

### Adding Test Fixtures

1. Place reusable test data in appropriate subdirectories under `tests/fixtures/`
2. Use descriptive filenames that indicate the fixture's purpose
3. Keep fixtures minimal but representative of real-world usage
4. Document the purpose and contents of each fixture

Example VHDL fixtures:
- **Simple entities** - For basic parsing tests
- **Complex entities** - For comprehensive feature testing  
- **Error cases** - For testing error handling
- **Edge cases** - For boundary condition testing

### Path Handling in Tests

When referencing fixtures from unit tests:
```python
import os

class TestVHDLParser:
    def setup_method(self):
        """Setup common paths for all tests."""
        self.fixture_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),  # Go up to tests/
            'fixtures', 'vhdl'
        )
        self.life_signs_path = os.path.join(self.fixture_dir, 'life_signs.vhd')
        self.entity_with_ports_path = os.path.join(self.fixture_dir, 'entity_with_ports.vhd')
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

5. **AST parsing tests failing:**
   - Verify the VHDL fixture syntax is correct
   - Check that visitor implementation matches VHDL grammar structure
   - Ensure AST classes are properly imported

### Getting Help

- Check test output for detailed error messages
- Use `python -m pytest tests/ -vv` for verbose output
- Verify virtual environment is activated
- Ensure all dependencies are installed
- For AST-related issues, check the visitor implementation and grammar compatibility

## Test Coverage

Current test coverage includes:

### VHDL Parser Tests
- ✅ Basic VHDL parsing (tree mode)
- ✅ AST mode parsing
- ✅ Entity name extraction
- ✅ Generic parameter extraction (name, type, default values)
- ✅ Port extraction (name, direction, type)
- ✅ Port grouping functionality
- ✅ Entity reporting (flat and grouped modes)
- ✅ Error handling (file not found, syntax errors)
- ✅ File path processing

### Areas for Future Test Expansion
- Complex VHDL language constructs
- Multiple entities per file
- Advanced port grouping based on comments/whitespace
- Performance testing with large VHDL files
- Integration tests with real-world VHDL projects

## Continuous Integration

Tests should pass before merging code changes. The test suite serves as:
- **Regression prevention** - Catch breaking changes
- **Documentation** - Show expected behavior through examples
- **Quality assurance** - Maintain code reliability and correctness
- **Feature validation** - Verify new functionality works as intended

Run the full test suite with verbose output before committing:
```bash
python -m pytest tests/ -v
```
