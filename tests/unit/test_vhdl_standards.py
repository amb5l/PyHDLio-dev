"""
Unit tests for VHDL language standards support
"""

import pytest
from hdlio import HDLio, VHDL_1993, VHDL_2000, VHDL_2008, VHDL_2019


class TestVHDLStandards:
    """Test VHDL language standards support with unified parser"""

    @pytest.mark.unit
    @pytest.mark.vhdl
    @pytest.mark.parametrize("vhdl_version", [VHDL_1993, VHDL_2000, VHDL_2008, VHDL_2019])
    def test_vhdl_version_constants(self, vhdl_version):
        """Test that all VHDL version constants are properly defined"""
        assert vhdl_version is not None
        assert isinstance(vhdl_version, str)
        assert 'vhdl' in vhdl_version.lower()

    @pytest.mark.unit
    @pytest.mark.vhdl
    @pytest.mark.parametrize("vhdl_version", [VHDL_1993, VHDL_2000, VHDL_2008, VHDL_2019])
    def test_simple_entity_parsing_all_versions(self, tmp_path, vhdl_version):
        """Test parsing a simple entity with all VHDL versions using unified parser"""
        # Simple VHDL entity that should work in all versions
        vhdl_content = """
library ieee;
use ieee.std_logic_1164.all;

entity simple_entity is
    port (
        clk : in std_logic;
        rst : in std_logic;
        data_in : in std_logic_vector(7 downto 0);
        data_out : out std_logic_vector(7 downto 0)
    );
end entity simple_entity;

architecture behavioral of simple_entity is
begin
    process(clk, rst)
    begin
        if rst = '1' then
            data_out <= (others => '0');
        elsif rising_edge(clk) then
            data_out <= data_in;
        end if;
    end process;
end architecture behavioral;
        """

        temp_file = tmp_path / f"simple_entity_{vhdl_version}.vhd"
        temp_file.write_text(vhdl_content)

        # Test with both comprehensive modes
        for comprehensive in [False, True]:
            hdl = HDLio(str(temp_file), vhdl_version, comprehensive=comprehensive)
            design_units = hdl.get_design_units()

            # Should parse successfully
            assert len(design_units) >= 1

            # Should find the entity
            entity = None
            for unit in design_units:
                if unit.get_vhdl_type() == "entity":
                    entity = unit
                    break

            assert entity is not None
            assert entity.name == "simple_entity"

            # Check ports
            if hasattr(entity, 'get_port_groups'):
                port_groups = entity.get_port_groups()
                total_ports = sum(len(group.get_ports()) for group in port_groups)
                assert total_ports >= 3  # Should have at least some ports parsed

    @pytest.mark.unit
    @pytest.mark.vhdl
    def test_unified_parser_consistency(self, tmp_path):
        """Test that all VHDL versions use the same unified parser"""
        vhdl_content = """
entity test_entity is
    port (clk : in std_logic);
end entity;
        """

        temp_file = tmp_path / "test_consistency.vhd"
        temp_file.write_text(vhdl_content)

        # All versions should produce consistent results
        results = []
        for version in [VHDL_1993, VHDL_2000, VHDL_2008, VHDL_2019]:
            hdl = HDLio(str(temp_file), version)
            design_units = hdl.get_design_units()
            results.append(len(design_units))

        # All versions should have the same number of design units
        assert all(r == results[0] for r in results), "Inconsistent parsing across VHDL versions"

    @pytest.mark.unit
    @pytest.mark.vhdl
    def test_complex_entity_all_versions(self, tmp_path):
        """Test parsing a more complex entity with all VHDL versions"""
        vhdl_content = """
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity complex_entity is
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
end entity complex_entity;

architecture rtl of complex_entity is
    signal reg_data : std_logic_vector(WIDTH-1 downto 0);
    type state_type is (IDLE, ACTIVE, DONE);
    signal state : state_type;
begin

    process(clk, reset_n)
    begin
        if reset_n = '0' then
            reg_data <= (others => '0');
            state <= IDLE;
        elsif rising_edge(clk) then
            case state is
                when IDLE =>
                    if valid = '1' then
                        reg_data <= data_in;
                        state <= ACTIVE;
                    end if;
                when ACTIVE =>
                    state <= DONE;
                when DONE =>
                    state <= IDLE;
            end case;
        end if;
    end process;

    data_out <= reg_data;
    ready <= '1' when state = DONE else '0';

end architecture rtl;
        """

        for vhdl_version in [VHDL_1993, VHDL_2000, VHDL_2008, VHDL_2019]:
            temp_file = tmp_path / f"complex_entity_{vhdl_version}.vhd"
            temp_file.write_text(vhdl_content)

            hdl = HDLio(str(temp_file), vhdl_version)
            design_units = hdl.get_design_units()

            # Should parse successfully
            assert len(design_units) >= 1

            # Find entity and verify port groups
            entity = next((unit for unit in design_units if unit.get_vhdl_type() == "entity"), None)
            assert entity is not None
            assert entity.name == "complex_entity"

            # Check port grouping functionality
            if hasattr(entity, 'get_port_groups'):
                port_groups = entity.get_port_groups()
                group_names = [group.get_name() for group in port_groups]

                # Should identify comment-based groups
                assert len(port_groups) >= 2
                # Should find our comment groups
                assert any("Clock" in name for name in group_names)
                assert any("Data" in name for name in group_names)