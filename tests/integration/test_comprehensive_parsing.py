#!/usr/bin/env python3
"""
Comprehensive parsing tests for HDLio library
Consolidates functionality from various root-level test scripts
"""

import pytest
import tempfile
import os
from pathlib import Path

from hdlio import HDLio, VHDL_2008, VHDL_2000, VHDL_2019, VHDL_1993


@pytest.mark.integration
@pytest.mark.parser
class TestComprehensiveParsing:
    """Test comprehensive VHDL parsing scenarios"""

    def test_simple_entity_parsing(self):
        """Test parsing a simple VHDL entity with port groups"""
        vhdl_content = """library ieee;
use ieee.std_logic_1164.all;

entity test_entity is
    port (
        -- Clock and reset signals
        clk : in std_logic;
        reset : in std_logic;

        -- Data signals
        data_in : in std_logic_vector(7 downto 0);
        data_out : out std_logic_vector(7 downto 0);
        valid : out std_logic
    );
end entity test_entity;

architecture rtl of test_entity is
begin
    process(clk, reset)
    begin
        if reset = '1' then
            data_out <= (others => '0');
            valid <= '0';
        elsif rising_edge(clk) then
            data_out <= data_in;
            valid <= '1';
        end if;
    end process;
end architecture rtl;
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.vhd', delete=False) as f:
            f.write(vhdl_content)
            f.flush()

            try:
                hdl = HDLio(f.name, VHDL_2008)
                design_units = hdl.get_design_units()

                assert len(design_units) >= 1, "Should parse at least one design unit"

                entity = design_units[0]
                assert entity.get_vhdl_type() == 'entity', "First unit should be entity"
                assert entity.name == 'test_entity', "Entity name should match"

                groups = entity.get_port_groups()
                assert len(groups) >= 2, "Should find at least 2 port groups"

                # Check for expected group names
                group_names = [g.get_name() for g in groups]
                assert any("Clock" in name for name in group_names), "Should find Clock group"
                assert any("Data" in name for name in group_names), "Should find Data group"

                # Count total ports
                total_ports = sum(len(group.get_ports()) for group in groups)
                assert total_ports == 5, "Should find 5 total ports"

            finally:
                os.unlink(f.name)

    def test_entity_only_parsing(self):
        """Test parsing entity-only VHDL files"""
        vhdl_content = """entity test_entity is
    port (
        -- Clock and reset signals
        clk : in std_logic;
        reset : in std_logic;

        -- Data signals
        data_in : in std_logic_vector;
        data_out : out std_logic_vector;
        valid : out std_logic
    );
end entity test_entity;
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.vhd', delete=False) as f:
            f.write(vhdl_content)
            f.flush()

            try:
                hdl = HDLio(f.name, VHDL_2008)
                design_units = hdl.get_design_units()

                assert len(design_units) == 1, "Should parse exactly one design unit"

                entity = design_units[0]
                assert entity.get_vhdl_type() == 'entity', "Should be entity type"

                groups = entity.get_port_groups()
                assert len(groups) >= 2, "Should find port groups"

                # Verify port grouping based on comments
                group_names = [g.get_name() for g in groups]
                assert any("Clock" in name for name in group_names), "Should find Clock group"
                assert any("Data" in name for name in group_names), "Should find Data group"

            finally:
                os.unlink(f.name)

    def test_multi_group_entity(self):
        """Test entity with multiple comment-based port groups"""
        vhdl_content = """entity multi_group_entity is
    port (
        -- System Signals
        clk : in std_logic;
        reset_n : in std_logic;
        enable : in std_logic;

        -- Input Bus
        addr_in : in std_logic_vector(31 downto 0);
        data_in : in std_logic_vector(31 downto 0);
        write_en : in std_logic;
        read_en : in std_logic;

        -- Output Bus
        data_out : out std_logic_vector(31 downto 0);
        ready : out std_logic;
        error : out std_logic;

        -- Debug Interface
        debug_addr : out std_logic_vector(15 downto 0);
        debug_data : out std_logic_vector(7 downto 0)
    );
end entity multi_group_entity;
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.vhd', delete=False) as f:
            f.write(vhdl_content)
            f.flush()

            try:
                hdl = HDLio(f.name, VHDL_2008)
                design_units = hdl.get_design_units()

                entity = design_units[0]
                groups = entity.get_port_groups()

                expected_groups = ["System Signals", "Input Bus", "Output Bus", "Debug Interface"]
                group_names = [g.get_name() for g in groups]

                for expected in expected_groups:
                    assert expected in group_names, f"Should find group: {expected}"

            finally:
                os.unlink(f.name)

    def test_no_comments_entity(self):
        """Test entity without comments (default grouping)"""
        vhdl_content = """entity no_comments_entity is
    port (
        clk : in std_logic;
        data_in : in std_logic_vector(7 downto 0);
        data_out : out std_logic_vector(7 downto 0);
        enable : in std_logic;
        ready : out std_logic
    );
