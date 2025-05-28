#!/usr/bin/env python3
"""
Test script to verify VHDL parser functionality
"""

import tempfile
import os
import sys

# Add PyHDLio to path
sys.path.insert(0, 'PyHDLio')

from hdlio import HDLio, HDL_LRM

def test_vhdl_parsing():
    """Test VHDL parsing with a simple entity"""
    
    # Start with the simplest possible VHDL entity
    vhdl_content = """entity simple is
end entity simple;
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.vhd', delete=False) as f:
        f.write(vhdl_content)
        temp_file = f.name
    
    try:
        print("Testing VHDL parsing...")
        print(f"File: {temp_file}")
        print(f"Content:\n{vhdl_content}")
        print("-" * 50)
        
        hdlio = HDLio()
        result = hdlio.load(temp_file, "work", HDL_LRM.VHDL_2008)
        
        print(f"Load result: {result}")
        print(f"Libraries: {list(hdlio.libraries.keys())}")
        
        if 'work' in hdlio.libraries:
            library = hdlio.libraries['work']
            print(f"Library name: {library.name}")
            print(f"Library language: {library.language}")
            print(f"Design units: {len(library.design_units)}")
            
            if library.design_units:
                for i, unit in enumerate(library.design_units):
                    print(f"  Unit {i+1}: {unit.name} ({type(unit).__name__})")
                    if hasattr(unit, 'port_groups'):
                        print(f"    Port groups: {len(unit.port_groups)}")
                        for j, group in enumerate(unit.port_groups):
                            print(f"      Group {j+1}: {len(group.ports)} ports")
                            for port in group.ports:
                                print(f"        - {port.name}: {port.direction} {port.type}")
                return True
            else:
                print("✗ FAILED: No design units found")
                return False
        else:
            print("✗ FAILED: No 'work' library found")
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        os.unlink(temp_file)

if __name__ == "__main__":
    success = test_vhdl_parsing()
    print(f"\nVHDL Parser Test: {'PASSED' if success else 'FAILED'}") 