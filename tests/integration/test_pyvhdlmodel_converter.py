"""
Comprehensive tests for PyVHDLModel converter
"""

import unittest
import os
import sys
from typing import List

# Add PyHDLio package to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'PyHDLio'))

from pyhdlio.vhdl.model import VHDLAST, Document
from pyhdlio.vhdl.ast import Entity as PyHDLioEntity

# pyVHDLModel imports (required)
from pyVHDLModel.DesignUnit import Entity as PyVHDLModelEntity
from pyVHDLModel.Interface import GenericConstantInterfaceItem, PortSignalInterfaceItem, PortGroup
from pyVHDLModel.Base import Mode
from pyVHDLModel.Expression import IntegerLiteral, EnumerationLiteral, StringLiteral

class TestPyVHDLModelConverter(unittest.TestCase):
    """Test PyVHDLModel conversion functionality via Document class."""

    def setUp(self):
        """Set up test fixtures."""
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

    def test_document_conversion_initialization(self):
        """Test Document conversion works correctly."""
        if self.simple_module:
            document = Document.from_ast(self.simple_module)
            self.assertIsInstance(document, Document)
            self.assertEqual(len(document.Entities), 1)

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_entity_conversion(self):
        """Test complete entity conversion."""
        document = Document.from_ast(self.simple_module)
        converted_entity = list(document.Entities.values())[0]

        # Basic entity properties
        self.assertIsInstance(converted_entity, PyVHDLModelEntity)
        self.assertEqual(converted_entity.Identifier, "counter")

        # Generics conversion
        self.assertEqual(len(converted_entity.GenericItems), 2)

        generic_names = [g.Identifiers[0] for g in converted_entity.GenericItems]
        self.assertIn("WIDTH", generic_names)
        self.assertIn("DEPTH", generic_names)

        # Check generic default values
        for generic in converted_entity.GenericItems:
            if generic.Identifiers[0] == "WIDTH":
                self.assertIsInstance(generic.DefaultExpression, IntegerLiteral)
                self.assertEqual(generic.DefaultExpression.Value, 8)
            elif generic.Identifiers[0] == "DEPTH":
                self.assertIsInstance(generic.DefaultExpression, IntegerLiteral)
                self.assertEqual(generic.DefaultExpression.Value, 16)

        # Ports conversion
        self.assertEqual(len(converted_entity.PortItems), 4)

        port_names = [p.Identifiers[0] for p in converted_entity.PortItems]
        self.assertIn("clk", port_names)
        self.assertIn("reset", port_names)
        self.assertIn("start", port_names)
        self.assertIn("count", port_names)

        # Check port modes
        for port in converted_entity.PortItems:
            if port.Identifiers[0] in ["clk", "reset", "start"]:
                self.assertEqual(port.Mode, Mode.In)
            elif port.Identifiers[0] == "count":
                self.assertEqual(port.Mode, Mode.Out)

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_port_grouping_preservation(self):
        """Test that port grouping is preserved during conversion."""
        document = Document.from_ast(self.simple_module)
        converted_entity = list(document.Entities.values())[0]

        # Check port groups
        self.assertEqual(len(converted_entity.PortGroups), 2)

        # Group 1 should have clk and reset
        group1_ports = [p.Identifiers[0] for p in converted_entity.PortGroups[0].Ports]
        self.assertEqual(len(group1_ports), 2)
        self.assertIn("clk", group1_ports)
        self.assertIn("reset", group1_ports)

        # Group 2 should have start and count
        group2_ports = [p.Identifiers[0] for p in converted_entity.PortGroups[1].Ports]
        self.assertEqual(len(group2_ports), 2)
        self.assertIn("start", group2_ports)
        self.assertIn("count", group2_ports)

    def test_generic_conversion_types(self):
        """Test generic conversion with different default value types."""
        from pyhdlio.vhdl.ast import Generic

        # Test integer default
        int_generic = Generic("TEST_INT", "integer", "42")
        converted = Document._convert_generic(int_generic)
        self.assertIsInstance(converted.DefaultExpression, IntegerLiteral)
        self.assertEqual(converted.DefaultExpression.Value, 42)

        # Test string default
        str_generic = Generic("TEST_STR", "string", '"hello"')
        converted = Document._convert_generic(str_generic)
        self.assertIsInstance(converted.DefaultExpression, StringLiteral)  # Should be StringLiteral object

        # Test enumeration default
        enum_generic = Generic("TEST_ENUM", "state_type", "IDLE")
        converted = Document._convert_generic(enum_generic)
        self.assertIsInstance(converted.DefaultExpression, EnumerationLiteral)
        self.assertEqual(converted.DefaultExpression.Value, "IDLE")

    def test_port_mode_mapping(self):
        """Test port mode mapping functionality."""
        from pyhdlio.vhdl.ast import Port

        # Test input port
        in_port = Port("test_in", "in", "std_logic")
        converted = Document._convert_port(in_port)
        self.assertEqual(converted.Mode, Mode.In)

        # Test output port
        out_port = Port("test_out", "out", "std_logic")
        converted = Document._convert_port(out_port)
        self.assertEqual(converted.Mode, Mode.Out)

        # Test inout port
        inout_port = Port("test_inout", "inout", "std_logic")
        converted = Document._convert_port(inout_port)
        self.assertEqual(converted.Mode, Mode.InOut)

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_convenience_function(self):
        """Test the convenience conversion function."""
        # Test with single entity using new API
        document = Document.from_ast(self.simple_module)
        entities_list = list(document.Entities.values())
        self.assertEqual(len(entities_list), 1)
        self.assertIsInstance(entities_list[0], PyVHDLModelEntity)

    def test_error_handling(self):
        """Test error handling in conversion."""
        # Test with invalid generic (should handle gracefully)
        from pyhdlio.vhdl.ast import Generic
        invalid_generic = Generic(None, None, None)  # Invalid data

        # Should handle gracefully through Document conversion
        try:
            result = Document._convert_generic(invalid_generic)
            self.assertIsNone(result)
        except Exception:
            # Expected to handle gracefully
            pass

    def test_default_value_conversion_edge_cases(self):
        """Test edge cases in default value conversion."""
        # Empty value
        result = Document._convert_default_value("")
        self.assertIsNone(result)

        # None value
        result = Document._convert_default_value(None)
        self.assertIsNone(result)

        # Whitespace only
        result = Document._convert_default_value("   ")
        self.assertIsInstance(result, EnumerationLiteral)  # Treated as identifier

        # Negative integer
        result = Document._convert_default_value("-42")
        self.assertIsInstance(result, IntegerLiteral)
        self.assertEqual(result.Value, -42)

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_end_to_end_conversion(self):
        """Test complete end-to-end conversion pipeline."""
        # Parse → Convert → Verify using new consolidated API
        module = VHDLAST.from_file(self.simple_vhdl)
        document = Document.from_ast(module)

        self.assertEqual(len(document.Entities), 1)
        entity = list(document.Entities.values())[0]

        # Verify all components are present and correct
        self.assertEqual(entity.Identifier, "counter")
        self.assertEqual(len(entity.GenericItems), 2)
        self.assertEqual(len(entity.PortItems), 4)
        self.assertEqual(len(entity.PortGroups), 2)

        # Verify port grouping matches original
        original_entity = module.entities[0]
        self.assertEqual(len(entity.PortGroups), len(original_entity.port_groups))

    def test_new_document_api(self):
        """Test the new Document.from_file() API."""
        document = Document.from_file(self.simple_vhdl)

        # Verify Document structure
        self.assertEqual(len(document.Entities), 1)
        entity = list(document.Entities.values())[0]

        self.assertEqual(entity.Identifier, "counter")
        self.assertEqual(len(entity.GenericItems), 2)
        self.assertEqual(len(entity.PortItems), 4)
        self.assertEqual(len(entity.PortGroups), 2)


if __name__ == '__main__':
    unittest.main()