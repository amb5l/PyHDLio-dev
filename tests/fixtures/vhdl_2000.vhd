-- VHDL-2000 Example: Comprehensive Design Units and Constructs
-- Includes protected types and shared variables that may fail VHDL-2008 parsing

-- Context clause (legal for package)
library ieee;
use ieee.std_logic_1164.all;
use work.all;

-- Package Declaration
package example_pkg is
  -- Declarative Region
  constant CLK_PERIOD : time := 10 ns;
  type state_t is (IDLE, RUNNING, STOPPED);
  subtype small_int is integer range 0 to 15;
  type int_array is array (0 to 3) of integer;
  
  -- Protected type for shared variable (VHDL-2000)
  type shared_counter_t is protected
    procedure increment;
    function get_value return small_int;
  end protected shared_counter_t;
  
  shared variable shared_count : shared_counter_t; -- Shared variable
  function max(a, b : integer) return integer;
  procedure reset_signal(signal sig : out std_logic);
  component counter
    port (
      clk, rst, en : in std_logic;
      count : out small_int
    );
  end component;
end package example_pkg;

-- Package Body
package body example_pkg is
  -- Protected type body
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
use work.example_pkg.all;

-- Entity Declaration
entity counter is
  generic (
    MAX_COUNT : small_int := 10
  );
  port (
    clk : in std_logic;
    rst : in std_logic;
    en : in std_logic;
    count : out small_int;
    state : out state_t
  );
end entity counter;

-- Context clause (legal for architecture)
library ieee;
use ieee.std_logic_1164.all;
use work.example_pkg.all;

-- Architecture Declaration
architecture behavioral of counter is
  -- Declarative Region
  signal internal_count : small_int;
  signal next_state : state_t;
  constant DELAY : time := 2 ns;
  type memory_t is array (0 to 1) of std_logic_vector(7 downto 0);
  signal mem : memory_t;
  attribute synthesis : boolean;
  attribute synthesis of internal_count : signal is true;

  -- Shared variable (may fail VHDL-2008 parsing)
  shared variable local_shared : shared_counter_t;

  procedure update_state(current : state_t; enable : std_logic; out_state : out state_t) is
  begin
    case current is
      when IDLE => out_state := RUNNING if enable = '1';
      when RUNNING => out_state := STOPPED if enable = '0';
      when STOPPED => out_state := IDLE;
    end case;
  end procedure;

begin
  -- Body Region
  count_proc : process (clk, rst)
    variable temp_count : small_int;
  begin
    if rst = '1' then
      internal_count <= 0;
      temp_count := 0;
      local_shared.increment; -- Use shared variable
      next_state <= IDLE;
    elsif rising_edge(clk) then
      if en = '1' then
        if temp_count < MAX_COUNT then
          temp_count := temp_count + 1;
        else
          temp_count := 0;
        end if;
        internal_count <= temp_count;
        local_shared.increment; -- Shared variable access
        update_state(next_state, en, next_state);
      end if;
    end if;
  end process;

  -- Concurrent signal assignment with shared variable (problematic in VHDL-2008)
  count <= local_shared.get_value after DELAY;

  -- Concurrent procedure call
  reset_signal(rst);

  -- Conditional signal assignment
  state <= next_state when en = '1' else IDLE;

  -- Block statement
  blk : block
    signal local_sig : std_logic;
  begin
    local_sig <= clk and en;
  end block;

  -- Generate statement
  gen_mem : for i in 0 to 1 generate
    mem(i) <= (others => '0') when rst = '1' else (others => '1');
  end generate;

  -- Component instantiation
  inst : counter
    port map (
      clk => clk,
      rst => rst,
      en => en,
      count => open
    );

end architecture behavioral;

-- Context clause (legal for configuration)
library ieee;
use ieee.std_logic_1164.all;
use work.example_pkg.all;

-- Configuration Declaration
configuration counter_cfg of counter is
  for behavioral
    for inst : counter
      use entity work.counter(behavioral);
    end for;
  end for;
end configuration counter_cfg;