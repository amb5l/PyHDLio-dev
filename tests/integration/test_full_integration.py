"""
Full Integration Tests for PyHDLio + pyVHDLModel
Tests the complete pipeline from VHDL parsing through conversion to reporting.
"""

import unittest
import os
import sys

# Add PyHDLio package to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'PyHDLio'))

from hdlio.vhdl.parse_vhdl import parse_vhdl
from hdlio.vhdl.converters.pyvhdlmodel_converter import convert_to_pyvhdlmodel
from hdlio.vhdl.reporter import report_entity, report_entities

# pyVHDLModel imports
try:
    from pyVHDLModel.DesignUnit import Entity as PyVHDLModelEntity
    PYVHDLMODEL_AVAILABLE = True
except ImportError:
    PYVHDLMODEL_AVAILABLE = False


class TestFullIntegration(unittest.TestCase):
    """Test complete integration pipeline."""

    def setUp(self):
        """Set up test fixtures."""
        self.simple_vhdl = os.path.join(
            os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
        )

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_ast_pipeline(self):
        """Test complete AST pipeline: Parse → Report."""
        # Step 1: Parse VHDL to AST
        module = parse_vhdl(self.simple_vhdl, mode='ast')
        self.assertIsNotNone(module)
        self.assertEqual(len(module.entities), 1)
        
        entity = module.entities[0]
        self.assertEqual(entity.name, "counter")
        
        # Step 2: Verify AST structure
        self.assertEqual(len(entity.generics), 2)
        self.assertEqual(len(entity.ports), 4)
        self.assertEqual(len(entity.port_groups), 2)
        
        # Step 3: Report AST
        report = report_entity(entity)
        self.assertIn("Entity: counter", report)
        self.assertIn("WIDTH", report)
        self.assertIn("Group 1:", report)
        self.assertIn("Group 2:", report)

    @unittest.skipUnless(PYVHDLMODEL_AVAILABLE and os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "pyVHDLModel not available or Simple VHDL file not found")
    def test_pyvhdlmodel_pipeline(self):
        """Test complete pyVHDLModel pipeline: Parse → Convert → Report."""
        # Step 1: Parse VHDL to AST
        module = parse_vhdl(self.simple_vhdl, mode='ast')
        self.assertIsNotNone(module)
        
        # Step 2: Convert to pyVHDLModel
        converted_entities = convert_to_pyvhdlmodel(module)
        self.assertEqual(len(converted_entities), 1)
        
        entity = converted_entities[0]
        self.assertIsInstance(entity, PyVHDLModelEntity)
        self.assertEqual(entity.Identifier, "counter")
        
        # Step 3: Verify pyVHDLModel structure
        self.assertEqual(len(entity.GenericItems), 2)
        self.assertEqual(len(entity.PortItems), 4)
        self.assertEqual(len(entity.PortGroups), 2)
        
        # Step 4: Report pyVHDLModel
        report = report_entity(entity)
        self.assertIn("Entity: counter", report)
        self.assertIn("WIDTH", report)
        self.assertIn("Group 1:", report)
        self.assertIn("Group 2:", report)

    @unittest.skipUnless(PYVHDLMODEL_AVAILABLE and os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "pyVHDLModel not available or Simple VHDL file not found")
    def test_dual_pipeline_consistency(self):
        """Test that both pipelines produce consistent results."""
        # Parse once
        module = parse_vhdl(self.simple_vhdl, mode='ast')
        
        # AST pipeline
        ast_entity = module.entities[0]
        ast_report = report_entity(ast_entity)
        
        # pyVHDLModel pipeline
        converted_entities = convert_to_pyvhdlmodel(module)
        model_entity = converted_entities[0]
        model_report = report_entity(model_entity)
        
        # Both should contain the same basic information
        for content in ["Entity: counter", "WIDTH", "DEPTH", "clk", "reset", "start", "count"]:
            self.assertIn(content, ast_report, f"AST report missing: {content}")
            self.assertIn(content, model_report, f"Model report missing: {content}")
        
        # Both should have the same grouping structure
        ast_groups = ast_report.count("Group ")
        model_groups = model_report.count("Group ")
        self.assertEqual(ast_groups, model_groups, "Different number of port groups")

    @unittest.skipUnless(PYVHDLMODEL_AVAILABLE and os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "pyVHDLModel not available or Simple VHDL file not found")
    def test_port_grouping_preservation(self):
        """Test that port grouping is perfectly preserved through the pipeline."""
        # Parse and convert
        module = parse_vhdl(self.simple_vhdl, mode='ast')
        converted_entities = convert_to_pyvhdlmodel(module)
        
        ast_entity = module.entities[0]
        model_entity = converted_entities[0]
        
        # Compare port grouping structure
        ast_groups = ast_entity.port_groups
        model_groups = model_entity.PortGroups
        
        self.assertEqual(len(ast_groups), len(model_groups))
        
        for i, (ast_group, model_group) in enumerate(zip(ast_groups, model_groups)):
            # Check group sizes match
            self.assertEqual(len(ast_group.ports), len(model_group.Ports),
                           f"Group {i+1} size mismatch")
            
            # Check port names match
            ast_port_names = {port.name for port in ast_group.ports}
            model_port_names = {port.Identifiers[0] for port in model_group.Ports}
            
            self.assertEqual(ast_port_names, model_port_names,
                           f"Group {i+1} port names mismatch")

    @unittest.skipUnless(PYVHDLMODEL_AVAILABLE and os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "pyVHDLModel not available or Simple VHDL file not found")
    def test_generic_preservation(self):
        """Test that generic information is preserved through conversion."""
        # Parse and convert
        module = parse_vhdl(self.simple_vhdl, mode='ast')
        converted_entities = convert_to_pyvhdlmodel(module)
        
        ast_entity = module.entities[0]
        model_entity = converted_entities[0]
        
        # Check generic count
        self.assertEqual(len(ast_entity.generics), len(model_entity.GenericItems))
        
        # Create mapping for comparison
        ast_generics = {g.name: g for g in ast_entity.generics}
        model_generics = {g.Identifiers[0]: g for g in model_entity.GenericItems}
        
        # Check that all AST generics have corresponding model generics
        for name, ast_generic in ast_generics.items():
            self.assertIn(name, model_generics, f"Generic {name} missing in model")
            
            model_generic = model_generics[name]
            
            # Check default values are preserved
            if ast_generic.default_value:
                self.assertIsNotNone(model_generic.DefaultExpression,
                                   f"Default value missing for {name}")

    @unittest.skipUnless(PYVHDLMODEL_AVAILABLE and os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "pyVHDLModel not available or Simple VHDL file not found")
    def test_port_mode_preservation(self):
        """Test that port modes are correctly preserved and converted."""
        # Parse and convert
        module = parse_vhdl(self.simple_vhdl, mode='ast')
        converted_entities = convert_to_pyvhdlmodel(module)
        
        ast_entity = module.entities[0]
        model_entity = converted_entities[0]
        
        # Create mapping for comparison
        ast_ports = {p.name: p for p in ast_entity.ports}
        model_ports = {p.Identifiers[0]: p for p in model_entity.PortItems}
        
        # Check specific port modes
        expected_modes = {
            'clk': 'in',
            'reset': 'in',
            'start': 'in',
            'count': 'out'
        }
        
        for port_name, expected_mode in expected_modes.items():
            # Check AST
            self.assertIn(port_name, ast_ports)
            self.assertEqual(ast_ports[port_name].direction, expected_mode)
            
            # Check model
            self.assertIn(port_name, model_ports)
            actual_mode = model_ports[port_name].Mode.name.lower()
            self.assertEqual(actual_mode, expected_mode)

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_error_resilience(self):
        """Test that the pipeline handles errors gracefully."""
        # This should not raise exceptions even if conversion fails
        module = parse_vhdl(self.simple_vhdl, mode='ast')
        
        try:
            # Even if pyVHDLModel is not available, this should not crash
            if PYVHDLMODEL_AVAILABLE:
                converted_entities = convert_to_pyvhdlmodel(module)
                self.assertIsNotNone(converted_entities)
            else:
                # Skip conversion test if pyVHDLModel not available
                pass
        except Exception as e:
            self.fail(f"Pipeline should handle errors gracefully, but got: {e}")

    @unittest.skipUnless(PYVHDLMODEL_AVAILABLE and os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "pyVHDLModel not available or Simple VHDL file not found")
    def test_round_trip_information_preservation(self):
        """Test that no essential information is lost in AST → pyVHDLModel conversion."""
        # Parse original
        module = parse_vhdl(self.simple_vhdl, mode='ast')
        ast_entity = module.entities[0]
        
        # Convert to pyVHDLModel
        converted_entities = convert_to_pyvhdlmodel(module)
        model_entity = converted_entities[0]
        
        # Check entity name
        self.assertEqual(ast_entity.name, model_entity.Identifier)
        
        # Check counts are preserved
        self.assertEqual(len(ast_entity.generics), len(model_entity.GenericItems))
        self.assertEqual(len(ast_entity.ports), len(model_entity.PortItems))
        self.assertEqual(len(ast_entity.port_groups), len(model_entity.PortGroups))
        
        # Check that we can generate meaningful reports from both
        ast_report = report_entity(ast_entity)
        model_report = report_entity(model_entity)
        
        # Both reports should contain essential information
        essential_info = ["counter", "WIDTH", "DEPTH", "clk", "reset", "start", "count"]
        for info in essential_info:
            self.assertIn(info, ast_report)
            self.assertIn(info, model_report)

    @unittest.skipUnless(os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )), "Simple VHDL file not found")
    def test_performance_baseline(self):
        """Test basic performance characteristics."""
        import time
        
        # Test AST parsing performance
        start_time = time.time()
        module = parse_vhdl(self.simple_vhdl, mode='ast')
        ast_time = time.time() - start_time
        
        # AST parsing should be reasonably fast (< 1 second for simple file)
        self.assertLess(ast_time, 1.0, "AST parsing too slow")
        
        if PYVHDLMODEL_AVAILABLE:
            # Test conversion performance
            start_time = time.time()
            converted_entities = convert_to_pyvhdlmodel(module)
            conversion_time = time.time() - start_time
            
            # Conversion should also be reasonably fast
            self.assertLess(conversion_time, 1.0, "Conversion too slow")


if __name__ == '__main__':
    unittest.main()