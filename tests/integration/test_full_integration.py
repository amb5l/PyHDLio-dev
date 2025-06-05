"""
Full integration tests for the VHDL parsing and modeling pipeline using pyVHDLModel
"""

import unittest
import os
import sys

# Add PyHDLio package to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'PyHDLio'))

# Add tests directory to path for utility imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyhdlio.vhdl.model import Document, VHDLSyntaxError
import pyVHDLModel
from utils.reporter import report_pyvhdlmodel_entities


class TestFullIntegration(unittest.TestCase):
    """Full integration tests for VHDL processing pipeline using pyVHDLModel objects."""

    def setUp(self):
        """Set up test fixtures."""
        self.simple_vhdl = os.path.join(
            os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl_in', 'sample.vhd'
        )

    def test_basic_parsing_pipeline(self):
        """Test basic VHDL parsing pipeline returning pyVHDLModel Document."""
        # Parse using Document API directly
        document = Document.FromFile(self.simple_vhdl)

        # Verify basic structure
        self.assertIsInstance(document, pyVHDLModel.Document)
        entities = list(document.Entities.values())
        self.assertEqual(len(entities), 2)

        # Use the processor entity which is more complex
        processor_entity = entities[1]
        self.assertEqual(processor_entity.Identifier, "processor")
        self.assertEqual(len(processor_entity.GenericItems), 4)
        self.assertEqual(len(processor_entity.PortItems), 15)

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

        document = Document.FromStr(vhdl_code)
        entities = list(document.Entities.values())
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].Identifier, "test_string")

    def test_document_api_pipeline(self):
        """Test Document API pipeline."""
        # Parse directly to Document
        document = Document.FromFile(self.simple_vhdl)

        # Verify structure
        entities = list(document.Entities.values())
        self.assertEqual(len(entities), 2)  # simple_gate and processor
        # Find simple_gate entity
        simple_gate = next((e for e in entities if e.Identifier == "simple_gate"), None)
        self.assertIsNotNone(simple_gate)

    def test_reporting_pipeline(self):
        """Test reporting functionality with parsed entities."""
        document = Document.FromFile(self.simple_vhdl)
        entities = list(document.Entities.values())

        # Generate report
        report = report_pyvhdlmodel_entities(entities)

        # Verify report content
        self.assertIn("Entity: processor", report)
        self.assertIn("Generics:", report)
        self.assertIn("DATA_WIDTH", report)
        self.assertIn("Ports (flat):", report)
        self.assertIn("Ports (grouped):", report)

    def test_error_handling_pipeline(self):
        """Test error handling throughout the pipeline."""
        # Test file not found
        with self.assertRaises(FileNotFoundError):
            Document.FromFile("nonexistent.vhd")

        # Test syntax error
        invalid_vhdl = "entity bad_syntax is port ( clk in std_logic invalid_syntax ); end entity;"
        with self.assertRaises(VHDLSyntaxError):
            Document.FromStr(invalid_vhdl)

    def test_generics_and_ports_extraction(self):
        """Test detailed extraction of generics and ports."""
        document = Document.FromFile(self.simple_vhdl)
        entities = list(document.Entities.values())
        processor_entity = entities[1]  # Use processor entity

        # Test generics
        self.assertEqual(len(processor_entity.GenericItems), 4)
        generic_names = [g.Identifiers[0] for g in processor_entity.GenericItems]
        self.assertIn("DATA_WIDTH", generic_names)
        self.assertIn("ADDR_WIDTH", generic_names)
        self.assertIn("CACHE_SIZE", generic_names)
        self.assertIn("ENABLE_CACHE", generic_names)

        # Test ports
        self.assertEqual(len(processor_entity.PortItems), 15)
        port_names = [p.Identifiers[0] for p in processor_entity.PortItems]
        self.assertIn("clk", port_names)
        self.assertIn("reset", port_names)
        self.assertIn("inst_addr", port_names)
        self.assertIn("data_addr", port_names)

    def test_port_grouping_functionality(self):
        """Test port grouping preservation through pipeline."""
        document = Document.FromFile(self.simple_vhdl)
        entities = list(document.Entities.values())
        processor_entity = entities[1]  # Use processor entity

        # Verify port groups exist if any
        if hasattr(processor_entity, 'PortGroups') and processor_entity.PortGroups:
            self.assertGreater(len(processor_entity.PortGroups), 0)
            # Verify groups contain correct port items
            total_grouped_ports = sum(len(group.PortItems) for group in processor_entity.PortGroups)
            self.assertEqual(total_grouped_ports, len(processor_entity.PortItems))

    def test_package_parsing(self):
        """Test parsing VHDL packages with components."""
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
        
            constant MAX_WIDTH : integer := 32;
        end package test_pkg;
        """
        
        document = Document.FromStr(vhdl_code)
        
        # Check packages
        packages = list(document.Packages.values())
        self.assertEqual(len(packages), 1)
        self.assertEqual(packages[0].Identifier, "test_pkg")
        
        # Check that package has declarative items
        self.assertGreater(len(packages[0].DeclaredItems), 0)

    def test_mixed_design_unit_parsing(self):
        """Test parsing VHDL files with both packages and entities."""
        vhdl_code = """
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
        
        document = Document.FromStr(vhdl_code)
        
        # Check both packages and entities
        packages = list(document.Packages.values())
        entities = list(document.Entities.values())
        
        self.assertEqual(len(packages), 1)
        self.assertEqual(len(entities), 1)
        
        self.assertEqual(packages[0].Identifier, "common_pkg")
        self.assertEqual(entities[0].Identifier, "test_entity")


if __name__ == '__main__':
    unittest.main()