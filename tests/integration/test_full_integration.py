"""
Full integration tests for the VHDL parsing and modeling pipeline
"""

import unittest
import os
import sys

# Add PyHDLio package to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'PyHDLio'))

from pyhdlio.vhdl.model import VHDLAST, Document, VHDLSyntaxError
from utils.reporter import report_entities

# Try to import pyVHDLModel for extended tests
try:
    from pyVHDLModel.DesignUnit import Entity as PyVHDLModelEntity
    from pyVHDLModel.Interface import GenericConstantInterfaceItem, PortSignalInterfaceItem
    PYVHDLMODEL_AVAILABLE = True
except ImportError:
    PyVHDLModelEntity = None
    GenericConstantInterfaceItem = None
    PortSignalInterfaceItem = None
    PYVHDLMODEL_AVAILABLE = False


class TestFullIntegration(unittest.TestCase):
    """Full integration tests for VHDL processing pipeline."""

    def setUp(self):
        """Set up test fixtures."""
        self.simple_vhdl = os.path.join(
            os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
        )

    def test_basic_parsing_pipeline(self):
        """Test basic VHDL parsing pipeline."""
        # Parse using new consolidated API
        module = VHDLAST.from_file(self.simple_vhdl)

        # Verify basic structure
        self.assertIsInstance(module, VHDLAST)
        self.assertEqual(len(module.entities), 1)

        entity = module.entities[0]
        self.assertEqual(entity.name, "counter")
        self.assertGreater(len(entity.generics), 0)
        self.assertGreater(len(entity.ports), 0)

    def test_string_parsing(self):
        """Test parsing VHDL from string."""
        vhdl_code = """
        entity test_string is
          generic (
            SIZE : natural := 8
          );
          port (
            clk : in std_logic;
            data : out std_logic_vector(SIZE-1 downto 0)
          );
        end entity;
        """

        module = VHDLAST.from_string(vhdl_code)
        self.assertEqual(len(module.entities), 1)
        self.assertEqual(module.entities[0].name, "test_string")

    @unittest.skipUnless(PYVHDLMODEL_AVAILABLE, "pyVHDLModel not available")
    def test_pyvhdlmodel_conversion_pipeline(self):
        """Test complete pipeline from VHDL file to pyVHDLModel."""
        # Parse to AST
        module = VHDLAST.from_file(self.simple_vhdl)

        # Convert to pyVHDLModel using new API
        document = Document.from_ast(module)

        # Verify conversion
        self.assertEqual(len(document.Entities), 1)
        entity = list(document.Entities.values())[0]
        self.assertIsInstance(entity, PyVHDLModelEntity)
        self.assertEqual(entity.Identifier, "counter")

    @unittest.skipUnless(PYVHDLMODEL_AVAILABLE, "pyVHDLModel not available")
    def test_document_api_pipeline(self):
        """Test new Document API pipeline."""
        # Parse directly to Document
        document = Document.from_file(self.simple_vhdl)

        # Verify structure
        self.assertEqual(len(document.Entities), 1)
        entity = list(document.Entities.values())[0]
        self.assertEqual(entity.Identifier, "counter")

    def test_reporting_pipeline(self):
        """Test reporting functionality with parsed entities."""
        module = VHDLAST.from_file(self.simple_vhdl)

        # Generate report
        report = report_entities(module)

        # Verify report content
        self.assertIn("Entity: counter", report)
        self.assertIn("Generics:", report)
        self.assertIn("Ports (flat):", report)
        self.assertIn("Ports (grouped):", report)

    def test_error_handling_pipeline(self):
        """Test error handling throughout the pipeline."""
        # Test file not found
        with self.assertRaises(FileNotFoundError):
            VHDLAST.from_file("nonexistent.vhd")

        # Test syntax error
        invalid_vhdl = "entity bad_syntax is port ( clk in std_logic invalid_syntax ); end entity;"
        with self.assertRaises(VHDLSyntaxError):
            VHDLAST.from_string(invalid_vhdl)

    @unittest.skipUnless(PYVHDLMODEL_AVAILABLE, "pyVHDLModel not available")
    def test_ast_to_document_conversion(self):
        """Test AST to Document conversion pipeline."""
        # Parse to AST first
        ast = VHDLAST.from_file(self.simple_vhdl)

        # Convert AST to Document using from_ast
        document = Document.from_ast(ast)

        # Verify conversion
        self.assertEqual(len(document.Entities), 1)
        entity = list(document.Entities.values())[0]
        self.assertEqual(entity.Identifier, "counter")

    def test_generics_and_ports_extraction(self):
        """Test detailed extraction of generics and ports."""
        module = VHDLAST.from_file(self.simple_vhdl)
        entity = module.entities[0]

        # Test generics
        self.assertEqual(len(entity.generics), 2)
        generic_names = [g.name for g in entity.generics]
        self.assertIn("WIDTH", generic_names)
        self.assertIn("DEPTH", generic_names)

        # Test ports
        self.assertEqual(len(entity.ports), 4)
        port_names = [p.name for p in entity.ports]
        self.assertIn("clk", port_names)
        self.assertIn("reset", port_names)
        self.assertIn("start", port_names)
        self.assertIn("count", port_names)

    def test_port_grouping_functionality(self):
        """Test port grouping preservation through pipeline."""
        module = VHDLAST.from_file(self.simple_vhdl)
        entity = module.entities[0]

        # Verify port groups exist
        self.assertGreater(len(entity.port_groups), 0)

        # Verify groups contain correct ports
        total_grouped_ports = sum(len(group.ports) for group in entity.port_groups)
        self.assertEqual(total_grouped_ports, len(entity.ports))

    def test_filename_attribution(self):
        """Test that filename is properly attributed to parsed AST."""
        module = VHDLAST.from_file(self.simple_vhdl)

        # Check filename attribution
        self.assertTrue(hasattr(module, 'filename'))
        self.assertTrue(module.filename.endswith('simple.vhd'))


if __name__ == '__main__':
    unittest.main()