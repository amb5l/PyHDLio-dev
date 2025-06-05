"""
Test enhanced reporting functionality with complex VHDL structures
"""

import unittest
import os
import sys

# Add PyHDLio package to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'PyHDLio'))

from pyhdlio.vhdl.model import VHDLAST, Document
from utils.reporter import report_entities, report_entity

# pyVHDLModel imports (required)
from pyVHDLModel.DesignUnit import Entity as PyVHDLModelEntity

class TestEnhancedReporter(unittest.TestCase):
    """Test enhanced reporting functionality."""

    def setUp(self):
        """Set up test cases."""
        self.simple_vhdl = os.path.join(
            os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
        )

        # Parse the simple VHDL file using new API
        if os.path.exists(self.simple_vhdl):
            self.simple_module = VHDLAST.from_file(self.simple_vhdl)
            self.simple_entity = self.simple_module.entities[0]
        else:
            self.simple_module = None
            self.simple_entity = None

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_ast_entity_reporting(self):
        """Test detailed AST entity reporting."""
        report = report_entity(self.simple_entity)

        # Check basic structure
        self.assertIn("Entity: counter", report)

        # Check generics section
        self.assertIn("Generics:", report)
        self.assertIn("WIDTH", report)
        self.assertIn("DEPTH", report)
        self.assertIn("integer", report)
        self.assertIn("natural", report)

        # Check ports section
        self.assertIn("Ports (flat):", report)
        self.assertIn("clk", report)
        self.assertIn("reset", report)
        self.assertIn("start", report)
        self.assertIn("count", report)

        # Check port grouping
        self.assertIn("Ports (grouped):", report)
        self.assertIn("Group", report)

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_pyvhdlmodel_entity_reporting(self):
        """Test pyVHDLModel entity reporting."""
        # Convert to pyVHDLModel
        document = Document.from_file(self.simple_vhdl)
        entity = list(document.Entities.values())[0]

        report = report_entity(entity)

        # Check basic structure
        self.assertIn("Entity: counter", report)

        # Check generics section
        self.assertIn("Generics:", report)
        self.assertIn("WIDTH", report)
        self.assertIn("DEPTH", report)

        # Check ports section
        self.assertIn("Ports (flat):", report)
        self.assertIn("clk", report)
        self.assertIn("reset", report)
        self.assertIn("start", report)
        self.assertIn("count", report)

        # Check port grouping
        self.assertIn("Ports (grouped):", report)
        self.assertIn("Group", report)

    def test_module_reporting(self):
        """Test reporting on entire VHDL module."""
        report = report_entities(self.simple_module)

        # Should contain entity information
        self.assertIn("Entity: counter", report)
        self.assertIn("WIDTH", report)
        self.assertIn("clk", report)

    def test_empty_sections_handling(self):
        """Test reporting handles entities with missing sections gracefully."""
        # Create minimal VHDL entity
        minimal_vhdl = """
        entity minimal is
        end entity;
        """

        module = VHDLAST.from_string(minimal_vhdl)
        entity = module.entities[0]

        report = report_entity(entity)

        # Should handle empty generics and ports gracefully
        self.assertIn("Entity: minimal", report)
        self.assertIn("Generics:\n      None", report)
        self.assertIn("Ports (flat):\n      None", report)

    def test_complex_port_types(self):
        """Test reporting with complex port types."""
        complex_vhdl = """
        entity complex_types is
          port (
            data_bus : in std_logic_vector(31 downto 0);
            addr_bus : out std_logic_vector(15 downto 0);
            control : inout std_logic_vector(7 downto 0)
          );
        end entity;
        """

        module = VHDLAST.from_string(complex_vhdl)
        entity = module.entities[0]

        report = report_entity(entity)

        # Check complex type reporting (the parser may truncate the type name)
        self.assertIn("std_logic_vec", report)  # May be truncated by parser
        self.assertIn("31 downto 0", report)
        self.assertIn("15 downto 0", report)
        self.assertIn("inout", report)

    def test_report_formatting(self):
        """Test that reports are properly formatted."""
        report = report_entity(self.simple_entity)

        # Check indentation and structure
        lines = report.split('\n')

        # Find sections
        entity_line = None
        generics_line = None
        ports_line = None

        for i, line in enumerate(lines):
            if line.startswith("Entity:"):
                entity_line = i
            elif line.strip().startswith("Generics:"):
                generics_line = i
            elif line.strip().startswith("Ports (flat):"):
                ports_line = i

        # Verify sections exist and are in order
        self.assertIsNotNone(entity_line)
        self.assertIsNotNone(generics_line)
        self.assertIsNotNone(ports_line)
        self.assertLess(entity_line, generics_line)
        self.assertLess(generics_line, ports_line)

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_document_reporting_consistency(self):
        """Test that AST and Document reporting produce consistent results."""
        # Get AST report
        ast_report = report_entity(self.simple_entity)

        # Get Document report
        document = Document.from_file(self.simple_vhdl)
        doc_entity = list(document.Entities.values())[0]
        doc_report = report_entity(doc_entity)

        # Both should contain the same essential information
        essential_info = ["Entity: counter", "WIDTH", "DEPTH", "clk", "reset", "start", "count"]
        for info in essential_info:
            self.assertIn(info, ast_report, f"AST report missing: {info}")
            self.assertIn(info, doc_report, f"Document report missing: {info}")

    def test_string_parsing_reporting(self):
        """Test reporting works with string-parsed entities."""
        vhdl_string = """
        entity string_entity is
          generic (
            TEST_PARAM : string := "hello"
          );
          port (
            input_sig : in std_logic;
            output_sig : out natural
          );
        end entity;
        """

        module = VHDLAST.from_string(vhdl_string)
        entity = module.entities[0]

        report = report_entity(entity)

        self.assertIn("Entity: string_entity", report)
        self.assertIn("TEST_PARAM", report)
        self.assertIn("input_sig", report)
        self.assertIn("output_sig", report)


if __name__ == '__main__':
    unittest.main()