"""
Comprehensive tests for Enhanced Reporter with Function Overloads
"""

import unittest
import os
import sys

# Add PyHDLio package to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'PyHDLio'))

from hdlio.vhdl.parse_vhdl import parse_vhdl
from hdlio.vhdl.converters.pyvhdlmodel_converter import convert_to_pyvhdlmodel
from hdlio.vhdl.reporter import (
    report_entity, report_generics, report_ports_flat, report_ports_grouped,
    report_entities, report_pyvhdlmodel_entities
)

# pyVHDLModel imports
try:
    from pyVHDLModel.DesignUnit import Entity as PyVHDLModelEntity
    PYVHDLMODEL_AVAILABLE = True
except ImportError:
    PYVHDLMODEL_AVAILABLE = False


class TestEnhancedReporter(unittest.TestCase):
    """Test enhanced reporter with function overloads."""

    def setUp(self):
        """Set up test fixtures."""
        self.simple_vhdl = os.path.join(
            os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
        )

        if os.path.exists(self.simple_vhdl):
            # Parse AST
            self.simple_module = parse_vhdl(self.simple_vhdl, mode='ast')
            self.ast_entity = self.simple_module.entities[0]

            # Convert to pyVHDLModel if available
            if PYVHDLMODEL_AVAILABLE:
                self.pyvhdlmodel_entities = convert_to_pyvhdlmodel(self.simple_module)
                self.model_entity = self.pyvhdlmodel_entities[0]
            else:
                self.pyvhdlmodel_entities = None
                self.model_entity = None
        else:
            self.simple_module = None
            self.ast_entity = None
            self.pyvhdlmodel_entities = None
            self.model_entity = None

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_ast_reporter_functions(self):
        """Test reporter functions work correctly with AST entities."""
        # Test entity report
        entity_report = report_entity(self.ast_entity)
        self.assertIn("Entity: counter", entity_report)
        self.assertIn("WIDTH", entity_report)
        self.assertIn("DEPTH", entity_report)
        self.assertIn("clk", entity_report)
        self.assertIn("Group 1:", entity_report)
        self.assertIn("Group 2:", entity_report)

        # Test generics report
        generics_report = report_generics(self.ast_entity)
        self.assertIn("Generics:", generics_report)
        self.assertIn("WIDTH: integer = 8", generics_report)
        self.assertIn("DEPTH: natural = 16", generics_report)

        # Test ports flat report
        ports_flat_report = report_ports_flat(self.ast_entity)
        self.assertIn("Ports (flat):", ports_flat_report)
        self.assertIn("clk: in STD_LOGIC", ports_flat_report)
        self.assertIn("count: out STD_LOGIC_VECTOR", ports_flat_report)

        # Test ports grouped report
        ports_grouped_report = report_ports_grouped(self.ast_entity)
        self.assertIn("Ports (grouped):", ports_grouped_report)
        self.assertIn("Group 1:", ports_grouped_report)
        self.assertIn("Group 2:", ports_grouped_report)

    @unittest.skipUnless(PYVHDLMODEL_AVAILABLE and os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "pyVHDLModel not available or Simple VHDL file not found")
    def test_pyvhdlmodel_reporter_functions(self):
        """Test reporter functions work correctly with pyVHDLModel entities."""
        # Test entity report
        entity_report = report_entity(self.model_entity)
        self.assertIn("Entity: counter", entity_report)
        self.assertIn("WIDTH", entity_report)
        self.assertIn("DEPTH", entity_report)
        self.assertIn("clk", entity_report)
        self.assertIn("Group 1:", entity_report)
        self.assertIn("Group 2:", entity_report)

        # Test generics report
        generics_report = report_generics(self.model_entity)
        self.assertIn("Generics:", generics_report)
        self.assertIn("WIDTH", generics_report)
        self.assertIn("DEPTH", generics_report)
        self.assertIn("= 8", generics_report)
        self.assertIn("= 16", generics_report)

        # Test ports flat report
        ports_flat_report = report_ports_flat(self.model_entity)
        self.assertIn("Ports (flat):", ports_flat_report)
        self.assertIn("clk: in", ports_flat_report)
        self.assertIn("count: out", ports_flat_report)

        # Test ports grouped report
        ports_grouped_report = report_ports_grouped(self.model_entity)
        self.assertIn("Ports (grouped):", ports_grouped_report)
        self.assertIn("Group 1:", ports_grouped_report)
        self.assertIn("Group 2:", ports_grouped_report)

    @unittest.skipUnless(PYVHDLMODEL_AVAILABLE and os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "pyVHDLModel not available or Simple VHDL file not found")
    def test_function_overload_dispatch(self):
        """Test that function overloads dispatch to correct implementations."""
        # Get reports from both approaches
        ast_report = report_entity(self.ast_entity)
        model_report = report_entity(self.model_entity)

        # Both should contain entity information
        self.assertIn("Entity: counter", ast_report)
        self.assertIn("Entity: counter", model_report)

        # Both should have generics and ports
        self.assertIn("WIDTH", ast_report)
        self.assertIn("WIDTH", model_report)
        self.assertIn("clk", ast_report)
        self.assertIn("clk", model_report)

        # Both should preserve port grouping
        self.assertIn("Group 1:", ast_report)
        self.assertIn("Group 1:", model_report)
        self.assertIn("Group 2:", ast_report)
        self.assertIn("Group 2:", model_report)

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_module_reporting(self):
        """Test module-level reporting functions."""
        # Test AST module reporting
        module_report = report_entities(self.simple_module)
        self.assertIn("Entity: counter", module_report)
        self.assertNotIn("No entities found", module_report)

    @unittest.skipUnless(PYVHDLMODEL_AVAILABLE and os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "pyVHDLModel not available or Simple VHDL file not found")
    def test_pyvhdlmodel_entities_reporting(self):
        """Test pyVHDLModel entities reporting function."""
        entities_report = report_pyvhdlmodel_entities(self.pyvhdlmodel_entities)
        self.assertIn("Entity: counter", entities_report)
        self.assertNotIn("No entities found", entities_report)

    def test_empty_entities_handling(self):
        """Test handling of empty entity lists."""
        # Test empty AST module
        from hdlio.vhdl.ast.ast import VHDLAST
        empty_module = VHDLAST(entities=[])
        report = report_entities(empty_module)
        self.assertIn("No entities found", report)

    @unittest.skipUnless(PYVHDLMODEL_AVAILABLE, "pyVHDLModel not available")
    def test_empty_pyvhdlmodel_entities_handling(self):
        """Test handling of empty pyVHDLModel entity lists."""
        empty_report = report_pyvhdlmodel_entities([])
        self.assertIn("No entities found", empty_report)

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_port_grouping_consistency(self):
        """Test that port grouping is consistent between AST and pyVHDLModel reports."""
        ast_grouped = report_ports_grouped(self.ast_entity)

        if PYVHDLMODEL_AVAILABLE:
            model_grouped = report_ports_grouped(self.model_entity)

            # Both should have the same number of groups
            ast_group_count = ast_grouped.count("Group ")
            model_group_count = model_grouped.count("Group ")
            self.assertEqual(ast_group_count, model_group_count)

            # Both should mention the same ports
            self.assertIn("clk", ast_grouped)
            self.assertIn("clk", model_grouped)
            self.assertIn("reset", ast_grouped)
            self.assertIn("reset", model_grouped)
            self.assertIn("start", ast_grouped)
            self.assertIn("start", model_grouped)
            self.assertIn("count", ast_grouped)
            self.assertIn("count", model_grouped)

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_indentation_consistency(self):
        """Test that indentation is consistent across reports."""
        entity_report = report_entity(self.ast_entity)

        # Check that proper indentation is used
        lines = entity_report.split('\n')

        # Entity name should be at root level
        entity_line = [line for line in lines if "Entity: counter" in line][0]
        self.assertFalse(entity_line.startswith(' '))

        # Generics/Ports headers should be indented
        generics_line = [line for line in lines if "Generics:" in line][0]
        self.assertTrue(generics_line.startswith('  '))

        # Individual items should be further indented
        width_lines = [line for line in lines if "WIDTH" in line]
        if width_lines:
            self.assertTrue(width_lines[0].startswith('    '))

    def test_reporter_error_handling(self):
        """Test reporter error handling with invalid inputs."""
        from hdlio.vhdl.ast.ast import Entity

        # Test with entity that has no generics or ports
        empty_entity = Entity("empty", [], [], [])

        report = report_entity(empty_entity)
        self.assertIn("Entity: empty", report)
        self.assertIn("None", report)  # Should show "None" for empty sections

    @unittest.skipUnless(PYVHDLMODEL_AVAILABLE and os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "pyVHDLModel not available or Simple VHDL file not found")
    def test_type_detection_accuracy(self):
        """Test that the reporter correctly detects and dispatches object types."""
        from hdlio.vhdl.ast.ast import Entity as PyHDLioEntity

        # Verify our test entities are of correct types
        self.assertIsInstance(self.ast_entity, PyHDLioEntity)
        self.assertIsInstance(self.model_entity, PyVHDLModelEntity)

        # Both should produce reports but potentially with different content
        ast_report = report_entity(self.ast_entity)
        model_report = report_entity(self.model_entity)

        # Both should be non-empty strings
        self.assertIsInstance(ast_report, str)
        self.assertIsInstance(model_report, str)
        self.assertTrue(len(ast_report) > 0)
        self.assertTrue(len(model_report) > 0)


if __name__ == '__main__':
    unittest.main()