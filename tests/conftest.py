"""
Pytest configuration and fixtures for HDLio tests
"""

import pytest
import os
import sys
from pathlib import Path

# Add hdlio to the path for testing
TEST_DIR = Path(__file__).parent
PROJECT_ROOT = TEST_DIR.parent

def setup_pyhdlio_path():
    """Setup PyHDLio core path for testing - uses local PyHDLio directory."""
    current_dir = Path(__file__).parent
    pyhdlio_core_path = current_dir.parent / "PyHDLio"  # Local PyHDLio directory
    hdlio_package_path = pyhdlio_core_path / "hdlio"

    if not pyhdlio_core_path.exists():
        raise ImportError(f"PyHDLio core directory not found at: {pyhdlio_core_path}")

    if not hdlio_package_path.exists():
        raise ImportError(f"hdlio package not found at: {hdlio_package_path}")

    # Add PyHDLio to Python path if not already there
    pyhdlio_str = str(pyhdlio_core_path)
    if pyhdlio_str not in sys.path:
        sys.path.insert(0, pyhdlio_str)

    return pyhdlio_core_path

# Setup the path before importing
setup_pyhdlio_path()
sys.path.insert(0, str(PROJECT_ROOT))

from hdlio import HDLio, VHDL_2008, VHDL_2000, VHDL_2019
from hdlio import VERILOG_1995, VERILOG_2001, VERILOG_2005
from hdlio import SYSTEMVERILOG_2005, SYSTEMVERILOG_2009, SYSTEMVERILOG_2012, SYSTEMVERILOG_2017


@pytest.fixture
def fixtures_dir():
    """Path to test fixtures directory"""
    return TEST_DIR / "fixtures"


@pytest.fixture
def simple_vhdl_file(fixtures_dir):
    """Path to simple VHDL test file"""
    return fixtures_dir / "simple_entity.vhd"


@pytest.fixture
def complex_vhdl_file(fixtures_dir):
    """Path to complex VHDL test file"""
    return fixtures_dir / "test_vhdl.vhd"


@pytest.fixture
def simple_vhdl_content():
    """Simple VHDL entity content for testing"""
    return """entity simple_test is
  port (
    clk : in std_logic;
    reset : in std_logic;
    data : out std_logic
  );
end entity simple_test;"""


@pytest.fixture
def grouped_vhdl_content():
    """VHDL entity with port groups for testing"""
    return """entity grouped_test is
  port (
    -- Clock signals
    clk : in std_logic;
    clk_en : in std_logic;

    -- Reset signals
    reset : in std_logic;
    reset_n : in std_logic;

    -- Data ports
    data_in : in std_logic;
    data_out : out std_logic;
    data_valid : out std_logic
  );
end entity grouped_test;"""


@pytest.fixture
def mixed_grouping_vhdl_content():
    """VHDL entity with mixed grouping patterns"""
    return """entity mixed_test is
  port (
    -- Control group
    enable : in std_logic;
    ready : out std_logic;

    -- Ungrouped port
    status : out std_logic;

    -- Another group
    addr : in std_logic;
    data : inout std_logic
  );
end entity mixed_test;"""


@pytest.fixture
def temp_vhdl_file(tmp_path, simple_vhdl_content):
    """Create a temporary VHDL file for testing"""
    temp_file = tmp_path / "temp_test.vhd"
    temp_file.write_text(simple_vhdl_content)
    return temp_file


@pytest.fixture
def hdlio_parser():
    """HDLio parser instance for VHDL 2008"""
    def _create_parser(filename, language=VHDL_2008):
        return HDLio(filename, language)
    return _create_parser


@pytest.fixture
def verilog_files_dir():
    """Path to Verilog test files directory"""
    return TEST_DIR / "verilog"


@pytest.fixture
def simple_module_file(fixtures_dir):
    """Path to simple_module.v test file"""
    return fixtures_dir / "simple_module.v"


@pytest.fixture
def simple_systemverilog_file(fixtures_dir):
    """Path to simple_systemverilog.sv test file"""
    return fixtures_dir / "simple_systemverilog.sv"


@pytest.fixture
def simple_cpu_file(verilog_files_dir):
    """Path to simple_cpu.v test file (complex, marked as slow)"""
    return verilog_files_dir / "simple_cpu.v"


@pytest.fixture
def ddr_controller_file(verilog_files_dir):
    """Path to ddr_controller.v test file (complex, marked as slow)"""
    return verilog_files_dir / "ddr_controller.v"


@pytest.fixture
def fifo_uvm_test_file(verilog_files_dir):
    """Path to fifo_uvm_test.sv test file (complex, marked as slow)"""
    return verilog_files_dir / "fifo_uvm_test.sv"


@pytest.fixture
def verilog_parser():
    """HDLio parser instance for Verilog 2005"""
    def _create_parser(filename, language=VERILOG_2005):
        return HDLio(filename, language)
    return _create_parser


@pytest.fixture
def systemverilog_parser():
    """HDLio parser instance for SystemVerilog 2012"""
    def _create_parser(filename, language=SYSTEMVERILOG_2012):
        return HDLio(filename, language)
    return _create_parser


@pytest.fixture(scope="session")
def all_vhdl_versions():
    """List of all supported VHDL versions"""
    return [VHDL_2000, VHDL_2008, VHDL_2019]


@pytest.fixture(scope="session")
def all_verilog_versions():
    """List of all supported Verilog versions"""
    return [VERILOG_1995, VERILOG_2001, VERILOG_2005]


@pytest.fixture(scope="session")
def all_systemverilog_versions():
    """List of all supported SystemVerilog versions"""
    return [SYSTEMVERILOG_2005, SYSTEMVERILOG_2009, SYSTEMVERILOG_2012, SYSTEMVERILOG_2017]


def pytest_configure(config):
    """Pytest configuration hook"""
    # Ensure fixtures directory exists
    fixtures_dir = Path(__file__).parent / "fixtures"
    fixtures_dir.mkdir(exist_ok=True)


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their location"""
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

        # Add markers based on test name patterns
        if "port_group" in item.name:
            item.add_marker(pytest.mark.port_groups)
        if "vhdl" in item.name.lower():
            item.add_marker(pytest.mark.vhdl)
        if "verilog" in item.name.lower():
            item.add_marker(pytest.mark.verilog)
        if "systemverilog" in item.name.lower():
            item.add_marker(pytest.mark.systemverilog)
        if "parser" in item.name.lower():
            item.add_marker(pytest.mark.parser)