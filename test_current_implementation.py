#!/usr/bin/env python3
"""
Test script to check current HDLio implementation
"""

import sys
import os

print("Testing HDLio Implementation")
print("=" * 40)

# Test basic imports
try:
    from hdlio import HDLio, VHDL_2008
    print("✓ HDLio import successful")
except Exception as e:
    print(f"✗ HDLio import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Create a simple VHDL test file
test_vhdl = """library ieee;
use ieee.std_logic_1164.all;

entity test_entity is
    port (
        -- Clock and reset signals
        clk : in std_logic;
        reset : in std_logic;

        -- Data signals
        data_in : in std_logic_vector(7 downto 0);
        data_out : out std_logic_vector(7 downto 0);
        valid : out std_logic
    );
end entity test_entity;

architecture rtl of test_entity is
begin
    process(clk, reset)
    begin
        if reset = '1' then
            data_out <= (others => '0');
            valid <= '0';
        elsif rising_edge(clk) then
            data_out <= data_in;
            valid <= '1';
        end if;
    end process;
end architecture rtl;
"""

print("\nCreating test VHDL file...")
with open('test_simple.vhd', 'w') as f:
    f.write(test_vhdl)

# Test parsing
try:
    print("✓ Test file created")

    print("\nTesting HDLio parsing...")
    hdl = HDLio('test_simple.vhd', VHDL_2008)
    print("✓ HDLio instance created")

    design_units = hdl.getDesignUnits()
    print(f"✓ Parsed {len(design_units)} design units")

    # Test each design unit
    for unit in design_units:
        print(f"\nDesign Unit: {unit.name} (type: {unit.getVhdlType()})")

        if unit.getVhdlType() == 'entity':
            groups = unit.getPortGroups()
            print(f"✓ Found {len(groups)} port groups")

            total_ports = 0
            for i, group in enumerate(groups):
                ports = group.getPorts()
                total_ports += len(ports)
                print(f"  Group {i+1}: '{group.getName()}' ({len(ports)} ports)")

                for port in ports:
                    print(f"    • {port.getName()}: {port.getDirection()} {port.getType()}")

            print(f"✓ Found {total_ports} total ports")

    print("\n✓ All tests passed!")

except Exception as e:
    print(f"✗ Parsing test failed: {e}")
    import traceback
    traceback.print_exc()

# Clean up
finally:
    if os.path.exists('test_simple.vhd'):
        os.remove('test_simple.vhd')
        print("\n✓ Cleaned up test file")