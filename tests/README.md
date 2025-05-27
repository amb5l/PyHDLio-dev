# HDLio Test Suite

This directory contains the test suite for HDLio, organized using pytest for automated regression testing.

## Test Organization

### Directory Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── unit/                    # Unit tests
│   ├── test_parser.py       # Parser functionality tests
│   └── test_port_groups.py  # Port grouping tests
├── integration/             # Integration tests
│   ├── test_hdlio_integration.py     # End-to-end workflow tests
│   └── test_real_world_projects.py  # Real-world project tests
├── fixtures/                # Test data files
│   ├── simple_entity.vhd    # Simple VHDL entity
│   └── test_vhdl.vhd        # Complex VHDL with port groups
├── vhdl/                    # VHDL test projects
│   ├── en_cl_fix/           # Enclustra fixed-point library
│   ├── osvvm/               # OSVVM verification library
│   └── open-logic/          # Open Logic library
├── verilog/                 # Verilog/SystemVerilog test projects
│   ├── simple_cpu.v         # Educational 8-bit CPU implementation
│   ├── ddr_controller.v     # Complex DDR memory controller with AXI4
│   ├── fifo_uvm_test.sv     # Advanced SystemVerilog FIFO with UVM
│   ├── picorv32/            # RISC-V CPU implementation
│   ├── VexRiscv/            # Another RISC-V CPU
│   ├── opentitan/           # Google's OpenTitan security chip
│   ├── basejump_stl/        # BaseJump STL library
│   ├── verilog-axi/         # Verilog AXI components
│   ├── verilog-ethernet/    # Verilog Ethernet components
│   └── verilog-uart/        # Verilog UART components
└── legacy/                  # Legacy test files (preserved for reference)
    ├── test_example.py
    ├── test_port_groups.py
    └── test_simple_entity.py
```

### Test Categories

Tests are organized using pytest markers:

- **`@pytest.mark.unit`**: Unit tests for individual components
- **`@pytest.mark.integration`**: Integration tests for complete workflows
- **`@pytest.mark.parser`**: Parser-specific tests
- **`@pytest.mark.port_groups`**: Port grouping functionality tests
- **`@pytest.mark.vhdl`**: VHDL-specific tests
- **`@pytest.mark.verilog`**: Verilog-specific tests
- **`@pytest.mark.systemverilog`**: SystemVerilog-specific tests
- **`@pytest.mark.real_world`**: Real-world project tests (requires submodules)
- **`@pytest.mark.performance`**: Performance benchmark tests
- **`@pytest.mark.slow`**: Tests that take more than 1 second

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install pytest pytest-cov
```

### Basic Test Execution

Run all tests:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

### Using the Test Runner Script

The project includes a convenient test runner script:

```bash
# Run all tests (excluding slow tests)
python run_tests.py

# Run only unit tests
python run_tests.py --unit

# Run only integration tests
python run_tests.py --integration

# Run port grouping tests specifically
python run_tests.py --port-groups

# Run parser tests specifically
python run_tests.py --parser

# Run VHDL tests specifically
python run_tests.py --vhdl

# Run Verilog tests specifically
python run_tests.py --verilog

# Run SystemVerilog tests specifically
python run_tests.py --systemverilog

# Include slow tests
python run_tests.py --slow

# Run with coverage reporting
python run_tests.py --coverage

# Verbose output
python run_tests.py --verbose
```

### Pytest Commands

Run specific test categories:
```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Port grouping tests
pytest -m port_groups

# Parser tests
pytest -m parser

# VHDL-specific tests
pytest -m vhdl

# Verilog-specific tests
pytest -m verilog

# SystemVerilog-specific tests
pytest -m systemverilog

# Real-world project tests
pytest -m real_world

# Performance tests
pytest -m performance

# Exclude slow tests
pytest -m "not slow"
```

Run specific test files:
```bash
pytest tests/unit/test_parser.py
pytest tests/integration/test_hdlio_integration.py
```

Run specific test methods:
```bash
pytest tests/unit/test_port_groups.py::TestPortGrouping::test_simple_entity_auto_grouping
```

### Coverage Reports

Generate coverage reports:
```bash
pytest --cov=hdlio --cov-report=html --cov-report=term
```

View HTML coverage report:
```bash
# Coverage report will be in htmlcov/index.html
```

## Test Fixtures

The test suite uses pytest fixtures for reusable test data:

