-- Test VHDL entity with port groups
library ieee;
use ieee.std_logic_1164.all;

entity my_entity is
  port (
    -- Clock and Reset group
    clk : in std_logic;
    rst_n : in std_logic;
    
    -- Data group
    data_in : in std_logic_vector(7 downto 0);
    data_out : out std_logic_vector(7 downto 0);
    
    -- Control group  
    enable : in std_logic;
    ready : out std_logic
  );
end entity my_entity;

architecture rtl of my_entity is
begin
  -- Implementation would go here
end architecture rtl; 