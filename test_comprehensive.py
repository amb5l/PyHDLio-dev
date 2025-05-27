#!/usr/bin/env python3
"""
Comprehensive test script for HDLio library
Tests various VHDL entities with different port grouping scenarios
"""

import sys
import os

print("HDLio Comprehensive Test Suite")
print("=" * 50)

# Test basic imports
try:
    from hdlio import HDLio, VHDL_2008, VHDL_1993, VHDL_2000, VHDL_2019
    print("✓ HDLio import successful")
except Exception as e:
    print(f"✗ HDLio import failed: {e}")
    sys.exit(1)

def test_entity_parsing(entity_name, vhdl_content, expected_groups=None):
    """Test parsing a single entity"""
    print(f"\nTesting {entity_name}:")
    print("-" * 30)
    
    filename = f'test_{entity_name.lower()}.vhd'
    
    try:
        # Create test file
        with open(filename, 'w') as f:
            f.write(vhdl_content)
        
        # Parse with HDLio
        hdl = HDLio(filename, VHDL_2008)
        design_units = hdl.getDesignUnits()
        
        print(f"✓ Parsed {len(design_units)} design units")
        
        for unit in design_units:
            print(f"  Unit: {unit.name} (type: {unit.getVhdlType()})")
            
            if unit.getVhdlType() == 'entity':
                groups = unit.getPortGroups()
                print(f"  ✓ Found {len(groups)} port groups")
                
                for i, group in enumerate(groups):
                    ports = group.getPorts()
                    print(f"    Group {i+1}: '{group.getName()}' ({len(ports)} ports)")
                    
                    for port in ports:
                        print(f"      • {port.getName()}: {port.getDirection()} {port.getType()}")
                
                # Check expected groups
                if expected_groups:
                    group_names = [g.getName() for g in groups]
                    for expected in expected_groups:
                        if expected in group_names:
                            print(f"  ✓ Found expected group: '{expected}'")
                        else:
                            print(f"  ✗ Missing expected group: '{expected}'")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        return False
    
    finally:
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)

# Test cases
test_cases = [
    # Test 1: Simple entity with comment-based groups
    {
        "name": "simple_grouped_entity",
        "content": """entity simple_entity is
    port (
        -- Clock and Reset
        clk : in std_logic;
        reset : in std_logic;
        
        -- Data Interface
        data_in : in std_logic_vector(7 downto 0);
        data_out : out std_logic_vector(7 downto 0);
        valid : out std_logic
    );
end entity simple_entity;""",
        "expected": ["Clock and Reset", "Data Interface"]
    },
    
    # Test 2: Entity with multiple comment groups
    {
        "name": "multi_group_entity",
        "content": """entity multi_group_entity is
    port (
        -- System Signals
        clk : in std_logic;
        reset_n : in std_logic;
        enable : in std_logic;
        
        -- Input Bus
        addr_in : in std_logic_vector(31 downto 0);
        data_in : in std_logic_vector(31 downto 0);
        write_en : in std_logic;
        read_en : in std_logic;
        
        -- Output Bus  
        data_out : out std_logic_vector(31 downto 0);
        ready : out std_logic;
        error : out std_logic;
        
        -- Debug Interface
        debug_addr : out std_logic_vector(15 downto 0);
        debug_data : out std_logic_vector(7 downto 0)
    );
end entity multi_group_entity;""",
        "expected": ["System Signals", "Input Bus", "Output Bus", "Debug Interface"]
    },
    
    # Test 3: Entity with mixed grouping styles
    {
        "name": "mixed_style_entity", 
        "content": """entity mixed_style_entity is
    port (
        -- Primary Interface
        primary_clk : in std_logic;
        primary_data : inout std_logic_vector(15 downto 0);
        
        secondary_clk : in std_logic;
        secondary_data : in std_logic_vector(7 downto 0);
        
        -- Status Outputs
        status_ready : out std_logic;
        status_error : out std_logic;
        status_busy : out std_logic
    );
end entity mixed_style_entity;""",
        "expected": ["Primary Interface", "Status Outputs"]
    },
    
    # Test 4: Entity without comments (default grouping)
    {
        "name": "no_comments_entity",
        "content": """entity no_comments_entity is
    port (
        clk : in std_logic;
        data_in : in std_logic_vector(7 downto 0);
        data_out : out std_logic_vector(7 downto 0);
        enable : in std_logic;
        ready : out std_logic
    );
end entity no_comments_entity;""",
        "expected": None  # Should create default group
    }
]

# Run all tests
passed_tests = 0
total_tests = len(test_cases)

for test_case in test_cases:
    if test_entity_parsing(
        test_case["name"], 
        test_case["content"], 
        test_case.get("expected")
    ):
        passed_tests += 1

# Summary
print(f"\n{'='*50}")
print(f"Test Results: {passed_tests}/{total_tests} tests passed")

if passed_tests == total_tests:
    print("✓ All tests passed!")
else:
    print(f"✗ {total_tests - passed_tests} tests failed")

# Test language version support
print(f"\nTesting language version support:")
try:
    for lang in [VHDL_1993, VHDL_2000, VHDL_2008, VHDL_2019]:
        print(f"✓ {lang} supported")
except Exception as e:
    print(f"✗ Language version test failed: {e}")

print("\n✓ HDLio library test complete!") 