"""
Comprehensive tests for PyVHDLModel converter
"""

import unittest
import os
import sys
from typing import List

# Add PyHDLio package to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'PyHDLio'))

from hdlio.vhdl.parse_vhdl import parse_vhdl
from hdlio.vhdl.converters.pyvhdlmodel_converter import PyVHDLModelConverter, convert_to_pyvhdlmodel
from hdlio.vhdl.ast.ast import Entity as PyHDLioEntity

# pyVHDLModel imports
try:
    from pyVHDLModel.DesignUnit import Entity as PyVHDLModelEntity
    from pyVHDLModel.Interface import GenericConstantInterfaceItem, PortSignalInterfaceItem, PortGroup
    from pyVHDLModel.Base import Mode
    from pyVHDLModel.Expression import IntegerLiteral, EnumerationLiteral, StringLiteral
    PYVHDLMODEL_AVAILABLE = True
except ImportError:
    PYVHDLMODEL_AVAILABLE = False


@unittest.skipUnless(PYVHDLMODEL_AVAILABLE, "pyVHDLModel not available")
class TestPyVHDLModelConverter(unittest.TestCase):
    """Test PyVHDLModel converter functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.converter = PyVHDLModelConverter()
        self.simple_vhdl = os.path.join(
            os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
        )
        
        # Parse the simple VHDL file
        if os.path.exists(self.simple_vhdl):
            self.simple_module = parse_vhdl(self.simple_vhdl, mode='ast')
            self.simple_entity = self.simple_module.entities[0]
        else:
            self.simple_module = None
            self.simple_entity = None

    def test_converter_initialization(self):
        """Test converter initializes correctly."""
        self.assertIsInstance(self.converter, PyVHDLModelConverter)
        self.assertIsInstance(self.converter._mode_mapping, dict)
        self.assertEqual(self.converter._mode_mapping['in'], Mode.In)
        self.assertEqual(self.converter._mode_mapping['out'], Mode.Out)
        self.assertEqual(self.converter._mode_mapping['inout'], Mode.InOut)

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_entity_conversion(self):
        """Test complete entity conversion."""
        converted_entity = self.converter.convert_entity(self.simple_entity)

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
        converted_entity = self.converter.convert_entity(self.simple_entity)

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
        from hdlio.vhdl.ast.ast import Generic

        # Test integer default
        int_generic = Generic("TEST_INT", "integer", "42")
        converted = self.converter._convert_generic(int_generic)
        self.assertIsInstance(converted.DefaultExpression, IntegerLiteral)
        self.assertEqual(converted.DefaultExpression.Value, 42)

        # Test string default
        str_generic = Generic("TEST_STR", "string", '"hello"')
        converted = self.converter._convert_generic(str_generic)
        from pyVHDLModel.Expression import StringLiteral
        self.assertIsInstance(converted.DefaultExpression, StringLiteral)  # Should be StringLiteral object

        # Test enumeration default
        enum_generic = Generic("TEST_ENUM", "state_type", "IDLE")
        converted = self.converter._convert_generic(enum_generic)
        self.assertIsInstance(converted.DefaultExpression, EnumerationLiteral)
        self.assertEqual(converted.DefaultExpression.Value, "IDLE")

    def test_port_mode_mapping(self):
        """Test port mode mapping functionality."""
        from hdlio.vhdl.ast.ast import Port

        # Test input port
        in_port = Port("test_in", "in", "std_logic")
        converted = self.converter._convert_port(in_port)
        self.assertEqual(converted.Mode, Mode.In)

        # Test output port
        out_port = Port("test_out", "out", "std_logic")
        converted = self.converter._convert_port(out_port)
        self.assertEqual(converted.Mode, Mode.Out)

        # Test inout port
        inout_port = Port("test_inout", "inout", "std_logic")
        converted = self.converter._convert_port(inout_port)
        self.assertEqual(converted.Mode, Mode.InOut)

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_convenience_function(self):
        """Test the convenience conversion function."""
        # Test with single entity
        converted_entities = convert_to_pyvhdlmodel(self.simple_entity)
        self.assertEqual(len(converted_entities), 1)
        self.assertIsInstance(converted_entities[0], PyVHDLModelEntity)

        # Test with module
        converted_entities = convert_to_pyvhdlmodel(self.simple_module)
        self.assertEqual(len(converted_entities), 1)
        self.assertIsInstance(converted_entities[0], PyVHDLModelEntity)

    def test_error_handling(self):
        """Test error handling in conversion."""
        # Test with invalid generic (should handle gracefully)
        from hdlio.vhdl.ast.ast import Generic
        invalid_generic = Generic(None, None, None)  # Invalid data

        # Should not raise exception, but return None
        result = self.converter._convert_generic(invalid_generic)
        self.assertIsNone(result)

    def test_default_value_conversion_edge_cases(self):
        """Test edge cases in default value conversion."""
        # Empty value
        result = self.converter._convert_default_value("")
        self.assertIsNone(result)

        # None value
        result = self.converter._convert_default_value(None)
        self.assertIsNone(result)

        # Whitespace only
        result = self.converter._convert_default_value("   ")
        self.assertIsInstance(result, EnumerationLiteral)  # Treated as identifier

        # Negative integer
        result = self.converter._convert_default_value("-42")
        self.assertIsInstance(result, IntegerLiteral)
        self.assertEqual(result.Value, -42)

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_end_to_end_conversion(self):
        """Test complete end-to-end conversion pipeline."""
        # Parse → Convert → Verify
        module = parse_vhdl(self.simple_vhdl, mode='ast')
        converted_entities = convert_to_pyvhdlmodel(module)

        self.assertEqual(len(converted_entities), 1)
        entity = converted_entities[0]

        # Verify all components are present and correct
        self.assertEqual(entity.Identifier, "counter")
        self.assertEqual(len(entity.GenericItems), 2)
        self.assertEqual(len(entity.PortItems), 4)
        self.assertEqual(len(entity.PortGroups), 2)

        # Verify port grouping matches original
        original_entity = module.entities[0]
        self.assertEqual(len(entity.PortGroups), len(original_entity.port_groups))


if __name__ == '__main__':
    unittest.main()