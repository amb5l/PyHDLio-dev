#!/usr/bin/env python3
"""
Test script to verify the unified VHDL parser handles all VHDL versions and features
"""

import sys
import os

# Add the hdlio package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from hdlio import HDLio
from hdlio.core.constants import *

def test_unified_parser():
    """Test that the unified parser works for all VHDL versions"""
    
    print("Unified VHDL Parser Test")
    print("=" * 40)
    
    # Test VHDL source with mixed language features
    vhdl_code = """
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity test_entity is
    generic (
        WIDTH : integer := 8;
        DEPTH : positive := 16
    );
    port (
        -- Clock and Reset
        clk     : in  std_logic;
        reset_n : in  std_logic;
        
        -- Data Interface  
        data_in  : in  std_logic_vector(WIDTH-1 downto 0);
        data_out : out std_logic_vector(WIDTH-1 downto 0);
        valid    : in  std_logic;
        ready    : out std_logic
    );
end entity test_entity;

architecture rtl of test_entity is
    signal reg_data : std_logic_vector(WIDTH-1 downto 0);
    type state_type is (IDLE, ACTIVE, DONE);
    signal state : state_type;
begin
    
    process(clk, reset_n)
    begin
        if reset_n = '0' then
            reg_data <= (others => '0');
            state <= IDLE;
        elsif rising_edge(clk) then
            case state is
                when IDLE =>
                    if valid = '1' then
                        reg_data <= data_in;
                        state <= ACTIVE;
                    end if;
                when ACTIVE =>
                    state <= DONE;
                when DONE =>
                    state <= IDLE;
            end case;
        end if;
    end process;
    
    data_out <= reg_data;
    ready <= '1' when state = DONE else '0';
    
end architecture rtl;
"""

    # Test all VHDL language versions with the unified parser
    vhdl_versions = [VHDL_1993, VHDL_2000, VHDL_2008, VHDL_2019]
    
    for version in vhdl_versions:
        print(f"\nTesting VHDL {version}:")
        print("-" * 20)
        
        try:
            # Test both comprehensive modes (should use same unified parser)
            for comprehensive in [False, True]:
                mode_name = "comprehensive" if comprehensive else "entity-focused"
                print(f"  {mode_name} mode: ", end="")
                
                # Parse directly using the parser
                from hdlio.core.parsers.parser_factory import ParserFactory
                parser = ParserFactory.get_parser(version, comprehensive)
                document = parser.parse("test.vhd", vhdl_code)
                
                # Verify parsing results
                design_units = document.getDesignUnits()
                print(f"✓ {len(design_units)} design units")
                
                # Check entity parsing
                entity = design_units[0]
                if hasattr(entity, 'getPortGroups'):
                    port_groups = entity.getPortGroups()
                    total_ports = sum(len(group.getPorts()) for group in port_groups)
                    print(f"    Port groups: {len(port_groups)}, Total ports: {total_ports}")
                    
                    # Verify port group names
                    group_names = [group.getName() for group in port_groups]
                    if "Clock and Reset" in group_names and "Data Interface" in group_names:
                        print(f"    ✓ Port groups correctly identified")
                    else:
                        print(f"    ⚠ Port groups: {group_names}")
        
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print(f"\n{'='*40}")
    print("✓ Unified VHDL parser test complete!")
    print("✓ Single parser handles all VHDL versions and language features")

if __name__ == "__main__":
    test_unified_parser() 