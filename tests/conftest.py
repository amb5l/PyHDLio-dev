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
        if "parser" in item.name.lower():
            item.add_marker(pytest.mark.parser) 