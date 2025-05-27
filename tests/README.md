# PyHDLio Test Suite

This directory contains the comprehensive test suite for PyHDLio, organized into a clean, maintainable structure.

## Test Structure

```
tests/
├── conftest.py                           # Pytest configuration and fixtures
├── unit/                                 # Unit tests
│   ├── test_parser.py                   # Core parser functionality
│   ├── test_port_groups.py              # Port grouping logic
│   ├── test_vhdl_standards.py           # VHDL standard support
│   └── test_verilog_parser.py           # Verilog/SystemVerilog parsing
├── integration/                          # Integration tests
│   ├── test_comprehensive_parsing.py    # Comprehensive parsing scenarios
│   ├── test_hdlio_integration.py        # HDLio API integration
│   ├── test_real_world_projects.py      # Real-world project tests
│   └── test_verilog_projects.py         # Verilog project tests
└── fixtures/                            # Test data and fixtures
    ├── simple_module.v                  # Simple Verilog module
    ├── simple_systemverilog.sv          # Simple SystemVerilog interface
    ├── simple_cpu.v                     # Educational CPU implementation
    ├── ddr_controller.v                 # Complex DDR memory controller
    ├── fifo_uvm_test.sv                 # SystemVerilog FIFO with UVM
    ├── test_vhdl.vhd                    # Simple VHDL test file
    ├── simple_entity.vhd                # Basic VHDL entity
    ├── osvvm/                           # OSVVM verification library
    ├── open-logic/                      # Open Logic VHDL library
    ├── en_cl_fix/                       # En_cl_fix VHDL library
    ├── picorv32/                        # PicoRV32 RISC-V CPU
    ├── VexRiscv/                        # VexRiscv RISC-V CPU
    ├── verilog-axi/                     # Verilog AXI components
    ├── verilog-ethernet/                # Verilog Ethernet components
    ├── verilog-uart/                    # Verilog UART components
    ├── basejump_stl/                    # BaseJump STL library
    └── opentitan/                       # OpenTitan hardware
```

## Running Tests

Use the single test runner script in the root directory:

```bash
# Run all tests (excluding slow ones)
python run_tests.py

# Run specific test categories
python run_tests.py --unit              # Unit tests only
python run_tests.py --integration       # Integration tests only
python run_tests.py --parser           # Parser-specific tests
python run_tests.py --port-groups      # Port grouping tests
python run_tests.py --vhdl             # VHDL-specific tests
python run_tests.py --verilog          # Verilog-specific tests

# Output and reporting options
python run_tests.py --verbose          # Verbose output
python run_tests.py --quiet            # Quiet output
python run_tests.py --coverage         # Generate coverage report
python run_tests.py --no-warnings      # Disable warnings

# Special options
python run_tests.py --slow             # Include slow tests
python run_tests.py --list-tests       # List available tests
python run_tests.py --dry-run          # Show what would be run
python run_tests.py --help             # Show all options
```

## Test Categories

Tests are automatically marked based on their location and content:

- `unit`: Unit tests in the `unit/` directory
- `integration`: Integration tests in the `integration/` directory
- `parser`: Parser-related tests
- `port_groups`: Port grouping functionality tests
- `vhdl`: VHDL-specific tests
- `verilog`: Verilog-specific tests
- `systemverilog`: SystemVerilog-specific tests
- `real_world`: Real-world project tests (requires submodules)
- `performance`: Performance benchmark tests
- `slow`: Slow-running tests (excluded by default)

## Environment Setup

The test suite automatically configures itself to use the local PyHDLio directory:

1. **Local PyHDLio Access**: Tests access `PyHDLio/` in the project root, not an adjacent directory
2. **Automatic Path Setup**: The `conftest.py` automatically adds PyHDLio to the Python path
3. **Import Validation**: Tests verify that hdlio can be imported from the local directory

## Test Fixtures

Common test fixtures are defined in `conftest.py`:

- `fixtures_dir`: Path to test fixtures directory
- `simple_vhdl_content`: Simple VHDL entity for basic tests
- `grouped_vhdl_content`: VHDL entity with port groups
- `temp_vhdl_file`: Temporary VHDL file for testing
- `hdlio_parser`: HDLio parser factory function
- `all_vhdl_versions`: List of supported VHDL versions
- `all_verilog_versions`: List of supported Verilog versions

## Writing New Tests

### Unit Tests

Place unit tests in `tests/unit/`. These should test individual functions or classes in isolation.

```python
import pytest
from hdlio import HDLio, VHDL_2008

@pytest.mark.unit
def test_parser_creation():
    """Test that parser can be created"""
    # Test implementation
    pass
```

### Integration Tests

Place integration tests in `tests/integration/`. These should test complete workflows and interactions.

```python
import pytest
import tempfile
from hdlio import HDLio, VHDL_2008

@pytest.mark.integration
def test_complete_parsing_workflow():
    """Test complete parsing workflow"""
    # Test implementation
    pass
```

### Test Markers

Use appropriate pytest markers:

```python
@pytest.mark.unit           # Unit test
@pytest.mark.integration    # Integration test
@pytest.mark.parser         # Parser-related
@pytest.mark.port_groups    # Port grouping
@pytest.mark.vhdl           # VHDL-specific
@pytest.mark.slow           # Slow test (excluded by default)
```

## Coverage Reporting

Generate coverage reports:

```bash
python run_tests.py --coverage
```

This generates:
- Terminal coverage summary
- HTML coverage report in `htmlcov/index.html`

## Validation

The test runner automatically validates the environment setup when you run tests. It checks:
- Local PyHDLio directory access
- Test structure integrity
- Import functionality

Simply run the test suite to validate your setup:

```bash
python run_tests.py
```

## Migration from Legacy Tests

The test suite has been rationalized to eliminate clutter:

### Removed Files
- `test_current_implementation.py` → Consolidated into integration tests
- `test_entity_only.py` → Consolidated into comprehensive parsing tests
- `test_unified_parser.py` → Consolidated into parser tests
- `test_comprehensive.py` → Consolidated into comprehensive parsing tests
- `test_comprehensive_vhdl.py` → Consolidated into comprehensive parsing tests

### Consolidated Functionality
All good functionality from the legacy test files has been preserved and organized into the proper test structure with appropriate pytest markers and fixtures.

## Troubleshooting

### Import Errors
If you see import errors for hdlio:
1. Ensure the `PyHDLio/` directory exists in the project root
2. Verify `PyHDLio/hdlio/` contains the hdlio package
3. Run `python validate_tests.py` to check the setup

### Path Issues
The test suite is configured to use the local PyHDLio directory. If you need to use a different location, update the path in `tests/conftest.py` and `run_tests.py`.

### Missing Tests
If tests are not being discovered:
1. Ensure test files start with `test_`
2. Ensure test functions start with `test_`
3. Check that pytest markers are properly applied
4. Use `python run_tests.py --list-tests` to see discovered tests