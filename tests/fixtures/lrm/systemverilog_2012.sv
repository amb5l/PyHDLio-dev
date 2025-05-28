`define CLK_PERIOD 10
`include "defines.sv" // Assume defines.sv contains `define MAX_COUNT 10

// Package Declaration (SystemVerilog-2012)
package counter_pkg;
  parameter WIDTH = 4;
  localparam IDLE = 2'b00,
             RUNNING = 2'b01,
             STOPPED = 2'b10;

  // Class Declaration with Constraints
  class CounterTransaction;
    rand bit [WIDTH-1:0] count;
    rand bit [1:0] state;
    constraint valid_count { soft count <= `MAX_COUNT; } // Soft constraint (2012, fails 2009)
    function new();
      count = 0;
      state = IDLE;
    endfunction
    virtual function void display();
      $display("Count: %0d, State: %0b", count, state);
    endfunction
  endclass

  // Function Declaration
  function automatic logic [WIDTH-1:0] increment(logic [WIDTH-1:0] val);
    return (val < `MAX_COUNT) ? val + 1 : 0;
  endfunction

  // Task Declaration
  task automatic reset_state(output logic [1:0] out_state);
    out_state = IDLE;
  endtask
endpackage

// Interface Declaration (SystemVerilog-2012)
interface counter_if (
  input logic clk
);
  logic rst;
  logic en;
  logic [3:0] count;
  logic [1:0] state;

  modport dut (
    input clk, rst, en,
    output count, state
  );
  modport tb (
    input clk, count, state,
    output rst, en
  );

  clocking cb @(posedge clk);
    input count, state;
    output rst, en;
  endclocking
endinterface

// Module Declaration: Counter (SystemVerilog-2012)
module counter import counter_pkg::*; (
  counter_if.dut ifc
);
  // Declarative Region
  logic [WIDTH-1:0] internal_count;
  logic [1:0] next_state;
  wire internal_en;
  integer i;
  logic [7:0] mem [0:1];

  // Covergroup
  covergroup cg @(posedge ifc.clk);
    coverpoint internal_count {
      bins low = {0, 1};
      bins high = {[2:`MAX_COUNT]};
    }
    coverpoint next_state;
  endgroup
  cg cov = new();

  // Body Region
  assign internal_en = ifc.en & ~ifc.rst;
  assign ifc.count = internal_count;
  assign ifc.state = next_state;

  always @(posedge ifc.clk or posedge ifc.rst) begin
    if (ifc.rst) begin
      internal_count <= 0;
      reset_state(next_state);
      for (i = 0; i < 2; i++)
        mem[i] <= 8'h00;
    end
    else if (internal_en) begin
      internal_count <= increment(internal_count);
      unique case (next_state) // Unique case (2012, fails 2009)
        IDLE:    next_state <= (ifc.en) ? RUNNING : IDLE;
        RUNNING: next_state <= (ifc.en) ? RUNNING : STOPPED;
        STOPPED: next_state <= IDLE;
        default: next_state <= IDLE;
      endcase
    end
  end

  // Concurrent Assertion with Sequence
  sequence valid_count;
    @(posedge ifc.clk) internal_count <= `MAX_COUNT;
  endsequence
  assert property (valid_count) else $error("Count overflow");

  genvar j;
  generate
    for (j = 0; j < 2; j++) begin : mem_gen
      always @(posedge ifc.clk) begin
        if (ifc.rst)
          mem[j] <= 8'h00;
      end
    end
  endgenerate

  counter sub_inst (
    .ifc(ifc)
  );
endmodule

// Program Declaration: Testbench (SystemVerilog-2012)
program tb import counter_pkg::*; (
  counter_if.tb ifc
);
  class Test extends CounterTransaction;
    function void display();
      super.display();
    endfunction
  endclass

  Test tx;
  initial begin
    tx = new();
    ifc.rst = 1;
    #`CLK_PERIOD ifc.rst = 0;
    repeat (20) begin
      tx.randomize();
      ifc.cb.en <= tx.count[0];
      @(ifc.cb);
      tx.display();
    end
    $finish;
  end
endprogram