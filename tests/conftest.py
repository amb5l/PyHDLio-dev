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

from hdlio import HDLio, VHDL_1993, VHDL_2008, VHDL_2000, VHDL_2019
from hdlio import Verilog_1995, Verilog_2001, Verilog_2005
from hdlio import SystemVerilog_2005, SystemVerilog_2009, SystemVerilog_2012, SystemVerilog_2017


@pytest.fixture(scope="session")
def fixtures_dir():
    """Path to test fixtures directory"""
    return TEST_DIR / "fixtures"


@pytest.fixture(scope="session")
def lrm_fixtures_dir(fixtures_dir):
    """Path to LRM (Language Reference Manual) test fixtures directory"""
    return fixtures_dir / "lrm"


# VHDL Language Version Specific Fixtures
@pytest.fixture(scope="session")
def vhdl_1993_file(lrm_fixtures_dir):
    """Path to VHDL-1993 language version specific test file"""
    return lrm_fixtures_dir / "vhdl_1993.vhd"


@pytest.fixture(scope="session")
def vhdl_2000_file(lrm_fixtures_dir):
    """Path to VHDL-2000 language version specific test file"""
    return lrm_fixtures_dir / "vhdl_2000.vhd"


@pytest.fixture(scope="session")
def vhdl_2008_file(lrm_fixtures_dir):
    """Path to VHDL-2008 language version specific test file"""
    return lrm_fixtures_dir / "vhdl_2008.vhd"


@pytest.fixture(scope="session")
def vhdl_2019_file(lrm_fixtures_dir):
    """Path to VHDL-2019 language version specific test file"""
    return lrm_fixtures_dir / "vhdl_2019.vhd"


# Verilog Language Version Specific Fixtures
@pytest.fixture(scope="session")
def verilog_1995_file(lrm_fixtures_dir):
    """Path to Verilog-1995 language version specific test file"""
    return lrm_fixtures_dir / "verilog_1995.v"


@pytest.fixture(scope="session")
def verilog_2001_file(lrm_fixtures_dir):
    """Path to Verilog-2001 language version specific test file"""
    return lrm_fixtures_dir / "verilog_2001.v"


@pytest.fixture(scope="session")
def verilog_2005_file(lrm_fixtures_dir):
    """Path to Verilog-2005 language version specific test file"""
    return lrm_fixtures_dir / "verilog_2005.v"


# SystemVerilog Language Version Specific Fixtures
@pytest.fixture(scope="session")
def systemverilog_2005_file(lrm_fixtures_dir):
    """Path to SystemVerilog-2005 language version specific test file"""
    return lrm_fixtures_dir / "systemverilog_2005.sv"


@pytest.fixture(scope="session")
def systemverilog_2009_file(lrm_fixtures_dir):
    """Path to SystemVerilog-2009 language version specific test file"""
    return lrm_fixtures_dir / "systemverilog_2009.sv"


@pytest.fixture(scope="session")
def systemverilog_2012_file(lrm_fixtures_dir):
    """Path to SystemVerilog-2012 language version specific test file"""
    return lrm_fixtures_dir / "systemverilog_2012.sv"


@pytest.fixture(scope="session")
def systemverilog_2017_file(lrm_fixtures_dir):
    """Path to SystemVerilog-2017 language version specific test file"""
    return lrm_fixtures_dir / "systemverilog_2017.sv"


# Combined fixtures for all language versions
@pytest.fixture(scope="session")
def all_vhdl_version_files(lrm_fixtures_dir):
    """Dictionary mapping VHDL versions to their fixture files"""
    return {
        VHDL_1993: lrm_fixtures_dir / "vhdl_1993.vhd",
        VHDL_2000: lrm_fixtures_dir / "vhdl_2000.vhd",
        VHDL_2008: lrm_fixtures_dir / "vhdl_2008.vhd",
        VHDL_2019: lrm_fixtures_dir / "vhdl_2019.vhd"
    }


