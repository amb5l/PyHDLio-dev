import pytest
import os
from PyHDLio.pyhdlio.vhdl.model import VHDLAST, VHDLSyntaxError
from PyHDLio.pyhdlio.vhdl import Entity
from utils.reporter import report_entities


class TestVHDLParser:
    """Unit tests for VHDL parser functionality."""

    def setup_method(self):
        """Setup common paths for all tests."""
        self.fixture_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fixtures', 'vhdl')
        self.life_signs_path = os.path.join(self.fixture_dir, 'life_signs.vhd')
        self.entity_with_ports_path = os.path.join(self.fixture_dir, 'entity_with_ports.vhd')

    def test_parse_life_signs_vhdl_ast(self):
        """Test parsing the life_signs.vhd fixture returns VHDLAST."""
        result = VHDLAST.from_file(self.life_signs_path)
        
        # Check that result is a VHDLAST
        assert isinstance(result, VHDLAST)
        
    def test_entity_reporting(self):
        """Test entity reporting functionality."""
        result = VHDLAST.from_file(self.life_signs_path)
        
        # Test reporting
        report = report_entities(result)
        assert "Entity: life_signs" in report
        assert "Generics:" in report
        assert "Ports (flat):" in report
        assert "Ports (grouped):" in report
        assert "None" in report  # Since this entity has no generics or ports

    def test_entity_with_ports_and_generics(self):
        """Test parsing entity with ports and generics."""
        result = VHDLAST.from_file(self.entity_with_ports_path)
        assert len(result.entities) == 1

        entity = result.entities[0]
        assert entity.name == "test_entity"

        # Check generics - now extraction is implemented
        assert len(entity.generics) == 2
        generic_names = [g.name for g in entity.generics]
        assert "WIDTH" in generic_names
        assert "DEPTH" in generic_names
        
        # Verify generic details
        width_generic = next(g for g in entity.generics if g.name == "WIDTH")
        assert width_generic.type == "integer"
        assert width_generic.default_value == "8"
        
        depth_generic = next(g for g in entity.generics if g.name == "DEPTH")
        assert depth_generic.type == "natural"
        assert depth_generic.default_value == "16"

        # Check ports - now extraction is implemented
        assert len(entity.ports) == 3
        port_names = [p.name for p in entity.ports]
        assert "clk" in port_names
        assert "reset" in port_names
        assert "data" in port_names
        
        # Verify port details
        clk_port = next(p for p in entity.ports if p.name == "clk")
        assert clk_port.direction == "in"
        assert clk_port.type == "STD_LOGIC"
        
        reset_port = next(p for p in entity.ports if p.name == "reset")
        assert reset_port.direction == "in"
        assert reset_port.type == "STD_LOGIC"
        
        data_port = next(p for p in entity.ports if p.name == "data")
        assert data_port.direction == "out"
        assert "STD_LOGIC_VECTOR" in data_port.type
        
    def test_parse_nonexistent_file(self):
        """Test that parsing a non-existent file raises appropriate exception."""
        non_existent_path = os.path.join(self.fixture_dir, 'does_not_exist.vhd')
        
        with pytest.raises(FileNotFoundError) as exc_info:
            VHDLAST.from_file(non_existent_path)
        
        assert 'VHDL file not found' in str(exc_info.value)
        assert 'does_not_exist.vhd' in str(exc_info.value)
        
    def test_parse_vhdl_file_path_handling(self):
        """Test that the parser handles file paths correctly."""
        # Test with absolute path 
        abs_path = os.path.abspath(self.life_signs_path)
        result = VHDLAST.from_file(abs_path)
        assert isinstance(result, VHDLAST)
        assert len(result.entities) > 0
        assert result.entities[0].name == "life_signs"
        
        # Test with relative path
        # Change to fixture directory and use relative path
        original_cwd = os.getcwd()
        try:
            os.chdir(self.fixture_dir)
            result = VHDLAST.from_file('life_signs.vhd')
            assert isinstance(result, VHDLAST)
            assert len(result.entities) > 0
            assert result.entities[0].name == "life_signs"
        finally:
            os.chdir(original_cwd)

    def test_string_parsing(self):
        """Test parsing VHDL code from string."""
        vhdl_code = """
        entity test_string_entity is
          generic (
            SIZE : natural := 8
          );
          port (
            clk : in std_logic;
            data : out std_logic_vector(SIZE-1 downto 0)
          );
        end entity;
        """
        
        result = VHDLAST.from_string(vhdl_code)
        assert isinstance(result, VHDLAST)
        assert len(result.entities) == 1
        assert result.entities[0].name == "test_string_entity"
        assert len(result.entities[0].generics) == 1
        assert len(result.entities[0].ports) == 2

    def test_syntax_error_handling(self):
        """Test that syntax errors are properly handled."""
        invalid_vhdl = """
        entity bad_syntax is
          port (
            clk : in std_logic  -- Missing semicolon
            reset : in std_logic
          );
        end entity;
        """
        
        with pytest.raises(VHDLSyntaxError) as exc_info:
            VHDLAST.from_string(invalid_vhdl)
        
        assert "Syntax error" in str(exc_info.value)