-- VHDL-2008 Example: Comprehensive Design Units and Constructs
-- Uses VHDL-2008 features like simplified sensitivity lists and fixed-point types

-- Context clause (legal for package)
library ieee;
use ieee.std_logic_1164.all;
use ieee.fixed_pkg.all; -- VHDL-2008 fixed-point package
use work.all;

-- Package Declaration
package example_pkg is
  -- Declarative Region
  constant CLK_PERIOD : time := 10 ns;
  type state_t is (IDLE, RUNNING, STOPPED);
  subtype small_int is integer range 0 to 15;
  type int_array is array (0 to 3) of integer;
  
  -- Generic type (VHDL-2008)
  type generic_matrix is array (natural range <>) of std_logic_vector;
  
  -- Protected type for shared variable
  type shared_counter_t is protected
    procedure increment;
    function get_value return small_int;
  end protected shared_counter_t;
  
  shared variable shared_count : shared_counter_t;
  function max(a, b : integer) return integer;
  procedure reset_signal(signal sig : out std_logic);
  component counter
    generic (
      WIDTH : positive
    );
    port (
      clk, rst, en : in std_logic;
      count : out ufixed(3 downto 0) -- Fixed-point type
    );
  end component;
end package example_pkg;

-- Package Body
package body example_pkg is
  type shared_counter_t is protected body
    variable count : small_int := 0;
    procedure increment is
    begin
      count := count + 1;
    end procedure;
    function get_value return small_int is
    begin
      return count;
    end function;
  end protected body shared_counter_t;

  function max(a, b : integer) return integer is
  begin
    return a when a > b else b;
  end function max;

  procedure reset_signal(signal sig : out std_logic) is
  begin
    sig <= '0';
  end procedure reset_signal;
end package body example_pkg;

-- Context clause (legal for entity)
library ieee;
use ieee.std_logic_1164.all;
use ieee.fixed_pkg.all;
use work.example_pkg.all;

-- Entity Declaration
entity counter is
  generic (
    type T; -- Generic type (VHDL-2008)
    MAX_COUNT : small_int := 10
  );
  port (
    clk : in std_logic;
    rst : in std_logic;
    en : in std_logic;
    count : out ufixed(3 downto 0);
    state : out state_t
  );
end entity counter;

-- Context clause (legal for architecture)
library ieee;
use ieee.std_logic_1164.all;
use ieee.fixed_pkg.all;
use work.example_pkg.all;

-- Architecture Declaration
architecture behavioral of counter is
  -- Declarative Region
  signal internal_count : ufixed(3 downto 0);
  signal next_state : state_t;
  constant DELAY : time := 2 ns;
  type memory_t is array (0 to 1) of generic_matrix(7 downto 0); -- VHDL-2008
  signal mem : memory_t;
  attribute synthesis : boolean;
  attribute synthesis of internal_count : signal is true;

  procedure update_state(current : state_t; enable : std_logic; out_state : out state_t) is
  begin
    case current is
      when IDLE => out_state := RUNNING when enable = '1' else IDLE;
      when RUNNING => out_state := STOPPED when enable = '0' else RUNNING;
      when STOPPED => out_state := IDLE;
    end case;
  end procedure;

begin
  -- Body Region
  count_proc : process (all) -- Simplified sensitivity list (VHDL-2008)
    variable temp_count : ufixed(3 downto 0);
  begin
    if rst = '1' then
      internal_count <= (others => '0');
      temp_count := (others => '0');
      shared_count.increment; -- Protected shared variable
      next_state <= IDLE;
    elsif rising_edge(clk) then
      if en = '1' then
        if temp_count < MAX_COUNT then
          temp_count := temp_count + 1.0;
        else
          temp_count := (others => '0');
        end if;
        internal_count <= temp_count;
        update_state(next_state, en, next_state);
      end if;
    end if;
  end process;

  -- Conditional signal assignment (VHDL-2008 allows in sequential regions)
  with en select
    count <= internal_count when '1',
             (others => '0') when others;

  -- Concurrent procedure call
  reset_signal(rst);

  -- Block statement with guard (VHDL-2008)
  blk : block (en = '1')
    signal local_sig : std_logic;
  begin
    local_sig <= guarded clk;
  end block;

  -- Generate statement
  gen_mem : for i in 0 to 1 generate
    mem(i) <= (others => '0') when rst = '1' else (others => '1');
  end generate;

  -- Component instantiation with generic map
  inst : counter
    generic map (
      WIDTH => 4
    )
    port map (
      clk => clk,
      rst => rst,
      en => en,
      count => open
    );

  -- Assertion statement
  assert internal_count <= MAX_COUNT
    report "Count overflow" severity warning;

end architecture behavioral;

-- Context clause (legal for configuration)
library ieee;
use ieee.std_logic_1164.all;
use work.example_pkg.all;

-- Configuration Declaration
configuration counter_cfg of counter is
  for behavioral
    for inst : counter
      use entity work.counter(behavioral)
        generic map (WIDTH => 4);
    end for;
  end for;
end configuration counter_cfg;