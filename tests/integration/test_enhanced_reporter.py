"""
Test enhanced reporting functionality with pyVHDLModel VHDL structures
"""

import unittest
import os
import sys

# Add PyHDLio package to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'PyHDLio'))

from pyhdlio.vhdl.model import Document
from tests.utils.reporter import report_pyvhdlmodel_entities, report_entity

# pyVHDLModel imports
from pyVHDLModel.DesignUnit import Entity as PyVHDLModelEntity

class TestEnhancedReporter(unittest.TestCase):
    """Test enhanced reporting functionality using pyVHDLModel objects."""

    def setUp(self):
        """Set up test cases."""
        self.simple_vhdl = os.path.join(
            os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
        )

        # Parse the simple VHDL file using Document API
        if os.path.exists(self.simple_vhdl):
            self.simple_document = Document.from_file(self.simple_vhdl)
            entities = list(self.simple_document.Entities.values())
            self.simple_entity = entities[0] if entities else None
        else:
            self.simple_document = None
            self.simple_entity = None

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_pyvhdlmodel_entity_reporting(self):
        """Test pyVHDLModel entity reporting."""
        report = report_entity(self.simple_entity)

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

    def test_document_entities_reporting(self):
        """Test reporting on all entities in a document."""
        entities = list(self.simple_document.Entities.values())
        report = report_pyvhdlmodel_entities(entities)

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

        document = Document.from_string(minimal_vhdl)
        entities = list(document.Entities.values())
        entity = entities[0]

        report = report_entity(entity)

        # Should handle empty generics and ports gracefully
        self.assertIn("Entity: minimal", report)
        self.assertIn("Generics:", report)
        self.assertIn("None", report)
        self.assertIn("Ports (flat):", report)

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

        document = Document.from_string(complex_vhdl)
        entities = list(document.Entities.values())
        entity = entities[0]

        report = report_entity(entity)

        # Check complex type reporting
        self.assertIn("Entity: complex_types", report)
        self.assertIn("data_bus", report)
        self.assertIn("addr_bus", report)
        self.assertIn("control", report)
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

        document = Document.from_string(vhdl_string)
        entities = list(document.Entities.values())
        entity = entities[0]

        report = report_entity(entity)

        # Check that string parsing produces reportable results
        self.assertIn("Entity: string_entity", report)
        self.assertIn("TEST_PARAM", report)
        self.assertIn("input_sig", report)
        self.assertIn("output_sig", report)

    def test_mixed_design_units_reporting(self):
        """Test reporting on documents with multiple design units."""
        mixed_vhdl = """
        package common_pkg is
            constant DATA_WIDTH : integer := 8;
        end package common_pkg;
        
        entity test_entity is
            generic (
                WIDTH : integer := 16
            );
            port (
                clk : in std_logic;
                data : out std_logic_vector(WIDTH-1 downto 0)
            );
        end entity test_entity;
        """
        
        document = Document.from_string(mixed_vhdl)
        
        # Test entity reporting
        entities = list(document.Entities.values())
        if entities:
            entity_report = report_entity(entities[0])
            self.assertIn("Entity: test_entity", entity_report)
            self.assertIn("WIDTH", entity_report)
            self.assertIn("clk", entity_report)
            self.assertIn("data", entity_report)

    def test_component_in_package_reporting(self):
        """Test that packages with components can be parsed (components not directly reported)."""
        package_vhdl = """
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
            
            constant MAX_VALUE : integer := 255;
        end package test_pkg;
        """
        
        document = Document.from_string(package_vhdl)
        
        # Check that packages were parsed successfully
        packages = list(document.Packages.values())
        self.assertEqual(len(packages), 1)
        self.assertEqual(packages[0].Identifier, "test_pkg")
        
        # Check that package has declarative items
        self.assertGreater(len(packages[0].DeclaredItems), 0)


if __name__ == '__main__':
    unittest.main()