"""
Unit tests for HDLio parser functionality
"""

import pytest
from hdlio import HDLio, VHDL_2008, VHDL_2000, VHDL_2019


class TestVHDLParser:
    """Test VHDL parser functionality"""

    @pytest.mark.parser
    @pytest.mark.vhdl
    def test_simple_entity_parsing(self, temp_vhdl_file, hdlio_parser):
        """Test parsing a simple VHDL entity"""
        hdl = hdlio_parser(str(temp_vhdl_file))
        design_units = hdl.getDesignUnits()
        
        assert len(design_units) == 1
        entity = design_units[0]
        assert entity.getVhdlType() == "entity"
        assert entity.name == "simple_test"

    @pytest.mark.parser
    @pytest.mark.vhdl
    def test_entity_with_ports(self, simple_vhdl_file, hdlio_parser):
        """Test parsing entity with ports"""
        if not simple_vhdl_file.exists():
            pytest.skip("Simple VHDL file not found")
        
        hdl = hdlio_parser(str(simple_vhdl_file))
        design_units = hdl.getDesignUnits()
        
        assert len(design_units) >= 1
        entity = design_units[0]
        
        port_groups = entity.getPortGroups()
        assert len(port_groups) >= 1
        
        # Check that we have some ports
        total_ports = sum(len(group.getPorts()) for group in port_groups)
        assert total_ports >= 1

    @pytest.mark.parser
    @pytest.mark.vhdl
    def test_vhdl_language_versions(self, tmp_path, simple_vhdl_content, all_vhdl_versions):
        """Test parsing with different VHDL language versions"""
        temp_file = tmp_path / "version_test.vhd"
        temp_file.write_text(simple_vhdl_content)
        
        for version in all_vhdl_versions:
            hdl = HDLio(str(temp_file), version)
            design_units = hdl.getDesignUnits()
            
            # Should be able to parse with any version
            assert len(design_units) >= 1

    @pytest.mark.parser
    @pytest.mark.vhdl
    def test_complex_entity_parsing(self, complex_vhdl_file, hdlio_parser):
        """Test parsing a more complex VHDL file"""
        if not complex_vhdl_file.exists():
            pytest.skip("Complex VHDL file not found")
        
        hdl = hdlio_parser(str(complex_vhdl_file))
        design_units = hdl.getDesignUnits()
        
        # Should find at least one design unit
        assert len(design_units) >= 1
        
        # Check for entity
        entities = [unit for unit in design_units if unit.getVhdlType() == "entity"]
        assert len(entities) >= 1

    @pytest.mark.parser
    def test_invalid_file_handling(self, tmp_path, hdlio_parser):
        """Test handling of invalid files"""
        # Test non-existent file
        non_existent = tmp_path / "does_not_exist.vhd"
        
        with pytest.raises((FileNotFoundError, IOError)):
            hdlio_parser(str(non_existent))

    @pytest.mark.parser
    @pytest.mark.vhdl
    def test_malformed_vhdl_handling(self, tmp_path, hdlio_parser):
        """Test handling of malformed VHDL"""
        malformed_vhdl = """entity bad_entity is
          port (
            clk : in std_logic  -- Missing semicolon
            data : out std_logic
          );
        end entity bad_entity;"""
        
        temp_file = tmp_path / "malformed.vhd"
        temp_file.write_text(malformed_vhdl)
        
        # Parser should not crash, but may have parsing errors
        hdl = hdlio_parser(str(temp_file))
        design_units = hdl.getDesignUnits()
        
        # May succeed with partial parsing or fail gracefully
        assert isinstance(design_units, list)

    @pytest.mark.parser
    @pytest.mark.vhdl
    def test_port_direction_parsing(self, tmp_path, hdlio_parser):
        """Test parsing of different port directions"""
        direction_test = """entity direction_test is
          port (
            input_port : in std_logic;
            output_port : out std_logic;
            bidirectional_port : inout std_logic;
            buffer_port : buffer std_logic
          );
        end entity direction_test;"""
        
        temp_file = tmp_path / "direction_test.vhd"
        temp_file.write_text(direction_test)
        
        hdl = hdlio_parser(str(temp_file))
        design_units = hdl.getDesignUnits()
        
        assert len(design_units) >= 1
        entity = design_units[0]
        
        port_groups = entity.getPortGroups()
        all_ports = []
        for group in port_groups:
            all_ports.extend(group.getPorts())
        
        # Should have parsed multiple ports
        assert len(all_ports) >= 2
        
        # Check directions are parsed correctly
        directions = [port.getDirection() for port in all_ports]
        assert any(direction == "in" for direction in directions)
        assert any(direction == "out" for direction in directions)

    @pytest.mark.parser
    @pytest.mark.vhdl
    def test_port_type_parsing(self, tmp_path, hdlio_parser):
        """Test parsing of different port types"""
        type_test = """entity type_test is
          port (
            std_logic_port : in std_logic;
            integer_port : in integer;
            boolean_port : in boolean
          );
        end entity type_test;"""
        
        temp_file = tmp_path / "type_test.vhd"
        temp_file.write_text(type_test)
        
        hdl = hdlio_parser(str(temp_file))
        design_units = hdl.getDesignUnits()
        
        assert len(design_units) >= 1
        entity = design_units[0]
        
        port_groups = entity.getPortGroups()
        all_ports = []
        for group in port_groups:
            all_ports.extend(group.getPorts())
        
        # Should have parsed multiple ports with different types
        assert len(all_ports) >= 2
        
        types = [port.getType() for port in all_ports]
        assert any("std_logic" in port_type for port_type in types)
        assert any("integer" in port_type for port_type in types) 