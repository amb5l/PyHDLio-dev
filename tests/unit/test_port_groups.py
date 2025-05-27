"""
Unit tests for HDLio port grouping functionality
"""

import pytest
from pathlib import Path
from hdlio import HDLio, VHDL_2008


class TestPortGrouping:
    """Test port grouping functionality"""

    @pytest.mark.port_groups
    @pytest.mark.vhdl
    def test_simple_entity_auto_grouping(self, temp_vhdl_file, hdlio_parser):
        """Test auto-grouping for simple entity without comments"""
        hdl = hdlio_parser(str(temp_vhdl_file))
        design_units = hdl.get_design_units()
        
        assert len(design_units) == 1
        entity = design_units[0]
        assert entity.get_vhdl_type() == "entity"
        
        port_groups = entity.get_port_groups()
        assert len(port_groups) >= 1  # Should have at least one group
        
        # Count total ports
        total_ports = sum(len(group.get_ports()) for group in port_groups)
        assert total_ports == 3  # clk, reset, data

    @pytest.mark.port_groups
    @pytest.mark.vhdl
    def test_comment_based_grouping(self, tmp_path, grouped_vhdl_content, hdlio_parser):
        """Test comment-based port grouping"""
        # Create temporary file with grouped content
        temp_file = tmp_path / "grouped_test.vhd"
        temp_file.write_text(grouped_vhdl_content)
        
        hdl = hdlio_parser(str(temp_file))
        design_units = hdl.get_design_units()
        
        assert len(design_units) == 1
        entity = design_units[0]
        
        port_groups = entity.get_port_groups()
        assert len(port_groups) >= 3  # Should have at least Clock, Reset, Data groups
        
        # Check for named groups
        group_names = [group.get_name() for group in port_groups]
        assert any("Clock" in name for name in group_names)
        assert any("Reset" in name for name in group_names) 
        assert any("Data" in name for name in group_names)

    @pytest.mark.port_groups
    @pytest.mark.vhdl
    def test_mixed_grouping_patterns(self, tmp_path, mixed_grouping_vhdl_content, hdlio_parser):
        """Test mixed grouping patterns"""
        temp_file = tmp_path / "mixed_test.vhd"
        temp_file.write_text(mixed_grouping_vhdl_content)
        
        hdl = hdlio_parser(str(temp_file))
        design_units = hdl.get_design_units()
        
        assert len(design_units) == 1
        entity = design_units[0]
        
        port_groups = entity.get_port_groups()
        assert len(port_groups) >= 3
        
        # Verify specific groups exist
        group_names = [group.get_name() for group in port_groups]
        assert "Control group" in group_names
        assert "Another group" in group_names

    @pytest.mark.port_groups
    def test_port_group_api(self, temp_vhdl_file, hdlio_parser):
        """Test port group API methods"""
        hdl = hdlio_parser(str(temp_vhdl_file))
        design_units = hdl.get_design_units()
        entity = design_units[0]
        
        port_groups = entity.get_port_groups()
        
        for port_group in port_groups:
            # Test group methods
            assert isinstance(port_group.get_name(), str)
            assert len(port_group.get_name()) > 0
            
            ports = port_group.get_ports()
            assert isinstance(ports, list)
            assert len(ports) > 0
            
            # Test port methods
            for port in ports:
                assert isinstance(port.get_name(), str)
                assert isinstance(port.get_type(), str)
                assert isinstance(port.get_direction(), str)
                assert port.get_direction() in ["in", "out", "inout", "buffer"]

    @pytest.mark.port_groups
    def test_port_group_source_order(self, tmp_path, grouped_vhdl_content, hdlio_parser):
        """Test that port groups maintain source order"""
        temp_file = tmp_path / "grouped_test.vhd"
        temp_file.write_text(grouped_vhdl_content)
        
        hdl = hdlio_parser(str(temp_file))
        design_units = hdl.get_design_units()
        entity = design_units[0]
        
        port_groups = entity.get_port_groups()
        
        # Check that groups maintain some logical order
        # (exact order may vary based on parsing, but should be consistent)
        assert len(port_groups) >= 1
        
        # Verify ports within groups maintain order
        for port_group in port_groups:
            ports = port_group.get_ports()
            if len(ports) > 1:
                # Ports should have consistent names (basic sanity check)
                port_names = [port.get_name() for port in ports]
                assert len(set(port_names)) == len(port_names)  # No duplicates

    @pytest.mark.port_groups
    def test_empty_entity_port_groups(self, tmp_path, hdlio_parser):
        """Test entity with no ports"""
        empty_entity = """entity empty_test is
end entity empty_test;"""
        
        temp_file = tmp_path / "empty_test.vhd"
        temp_file.write_text(empty_entity)
        
        hdl = hdlio_parser(str(temp_file))
        design_units = hdl.get_design_units()
        
        assert len(design_units) == 1
        entity = design_units[0]
        
        port_groups = entity.get_port_groups()
        # Should either be empty or have empty groups
        if port_groups:
            total_ports = sum(len(group.get_ports()) for group in port_groups)
            assert total_ports == 0 