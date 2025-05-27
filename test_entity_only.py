#!/usr/bin/env python3
"""
Test script to check entity parsing specifically
"""

import sys
import os

print("Testing Entity Parsing Only")
print("=" * 40)

# Test basic imports
try:
    from hdlio import HDLio, VHDL_2008
    print("✓ HDLio import successful")
except Exception as e:
    print(f"✗ HDLio import failed: {e}")
    sys.exit(1)

# Create a simple entity-only VHDL test file
test_vhdl = """entity test_entity is
    port (
        -- Clock and reset signals
        clk : in std_logic;
        reset : in std_logic;

        -- Data signals
        data_in : in std_logic_vector;
        data_out : out std_logic_vector;
        valid : out std_logic
    );
end entity test_entity;
"""

print("\nCreating simple entity test...")
with open('test_entity.vhd', 'w') as f:
    f.write(test_vhdl)

# Test parsing
try:
    print("✓ Test file created")

    print("\nTesting HDLio parsing...")
    hdl = HDLio('test_entity.vhd', VHDL_2008)
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

            # Test the expected grouping based on comments
            if len(groups) >= 2:
                group_names = [g.getName() for g in groups]
                print(f"Group names: {group_names}")
                if any("Clock" in name for name in group_names):
                    print("✓ Found Clock signals group")
                if any("Data" in name for name in group_names):
                    print("✓ Found Data signals group")

    print("\n✓ Entity parsing test passed!")

except Exception as e:
    print(f"✗ Parsing test failed: {e}")
    import traceback
    traceback.print_exc()

# Clean up
finally:
    if os.path.exists('test_entity.vhd'):
        os.remove('test_entity.vhd')
        print("\n✓ Cleaned up test file")