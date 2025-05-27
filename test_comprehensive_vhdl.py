#!/usr/bin/env python3
"""
Test comprehensive VHDL parsing with full VHDL files
"""

import sys
import os

print("Comprehensive VHDL Parsing Test")
print("=" * 40)

try:
    from hdlio import HDLio, VHDL_2008
    print("✓ HDLio import successful")
except Exception as e:
    print(f"✗ HDLio import failed: {e}")
    sys.exit(1)

# Create a comprehensive VHDL test file
full_vhdl = """library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity cpu_core is
    generic (
        DATA_WIDTH : integer := 32;
        ADDR_WIDTH : integer := 32
    );
    port (
        -- Clock and Reset
        clk : in std_logic;
        reset_n : in std_logic;
        
        -- Instruction Interface
        instr_addr : out std_logic_vector(ADDR_WIDTH-1 downto 0);
        instr_data : in std_logic_vector(DATA_WIDTH-1 downto 0);
        instr_valid : in std_logic;
        
        -- Data Interface
        data_addr : out std_logic_vector(ADDR_WIDTH-1 downto 0);
        data_write : out std_logic_vector(DATA_WIDTH-1 downto 0);
        data_read : in std_logic_vector(DATA_WIDTH-1 downto 0);
        data_we : out std_logic;
        data_re : out std_logic;
        
        -- Control Signals
        interrupt : in std_logic;
        halt : out std_logic
    );
end entity cpu_core;

architecture behavioral of cpu_core is
    type cpu_state_t is (IDLE, FETCH, DECODE, EXECUTE, WRITEBACK);
    
    signal current_state : cpu_state_t := IDLE;
    signal next_state : cpu_state_t;
    
    signal pc : unsigned(ADDR_WIDTH-1 downto 0) := (others => '0');
    signal instruction : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal alu_result : signed(DATA_WIDTH-1 downto 0);
    
    constant NOP_INSTRUCTION : std_logic_vector(DATA_WIDTH-1 downto 0) := x"00000000";
    
begin
    -- Program Counter
    instr_addr <= std_logic_vector(pc);
    
    -- State Machine Process
    state_machine_proc: process(clk, reset_n)
    begin
        if reset_n = '0' then
            current_state <= IDLE;
            pc <= (others => '0');
            halt <= '0';
        elsif rising_edge(clk) then
            current_state <= next_state;
            
            case current_state is
                when IDLE =>
                    if interrupt = '0' then
                        pc <= pc + 1;
                    end if;
                    
                when FETCH =>
                    if instr_valid = '1' then
                        instruction <= instr_data;
                    end if;
                    
                when DECODE =>
                    -- Decode instruction
                    null;
                    
                when EXECUTE =>
                    -- Execute instruction
                    alu_result <= signed(instruction(15 downto 0)) + signed(instruction(31 downto 16));
                    
                when WRITEBACK =>
                    data_write <= std_logic_vector(alu_result);
                    data_we <= '1';
                    
                when others =>
                    current_state <= IDLE;
            end case;
        end if;
    end process state_machine_proc;
    
    -- Next State Logic
    next_state_proc: process(current_state, instr_valid, interrupt)
    begin
        case current_state is
            when IDLE =>
                if interrupt = '0' then
                    next_state <= FETCH;
                else
                    next_state <= IDLE;
                end if;
                
            when FETCH =>
                if instr_valid = '1' then
                    next_state <= DECODE;
                else
                    next_state <= FETCH;
                end if;
                
            when DECODE =>
                next_state <= EXECUTE;
                
            when EXECUTE =>
                next_state <= WRITEBACK;
                
            when WRITEBACK =>
                next_state <= IDLE;
                
            when others =>
                next_state <= IDLE;
        end case;
    end process next_state_proc;

end architecture behavioral;
"""

def test_parsing_mode(mode_name, comprehensive_mode):
    """Test parsing with specified mode"""
    print(f"\n{mode_name} Parsing Test:")
    print("-" * 30)
    
    filename = 'test_cpu_core.vhd'
    
    try:
        # Create test file
        with open(filename, 'w') as f:
            f.write(full_vhdl)
        
        print("✓ Test file created")
        
        # Parse with HDLio
        hdl = HDLio(filename, VHDL_2008, comprehensive=comprehensive_mode)
        parser_info = hdl.getParserInfo()
        
        print(f"✓ Parser type: {parser_info['parser_type']}")
        print(f"✓ Comprehensive mode: {parser_info['comprehensive']}")
        
        design_units = hdl.getDesignUnits()
        print(f"✓ Parsed {len(design_units)} design units")
        
        # Analyze each design unit
        for unit in design_units:
            print(f"  Unit: {unit.name} (type: {unit.getVhdlType()})")
            
            if unit.getVhdlType() == 'entity':
                groups = unit.getPortGroups()
                print(f"    Port groups: {len(groups)}")
                
                total_ports = 0
                for group in groups:
                    ports = group.getPorts()
                    total_ports += len(ports)
                    print(f"      '{group.getName()}': {len(ports)} ports")
                
                print(f"    Total ports: {total_ports}")
            
            elif unit.getVhdlType() == 'architecture':
                print(f"    Architecture for entity: {getattr(unit, 'entity_name', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ {mode_name} parsing failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)

# Test both parsing modes
entity_focused_success = test_parsing_mode("Entity-Focused", comprehensive_mode=False)
comprehensive_success = test_parsing_mode("Comprehensive", comprehensive_mode=True)

# Summary
print(f"\n{'='*40}")
print("Test Results Summary:")
print(f"Entity-focused parsing: {'✓ PASS' if entity_focused_success else '✗ FAIL'}")
print(f"Comprehensive parsing:  {'✓ PASS' if comprehensive_success else '✗ FAIL'}")

if entity_focused_success and comprehensive_success:
    print("\n✓ All parsing modes working!")
elif entity_focused_success:
    print("\n⚠ Entity-focused parsing working, comprehensive needs implementation")
else:
    print("\n✗ Both parsing modes need attention")

print("\n✓ Comprehensive VHDL parsing test complete!") 