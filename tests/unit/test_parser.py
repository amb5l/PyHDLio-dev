"""
Unit tests for HDL parsers
"""

import pytest
from hdlio import HDLio, HDL_LRM


class TestVHDLParser:
    """Test VHDL parser functionality"""

    @pytest.mark.unit
    @pytest.mark.vhdl
    def test_simple_entity_parsing(self, tmp_path):
        """Test parsing a simple VHDL entity"""
        vhdl_content = """
entity test_entity is
    port (
        clk : in std_logic;
        data : out std_logic
    );
end entity test_entity;
        """

        temp_file = tmp_path / "test_entity.vhd"
        temp_file.write_text(vhdl_content)

        hdlio = HDLio()
        source_path = hdlio.load(str(temp_file), "work", HDL_LRM.VHDL_2008)
        assert source_path is not None
        
        design_units = hdlio.get_design_units("work")
        assert len(design_units) >= 1

        entity = design_units[0]
        assert entity.name == "test_entity"
        assert entity.get_vhdl_type() == "entity"

    @pytest.mark.unit
    @pytest.mark.vhdl
    def test_entity_with_architecture(self, tmp_path):
        """Test parsing entity with architecture"""
        vhdl_content = """
entity counter is
    port (
        clk : in std_logic;
        count : out integer
    );
end entity counter;

architecture behavioral of counter is
begin
    -- Simple counter implementation
end architecture behavioral;
        """

        temp_file = tmp_path / "counter.vhd"
        temp_file.write_text(vhdl_content)

        hdlio = HDLio()
        source_path = hdlio.load(str(temp_file), "work", HDL_LRM.VHDL_2008)
        assert source_path is not None
        
        design_units = hdlio.get_design_units("work")
        assert len(design_units) >= 2  # Entity + Architecture

        # Map old version strings to new HDL_LRM enum
        from hdlio.core.constants import VHDL_1993, VHDL_2000, VHDL_2008, VHDL_2019
        version_map = {
            VHDL_1993: HDL_LRM.VHDL_1993,
            VHDL_2000: HDL_LRM.VHDL_2000,
            VHDL_2008: HDL_LRM.VHDL_2008,
            VHDL_2019: HDL_LRM.VHDL_2019
        }

        # Find entity and architecture
        entity = next((unit for unit in design_units if unit.get_vhdl_type() == "entity"), None)
        architecture = next((unit for unit in design_units if unit.get_vhdl_type() == "architecture"), None)

        assert entity is not None
        assert architecture is not None
        assert entity.name == "counter"
        assert architecture.name == "behavioral"

    @pytest.mark.unit
    @pytest.mark.vhdl
    def test_package_parsing(self, tmp_path):
        """Test parsing VHDL package"""
        vhdl_content = """
package test_package is
    constant WIDTH : integer := 8;
end package test_package;
        """

        temp_file = tmp_path / "test_package.vhd"
        temp_file.write_text(vhdl_content)

        hdlio = HDLio()
        source_path = hdlio.load(str(temp_file), "work", HDL_LRM.VHDL_2008)
        assert source_path is not None
        
        design_units = hdlio.get_design_units("work")
        assert len(design_units) >= 1

        package = design_units[0]
        assert package.name == "test_package"
        assert package.get_vhdl_type() == "package"

    @pytest.mark.unit
    @pytest.mark.vhdl
    def test_multiple_design_units(self, tmp_path):
        """Test parsing multiple design units in one file"""
        vhdl_content = """
package utils is
    constant MAX_COUNT : integer := 255;
end package utils;

entity multi_unit is
    port (
        input : in std_logic;
        output : out std_logic
    );
end entity multi_unit;

architecture simple of multi_unit is
begin
    output <= input;
end architecture simple;
        """

        temp_file = tmp_path / "multi_unit.vhd"
        temp_file.write_text(vhdl_content)

        hdlio = HDLio()
        source_path = hdlio.load(str(temp_file), "work", HDL_LRM.VHDL_2008)
        assert source_path is not None
        
        design_units = hdlio.get_design_units("work")
        assert len(design_units) >= 3  # Package + Entity + Architecture

        # Check that we have the expected types
        unit_types = [unit.get_vhdl_type() for unit in design_units]
        assert "package" in unit_types
        assert "entity" in unit_types
        assert "architecture" in unit_types

    @pytest.mark.unit
    @pytest.mark.vhdl
    def test_library_management(self, tmp_path):
        """Test library management functionality"""
        vhdl_content1 = """
entity lib1_entity is
    port (clk : in std_logic);
end entity lib1_entity;
        """

        vhdl_content2 = """
entity lib2_entity is
    port (data : out std_logic);
end entity lib2_entity;
        """

        temp_file1 = tmp_path / "lib1.vhd"
        temp_file1.write_text(vhdl_content1)

        temp_file2 = tmp_path / "lib2.vhd"
        temp_file2.write_text(vhdl_content2)

        hdlio = HDLio()
        
        # Load into different libraries
        source1 = hdlio.load(str(temp_file1), "lib1", HDL_LRM.VHDL_2008)
        source2 = hdlio.load(str(temp_file2), "lib2", HDL_LRM.VHDL_2008)
        
        assert source1 is not None
        assert source2 is not None

        # Check library separation
        lib1_units = hdlio.get_design_units("lib1")
        lib2_units = hdlio.get_design_units("lib2")

        assert len(lib1_units) == 1
        assert len(lib2_units) == 1
        assert lib1_units[0].name == "lib1_entity"
        assert lib2_units[0].name == "lib2_entity"

        # Check library listing
        libraries = hdlio.get_libraries()
        assert "lib1" in libraries
        assert "lib2" in libraries

    @pytest.mark.unit
    @pytest.mark.vhdl
    def test_error_handling(self, tmp_path):
        """Test error handling for invalid files"""
        # Test non-existent file
        hdlio = HDLio()
        source_path = hdlio.load("non_existent_file.vhd", "work", HDL_LRM.VHDL_2008)
        assert source_path is None

        # Test invalid VHDL syntax
        invalid_vhdl = """
        this is not valid VHDL syntax at all
        """

        temp_file = tmp_path / "invalid.vhd"
        temp_file.write_text(invalid_vhdl)

        source_path = hdlio.load(str(temp_file), "work", HDL_LRM.VHDL_2008)
        # Should return None for parse errors
        assert source_path is None

    @pytest.mark.unit
    @pytest.mark.vhdl
    def test_source_tracking(self, tmp_path):
        """Test that design units track their source files"""
        vhdl_content = """
entity source_test is
    port (clk : in std_logic);
end entity source_test;
        """

        temp_file = tmp_path / "source_test.vhd"
        temp_file.write_text(vhdl_content)

        hdlio = HDLio()
        source_path = hdlio.load(str(temp_file), "work", HDL_LRM.VHDL_2008)
        assert source_path is not None
        
        design_units = hdlio.get_design_units("work")
        assert len(design_units) >= 1

        entity = design_units[0]
        assert entity.get_source() is not None
        assert str(temp_file) in entity.get_source()


class TestVerilogParser:
    """Test Verilog parser functionality (placeholder for future implementation)"""

    @pytest.mark.unit
    @pytest.mark.verilog
    @pytest.mark.skip(reason="Verilog parser not yet implemented in new API")
    def test_simple_module_parsing(self):
        """Test parsing a simple Verilog module"""
        # This will be implemented when Verilog support is added to the new API
        pass