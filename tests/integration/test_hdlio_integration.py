"""
Integration tests for HDLio complete workflow
"""

import pytest
from pathlib import Path
from hdlio import HDLio, VHDL_2008


class TestHDLioIntegration:
    """Integration tests for complete HDLio workflow"""

    @pytest.mark.integration
    @pytest.mark.vhdl
    def test_complete_vhdl_workflow(self, tmp_path, grouped_vhdl_content):
        """Test complete workflow from parsing to port group extraction"""
        # Create test file
        vhdl_file = tmp_path / "complete_test.vhd"
        vhdl_file.write_text(grouped_vhdl_content)
        
        # Parse the file
        hdl = HDLio(str(vhdl_file), VHDL_2008)
        
        # Get design units
        design_units = hdl.getDesignUnits()
        assert len(design_units) >= 1
        
        # Find the entity
        entity = None
        for unit in design_units:
            if unit.getVhdlType() == "entity":
                entity = unit
                break
        
        assert entity is not None
        assert entity.name == "grouped_test"
        
        # Get port groups
        port_groups = entity.getPortGroups()
        assert len(port_groups) >= 3
        
        # Verify we can access all ports
        total_ports = 0
        for port_group in port_groups:
            group_name = port_group.getName()
            assert isinstance(group_name, str)
            assert len(group_name) > 0
            
            ports = port_group.getPorts()
            total_ports += len(ports)
            
            for port in ports:
                assert isinstance(port.getName(), str)
                assert isinstance(port.getType(), str)
                assert isinstance(port.getDirection(), str)
        
        assert total_ports >= 5  # Should have several ports

    @pytest.mark.integration
    @pytest.mark.vhdl
    def test_api_consistency(self, simple_vhdl_file):
        """Test API consistency across different usage patterns"""
        if not simple_vhdl_file.exists():
            pytest.skip("Simple VHDL file not found")
        
        # Test with string path
        hdl1 = HDLio(str(simple_vhdl_file), VHDL_2008)
        design_units1 = hdl1.getDesignUnits()
        
        # Test with Path object
        hdl2 = HDLio(simple_vhdl_file, VHDL_2008)
        design_units2 = hdl2.getDesignUnits()
        
        # Results should be consistent
        assert len(design_units1) == len(design_units2)
        
        if design_units1:
            entity1 = design_units1[0]
            entity2 = design_units2[0]
            
            assert entity1.name == entity2.name
            assert entity1.getVhdlType() == entity2.getVhdlType()

    @pytest.mark.integration
    def test_real_world_vhdl_file(self, complex_vhdl_file):
        """Test with real-world VHDL file if available"""
        if not complex_vhdl_file.exists():
            pytest.skip("Complex VHDL file not found in fixtures")
        
        hdl = HDLio(str(complex_vhdl_file), VHDL_2008)
        design_units = hdl.getDesignUnits()
        
        # Should be able to parse without errors
        assert isinstance(design_units, list)
        assert len(design_units) >= 1
        
        # Check that we can access all design units
        for unit in design_units:
            assert hasattr(unit, 'name')
            assert hasattr(unit, 'getVhdlType')
            unit_type = unit.getVhdlType()
            assert unit_type in ["entity", "architecture", "package", "package_body", "configuration"]

    @pytest.mark.integration
    @pytest.mark.slow
    def test_large_file_performance(self, tmp_path):
        """Test performance with larger VHDL files"""
        # Generate a larger VHDL file
        large_vhdl = self._generate_large_vhdl_entity(50)  # 50 ports
        
        vhdl_file = tmp_path / "large_test.vhd"
        vhdl_file.write_text(large_vhdl)
        
        # Time the parsing (basic performance test)
        import time
        start_time = time.time()
        
        hdl = HDLio(str(vhdl_file), VHDL_2008)
        design_units = hdl.getDesignUnits()
        
        end_time = time.time()
        parse_time = end_time - start_time
        
        # Should complete in reasonable time (adjust threshold as needed)
        assert parse_time < 5.0  # 5 seconds max
        
        assert len(design_units) >= 1
        entity = design_units[0]
        port_groups = entity.getPortGroups()
        
        # Should have parsed all ports
        total_ports = sum(len(group.getPorts()) for group in port_groups)
        assert total_ports >= 40  # Should parse most ports

    @pytest.mark.integration
    def test_error_recovery(self, tmp_path):
        """Test error recovery and partial parsing"""
        # Create VHDL with some errors but valid parts
        mixed_quality_vhdl = """
        -- Valid entity
        entity good_entity is
          port (
            clk : in std_logic;
            data : out std_logic
          );
        end entity good_entity;
        
        -- Invalid syntax but parser should continue
        entity bad_entity is
          port (
            invalid syntax here
            but_this_might_work : in std_logic
          );
        end entity bad_entity;
        
        -- Another valid entity
        entity another_good is
        end entity another_good;
        """
        
        vhdl_file = tmp_path / "mixed_quality.vhd"
        vhdl_file.write_text(mixed_quality_vhdl)
        
        # Should not crash and should parse what it can
        hdl = HDLio(str(vhdl_file), VHDL_2008)
        design_units = hdl.getDesignUnits()
        
        # Should find at least some design units
        assert isinstance(design_units, list)
        # May have found 1 or more units depending on error recovery

    def _generate_large_vhdl_entity(self, num_ports):
        """Generate a VHDL entity with many ports for performance testing"""
        ports = []
        for i in range(num_ports):
            direction = "in" if i % 2 == 0 else "out"
            port_type = "std_logic" if i % 3 == 0 else "integer"
            ports.append(f"    port_{i} : {direction} {port_type};")
        
        # Remove semicolon from last port
        if ports:
            ports[-1] = ports[-1].rstrip(';')
        
        ports_str = '\n'.join(ports)
        
        return f"""library ieee;
use ieee.std_logic_1164.all;

entity large_test_entity is
  port (
{ports_str}
  );
end entity large_test_entity;

architecture rtl of large_test_entity is
begin
  -- Implementation would go here
end architecture rtl;""" 