@pytest.fixture(scope="session")
def all_verilog_version_files(lrm_fixtures_dir):
    """Dictionary mapping Verilog versions to their fixture files"""
    return {
        Verilog_1995: lrm_fixtures_dir / "verilog_1995.v",
        Verilog_2001: lrm_fixtures_dir / "verilog_2001.v",
        Verilog_2005: lrm_fixtures_dir / "verilog_2005.v"
    }


@pytest.fixture(scope="session")
def all_systemverilog_version_files(lrm_fixtures_dir):
    """Dictionary mapping SystemVerilog versions to their fixture files"""
    return {
        SystemVerilog_2005: lrm_fixtures_dir / "systemverilog_2005.sv",
        SystemVerilog_2009: lrm_fixtures_dir / "systemverilog_2009.sv",
        SystemVerilog_2012: lrm_fixtures_dir / "systemverilog_2012.sv",
        SystemVerilog_2017: lrm_fixtures_dir / "systemverilog_2017.sv"
    }


@pytest.fixture(scope="session")
def all_language_version_files(all_vhdl_version_files, all_verilog_version_files, all_systemverilog_version_files):
    """List of all language version fixture files"""
    all_files = []
    all_files.extend(all_vhdl_version_files.values())
    all_files.extend(all_verilog_version_files.values())
    all_files.extend(all_systemverilog_version_files.values())
    return all_files


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
        from hdlio import HDLio, HDL_LRM
        from hdlio.core.constants import VHDL_1993 as CONST_VHDL_1993, VHDL_2000 as CONST_VHDL_2000, VHDL_2008 as CONST_VHDL_2008, VHDL_2019 as CONST_VHDL_2019
        
        # Map old language constants to new HDL_LRM enum
        language_map = {
            CONST_VHDL_1993: HDL_LRM.VHDL_1993,
            CONST_VHDL_2000: HDL_LRM.VHDL_2000,
            CONST_VHDL_2008: HDL_LRM.VHDL_2008,
            CONST_VHDL_2019: HDL_LRM.VHDL_2019
        }
        
        hdl_lrm = language_map.get(language, HDL_LRM.VHDL_2008)
        
        hdlio = HDLio()
        source_path = hdlio.load(filename, "work", hdl_lrm)
        if source_path is None:
            raise FileNotFoundError(f"Failed to load file: {filename}")
        return hdlio
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
    def _create_parser(filename, language=Verilog_2005):
        # For now, Verilog support is not implemented in the new API
        # This will need to be updated when Verilog support is added
        raise NotImplementedError("Verilog support not yet implemented in new API")
    return _create_parser


@pytest.fixture
def systemverilog_parser():
    """HDLio parser instance for SystemVerilog 2012"""
    def _create_parser(filename, language=SystemVerilog_2012):
        # For now, SystemVerilog support is not implemented in the new API
        # This will need to be updated when SystemVerilog support is added
        raise NotImplementedError("SystemVerilog support not yet implemented in new API")
    return _create_parser


@pytest.fixture(scope="session")
def all_vhdl_versions():
    """List of all supported VHDL versions"""
    return [VHDL_1993, VHDL_2000, VHDL_2008, VHDL_2019]


@pytest.fixture(scope="session")
def all_verilog_versions():
    """List of all supported Verilog versions"""
    return [Verilog_1995, Verilog_2001, Verilog_2005]


@pytest.fixture(scope="session")
def all_systemverilog_versions():
    """List of all supported SystemVerilog versions"""
    return [SystemVerilog_2005, SystemVerilog_2009, SystemVerilog_2012, SystemVerilog_2017]


def pytest_configure(config):
    """Pytest configuration hook"""
    # Ensure fixtures directory exists
    fixtures_dir = Path(__file__).parent / "fixtures"
    fixtures_dir.mkdir(exist_ok=True)


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their location"""
    # Ensure all marks are registered
    marks_to_register = [
        "unit: Unit tests",
        "integration: Integration tests", 
        "parser: Parser tests",
        "port_groups: Port grouping tests",
        "vhdl: VHDL-specific tests",
        "verilog: Verilog-specific tests", 
        "systemverilog: SystemVerilog-specific tests"
    ]
    
    for mark_def in marks_to_register:
        try:
            config.addinivalue_line("markers", mark_def)
        except ValueError:
            # Mark already registered
            pass
    
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