- **`fixtures_dir`**: Path to test fixtures directory
- **`simple_vhdl_file`**: Path to simple VHDL test file
- **`complex_vhdl_file`**: Path to complex VHDL test file
- **`simple_vhdl_content`**: Simple VHDL entity content
- **`grouped_vhdl_content`**: VHDL entity with port groups
- **`temp_vhdl_file`**: Temporary VHDL file for testing
- **`hdlio_parser`**: HDLio parser factory function
- **`verilog_files_dir`**: Path to Verilog test files directory
- **`simple_cpu_file`**: Path to simple_cpu.v test file
- **`ddr_controller_file`**: Path to ddr_controller.v test file
- **`fifo_uvm_test_file`**: Path to fifo_uvm_test.sv test file
- **`verilog_parser`**: HDLio parser factory for Verilog 2005
- **`systemverilog_parser`**: HDLio parser factory for SystemVerilog 2012

## Writing New Tests

### Unit Test Example

```python
import pytest
from hdlio import HDLio, VHDL_2008

class TestNewFeature:
    @pytest.mark.unit
    def test_new_functionality(self, temp_vhdl_file, hdlio_parser):
        """Test new functionality"""
        hdl = hdlio_parser(str(temp_vhdl_file))
        # Test implementation
        assert hdl is not None
```

### Integration Test Example

```python
@pytest.mark.integration
@pytest.mark.vhdl
def test_complete_workflow(self, tmp_path, grouped_vhdl_content):
    """Test complete workflow"""
    vhdl_file = tmp_path / "test.vhd"
    vhdl_file.write_text(grouped_vhdl_content)
    
    hdl = HDLio(str(vhdl_file), VHDL_2008)
    design_units = hdl.getDesignUnits()
    # Test complete workflow
```

### Verilog Test Example

```python
@pytest.mark.integration
@pytest.mark.verilog
def test_verilog_parsing(self, simple_cpu_file, verilog_parser):
    """Test Verilog module parsing"""
    hdl = verilog_parser(str(simple_cpu_file))
    design_units = hdl.getDesignUnits()
    
    # Verify modules are found
    module_names = [unit.getName() for unit in design_units]
    assert 'simple_cpu' in module_names
    assert 'alu' in module_names
```

## Continuous Integration

The test suite is designed to work with CI/CD systems:

```yaml
# Example GitHub Actions workflow
- name: Install dependencies
  run: pip install pytest pytest-cov

- name: Run tests
  run: pytest --cov=hdlio --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v1
```

## Test Data

### VHDL Test Files
Test fixtures are located in `tests/fixtures/`:
- VHDL files for testing parsing functionality
- Expected output data for regression testing
- Performance test data

### Verilog Test Files
The `tests/verilog/` directory contains Verilog and SystemVerilog test files:

#### Core Test Files
- **`simple_cpu.v`**: Educational 8-bit CPU implementation with ALU
  - Contains `simple_cpu` and `alu` modules
  - Tests basic Verilog parsing and module extraction
  - Used for port extraction testing

- **`ddr_controller.v`**: Complex DDR memory controller with AXI4 interface
  - Advanced Verilog with parameterized modules
  - Tests complex state machines and memory interfaces
  - Performance testing target

- **`fifo_uvm_test.sv`**: Advanced SystemVerilog FIFO with UVM verification
  - SystemVerilog interfaces, classes, and assertions
  - UVM testbench components
  - Tests SystemVerilog language features

#### Submodule Projects
Real-world Verilog projects included as git submodules:
- **PicoRV32**: RISC-V CPU implementation
- **VexRiscv**: Another RISC-V CPU design
- **OpenTitan**: Google's security chip design
- **BaseJump STL**: SystemVerilog standard template library
- **Verilog-AXI**: AXI bus components
- **Verilog-Ethernet**: Ethernet MAC and PHY components
- **Verilog-UART**: UART communication components

## Legacy Tests

Legacy test files are preserved in `tests/legacy/` for reference but are not run as part of the automated test suite. These can be useful for:
- Understanding historical test approaches
- Manual testing during development
- Reference implementations

## Best Practices

1. **Use descriptive test names** that explain what is being tested
2. **Use appropriate markers** to categorize tests
3. **Use fixtures** for reusable test data and setup
4. **Test both success and failure cases**
5. **Keep tests focused** on specific functionality
6. **Use parameterized tests** for testing multiple scenarios
7. **Add performance tests** for critical functionality 