end entity no_comments_entity;
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.vhd', delete=False) as f:
            f.write(vhdl_content)
            f.flush()

            try:
                hdl = HDLio(f.name, VHDL_2008)
                design_units = hdl.get_design_units()

                entity = design_units[0]
                groups = entity.get_port_groups()

                # Should create at least one group (default)
                assert len(groups) >= 1, "Should create at least one port group"

                total_ports = sum(len(group.get_ports()) for group in groups)
                assert total_ports == 5, "Should find all 5 ports"

            finally:
                os.unlink(f.name)

    @pytest.mark.parametrize("vhdl_version", [VHDL_1993, VHDL_2000, VHDL_2008, VHDL_2019])
    def test_vhdl_version_support(self, vhdl_version):
        """Test that all VHDL versions are supported"""
        vhdl_content = """library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity version_test is
    generic (
        WIDTH : integer := 8;
        DEPTH : positive := 16
    );
    port (
        -- Clock and Reset
        clk     : in  std_logic;
        reset_n : in  std_logic;

        -- Data Interface
        data_in  : in  std_logic_vector(WIDTH-1 downto 0);
        data_out : out std_logic_vector(WIDTH-1 downto 0);
        valid    : in  std_logic;
        ready    : out std_logic
    );
end entity version_test;
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.vhd', delete=False) as f:
            f.write(vhdl_content)
            f.flush()

            try:
                hdl = HDLio(f.name, vhdl_version)
                design_units = hdl.get_design_units()

                assert len(design_units) >= 1, f"Should parse with {vhdl_version}"

                entity = design_units[0]
                assert entity.get_vhdl_type() == 'entity', "Should parse entity"

                groups = entity.get_port_groups()
                assert len(groups) >= 2, "Should find port groups"

            finally:
                os.unlink(f.name)

    def test_comprehensive_cpu_core(self):
        """Test parsing a comprehensive CPU core entity"""
        vhdl_content = """library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity cpu_core is
    generic (
        DATA_WIDTH : integer := 32;
        ADDR_WIDTH : integer := 32
    );
    port (
        -- Clock and Reset
        clk : in std_logic;
        reset_n : in std_logic;

        -- Instruction Interface
        instr_addr : out std_logic_vector(ADDR_WIDTH-1 downto 0);
        instr_data : in std_logic_vector(DATA_WIDTH-1 downto 0);
        instr_valid : in std_logic;

        -- Data Interface
        data_addr : out std_logic_vector(ADDR_WIDTH-1 downto 0);
        data_write : out std_logic_vector(DATA_WIDTH-1 downto 0);
        data_read : in std_logic_vector(DATA_WIDTH-1 downto 0);
        data_we : out std_logic;
        data_re : out std_logic;

        -- Control Signals
        interrupt : in std_logic;
        halt : out std_logic
    );
end entity cpu_core;

