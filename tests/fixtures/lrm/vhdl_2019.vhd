-- VHDL-2019 Example: Comprehensive Design Units and Constructs
-- Uses VHDL-2019 features like interfaces and conditional analysis

-- Context clause (legal for package)
library ieee;
use ieee.std_logic_1164.all;
use ieee.fixed_pkg.all;
use work.all;

-- Package Declaration
package example_pkg is
  -- Declarative Region
  constant CLK_PERIOD : time := 10 ns;
  type state_t is (IDLE, RUNNING, STOPPED);
  subtype small_int is integer range 0 to 15;

  -- Interface declaration (VHDL-2019)
  interface counter_if is
    clk, rst, en : in std_logic;
    count : out ufixed(3 downto 0);
  end interface;

  -- Protected type
  type shared_counter_t is protected
    procedure increment;
    function get_value return small_int;
  end protected shared_counter_t;

  shared variable shared_count : shared_counter_t;
  function max(a, b : integer) return integer;
  procedure reset_signal(signal sig : out std_logic);
  component counter
    generic (
      type T;
      WIDTH : positive
    );
    port (
      ifc : counter_if
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
    type T;
    MAX_COUNT : small_int := 10
  );
  port (
    ifc : counter_if -- VHDL-2019 interface
  );
end entity counter;

-- Context clause (legal for architecture)
library ieee;
use ieee.std_logic_1164.all;
use ieee.fixed_pkg.all;
use work.example_pkg.all;

-- Conditional Analysis (VHDL-2019)
`if SIMULATION then
library sim_lib;
use sim_lib.test_utils.all;
`end if

-- Architecture Declaration
architecture behavioral of counter is
  -- Declarative Region
  signal internal_count : ufixed(3 downto 0);
  signal next_state : state_t;
  constant DELAY : time := 2 ns;
  type memory_t is array (0 to 1) of generic_matrix(7 downto 0);
  signal mem : memory_t;
  attribute synthesis : boolean;
  attribute synthesis of internal_count : signal is true;

  procedure update_state(current : state_t; enable : std_logic; out_state : out state_t) is
  begin
    case? current is -- VHDL-2019 case? (matching case)
      when IDLE => out_state := RUNNING when enable = '1' else IDLE;
      when RUNNING => out_state := STOPPED when enable = '0' else RUNNING;
      when STOPPED => out_state := IDLE;
      when others => out_state := IDLE;
    end case?;
  end procedure;

begin
  -- Body Region
  count_proc : process (all)
    variable temp_count : ufixed(3 downto 0);
  begin
    if ifc.rst = '1' then
      internal_count <= (others => '0');
      temp_count := (others => '0');
      shared_count.increment;
      next_state <= IDLE;
    elsif rising_edge(ifc.clk) then
      if ifc.en = '1' then
        if temp_count < MAX_COUNT then
          temp_count := temp_count + 1.0;
        else
          temp_count := (others => '0');
        end if;
        internal_count <= temp_count;
        update_state(next_state, ifc.en, next_state);
      end if;
    end if;
  end process;

  -- Interface-based assignment
  ifc.count <= internal_count;

  -- Concurrent procedure call
  reset_signal(ifc.rst);

  -- Block statement
  blk : block (ifc.en = '1')
    signal local_sig : std_logic;
  begin
    local_sig <= guarded ifc.clk;
  end block;

  -- Generate statement with conditional analysis
  `if SYNTHESIS generate
  gen_mem : for i in 0 to 1 generate
    mem(i) <= (others => '0') when ifc.rst = '1' else (others => '1');
  end generate;
  `end if

  -- Component instantiation
  inst : counter
    generic map (
      T => std_logic,
      WIDTH => 4
    )
    port map (
      ifc => ifc
    );

  -- Assertion with VHPI (VHDL-2019)
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
        generic map (T => std_logic, WIDTH => 4);
    end for;
  end for;
end configuration counter_cfg;