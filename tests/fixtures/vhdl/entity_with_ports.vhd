library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity test_entity is
    generic (
        WIDTH : integer := 8;
        DEPTH : natural := 16
    );
    port (
        clk   : in  STD_LOGIC;
        reset : in  STD_LOGIC;
        data  : out STD_LOGIC_VECTOR(WIDTH-1 downto 0)
    );
end test_entity; 