architecture behavioral of cpu_core is
    type cpu_state_t is (IDLE, FETCH, DECODE, EXECUTE, WRITEBACK);
    signal current_state : cpu_state_t := IDLE;
begin
    -- Simple state machine
    process(clk, reset_n)
    begin
        if reset_n = '0' then
            current_state <= IDLE;
        elsif rising_edge(clk) then
            case current_state is
                when IDLE => current_state <= FETCH;
                when FETCH => current_state <= DECODE;
                when DECODE => current_state <= EXECUTE;
                when EXECUTE => current_state <= WRITEBACK;
                when WRITEBACK => current_state <= IDLE;
            end case;
        end if;
    end process;
end architecture behavioral;
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.vhd', delete=False) as f:
            f.write(vhdl_content)
            f.flush()

            try:
                # Test both entity-focused and comprehensive modes
                for comprehensive in [False, True]:
                    hdl = HDLio(f.name, VHDL_2008, comprehensive=comprehensive)
                    design_units = hdl.get_design_units()

                    assert len(design_units) >= 1, f"Should parse design units (comprehensive={comprehensive})"

                    entity = design_units[0]
                    assert entity.get_vhdl_type() == 'entity', "First unit should be entity"

                    groups = entity.get_port_groups()
                    expected_groups = ["Clock and Reset", "Instruction Interface", "Data Interface", "Control Signals"]
                    group_names = [g.get_name() for g in groups]

                    for expected in expected_groups:
                        assert expected in group_names, f"Should find group: {expected}"

                    # Count total ports
                    total_ports = sum(len(group.get_ports()) for group in groups)
                    assert total_ports == 11, "Should find 11 total ports"

            finally:
                os.unlink(f.name)

    def test_parser_info(self):
        """Test that parser info is available"""
        vhdl_content = """entity simple is
    port (clk : in std_logic);
end entity simple;
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.vhd', delete=False) as f:
            f.write(vhdl_content)
            f.flush()

            try:
                hdl = HDLio(f.name, VHDL_2008)
                parser_info = hdl.get_parser_info()

                assert 'parser_type' in parser_info, "Should have parser_type info"
                assert 'comprehensive' in parser_info, "Should have comprehensive mode info"

            finally:
                os.unlink(f.name)


@pytest.mark.integration
@pytest.mark.parser
class TestUnifiedParser:
    """Test unified VHDL parser functionality"""

    def test_unified_parser_all_versions(self):
        """Test that the unified parser works for all VHDL versions"""
        vhdl_content = """library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity test_entity is
    generic (
        WIDTH : integer := 8;
        DEPTH : positive := 16
    );
    port (
        -- Clock and Reset
        clk     : in  std_logic;
        reset_n : in  std_logic;

        -- Data Interface
        data_in  : in  std_logic_vector(WIDTH-1 downto 0);
        data_out : out std_logic_vector(WIDTH-1 downto 0);
        valid    : in  std_logic;
        ready    : out std_logic
    );
end entity test_entity;
"""

        vhdl_versions = [VHDL_1993, VHDL_2000, VHDL_2008, VHDL_2019]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.vhd', delete=False) as f:
            f.write(vhdl_content)
            f.flush()

            try:
                for version in vhdl_versions:
                    # Test both comprehensive modes
                    for comprehensive in [False, True]:
                        hdl = HDLio(f.name, version, comprehensive=comprehensive)
                        design_units = hdl.get_design_units()

                        assert len(design_units) >= 1, f"Should parse with {version} (comprehensive={comprehensive})"

                        entity = design_units[0]
                        groups = entity.get_port_groups()

                        # Verify port group names
                        group_names = [group.get_name() for group in groups]
                        assert "Clock and Reset" in group_names, f"Should find Clock group in {version}"
                        assert "Data Interface" in group_names, f"Should find Data group in {version}"

                        # Count total ports
                        total_ports = sum(len(group.get_ports()) for group in groups)
                        assert total_ports == 6, f"Should find 6 ports in {version}"

            finally:
                os.unlink(f.name)