import pytest
import os
from PyHDLio.pyhdlio.vhdl.model import Document, VHDLSyntaxError
import pyVHDLModel
from tests.utils.reporter import report_pyvhdlmodel_entities


class TestVHDLParser:
    """Unit tests for VHDL parser functionality using pyVHDLModel objects."""

    def setup_method(self):
        """Setup common paths for all tests."""
        self.fixture_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fixtures', 'vhdl')
        self.life_signs_path = os.path.join(self.fixture_dir, 'life_signs.vhd')
        self.entity_with_ports_path = os.path.join(self.fixture_dir, 'entity_with_ports.vhd')

    def test_parse_life_signs_vhdl_document(self):
        """Test parsing the life_signs.vhd fixture returns pyVHDLModel Document."""
        result = Document.FromFile(self.life_signs_path)
        
        # Check that result is a pyVHDLModel Document
        assert isinstance(result, pyVHDLModel.Document)
        
    def test_entity_reporting(self):
        """Test entity reporting functionality with pyVHDLModel entities."""
        result = Document.FromFile(self.life_signs_path)
        
        # Get entities from Document
        entities = list(result.Entities.values())
        
        # Test reporting
        report = report_pyvhdlmodel_entities(entities)
        assert "Entity: life_signs" in report
        assert "Generics:" in report
        assert "Ports (flat):" in report
        assert "Ports (grouped):" in report
        assert "None" in report  # Since this entity has no generics or ports

    def test_entity_with_ports_and_generics(self):
        """Test parsing entity with ports and generics using pyVHDLModel objects."""
        result = Document.FromFile(self.entity_with_ports_path)
        
        # Get entities from Document
        entities = list(result.Entities.values())
        assert len(entities) == 1

        entity = entities[0]
        assert entity.Identifier == "test_entity"

        # Check generics - pyVHDLModel structure
        assert len(entity.GenericItems) == 2
        generic_names = [g.Identifiers[0] for g in entity.GenericItems]
        assert "WIDTH" in generic_names
        assert "DEPTH" in generic_names
        
        # Verify generic details
        width_generic = next(g for g in entity.GenericItems if g.Identifiers[0] == "WIDTH")
        assert "integer" in str(width_generic.Subtype).lower()
        assert width_generic.DefaultExpression is not None
        
        depth_generic = next(g for g in entity.GenericItems if g.Identifiers[0] == "DEPTH")
        assert "natural" in str(depth_generic.Subtype).lower()
        assert depth_generic.DefaultExpression is not None

        # Check ports - pyVHDLModel structure
        assert len(entity.PortItems) == 3
        port_names = [p.Identifiers[0] for p in entity.PortItems]
        assert "clk" in port_names
        assert "reset" in port_names
        assert "data" in port_names
        
        # Verify port details
        clk_port = next(p for p in entity.PortItems if p.Identifiers[0] == "clk")
        assert clk_port.Mode == pyVHDLModel.Mode.In
        assert "std_logic" in str(clk_port.Subtype).lower()
        
        reset_port = next(p for p in entity.PortItems if p.Identifiers[0] == "reset")
        assert reset_port.Mode == pyVHDLModel.Mode.In
        assert "std_logic" in str(reset_port.Subtype).lower()
        
        data_port = next(p for p in entity.PortItems if p.Identifiers[0] == "data")
        assert data_port.Mode == pyVHDLModel.Mode.Out
        assert "std_logic_vector" in str(data_port.Subtype).lower()
        
    def test_parse_nonexistent_file(self):
        """Test that parsing a non-existent file raises appropriate exception."""
        non_existent_path = os.path.join(self.fixture_dir, 'does_not_exist.vhd')
        
        with pytest.raises(FileNotFoundError) as exc_info:
            Document.FromFile(non_existent_path)
        
        assert 'VHDL file not found' in str(exc_info.value)
        assert 'does_not_exist.vhd' in str(exc_info.value)
        
    def test_parse_vhdl_file_path_handling(self):
        """Test that the parser handles file paths correctly."""
        # Test with absolute path 
        abs_path = os.path.abspath(self.life_signs_path)
        result = Document.FromFile(abs_path)
        assert isinstance(result, pyVHDLModel.Document)
        entities = list(result.Entities.values())
        assert len(entities) > 0
        assert entities[0].Identifier == "life_signs"
        
        # Test with relative path
        # Change to fixture directory and use relative path
        original_cwd = os.getcwd()
        try:
            os.chdir(self.fixture_dir)
            result = Document.FromFile('life_signs.vhd')
            assert isinstance(result, pyVHDLModel.Document)
            entities = list(result.Entities.values())
            assert len(entities) > 0
            assert entities[0].Identifier == "life_signs"
        finally:
            os.chdir(original_cwd)

    def test_string_parsing(self):
        """Test parsing VHDL code from string using pyVHDLModel objects."""
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
        
        result = Document.FromStr(vhdl_code)
        assert isinstance(result, pyVHDLModel.Document)
        
        entities = list(result.Entities.values())
        assert len(entities) == 1
        assert entities[0].Identifier == "test_string_entity"
        assert len(entities[0].GenericItems) == 1
        assert len(entities[0].PortItems) == 2

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
            Document.FromStr(invalid_vhdl)
        
        assert "Syntax error" in str(exc_info.value)

    def test_package_parsing(self):
        """Test parsing packages with components using pyVHDLModel objects."""
        vhdl_code = """
        package test_pkg is
            component adder is
                generic (
                    WIDTH : integer := 8
                );
                port (
                    a, b : in std_logic_vector(WIDTH-1 downto 0);
                    sum : out std_logic_vector(WIDTH-1 downto 0)
                );
            end component adder;
        end package test_pkg;
        """
        
        result = Document.FromStr(vhdl_code)
        assert isinstance(result, pyVHDLModel.Document)
        
        # Check packages
        packages = list(result.Packages.values())
        assert len(packages) == 1
        assert packages[0].Identifier == "test_pkg"
        
        # Check that package has declarative items (components)
        assert len(packages[0].DeclaredItems) > 0