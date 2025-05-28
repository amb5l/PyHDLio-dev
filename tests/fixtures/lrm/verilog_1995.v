`define CLK_PERIOD 10
`include "defines.v" // Assume defines.v contains `define MAX_COUNT 10

// Module Declaration: Counter (Verilog-1995)
module counter (clk, rst, en, count, state);
  // Port Declarations (non-ANSI, Verilog-1995 style)
  input clk;          // Clock input
  input rst;          // Reset input
  input en;           // Enable input
  output [3:0] count; // Counter output
  output [1:0] state; // State output

  // Declarative Region
  parameter WIDTH = 4;        // Parameter
  reg [WIDTH-1:0] count;      // Output register
  reg [1:0] state;            // Output register
  wire internal_en;           // Internal wire
  integer i;                  // Integer variable
  reg [7:0] mem [0:1];        // Memory array
  localparam IDLE = 2'b00,    // Local parameter
             RUNNING = 2'b01,
             STOPPED = 2'b10;

  // Function Declaration
  function [WIDTH-1:0] increment;
    input [WIDTH-1:0] val;
    begin
      increment = (val < `MAX_COUNT) ? val + 1 : 0;
    end
  endfunction

  // Task Declaration
  task reset_state;
    output [1:0] out_state;
    begin
      out_state = IDLE;
    end
  endtask

  // Body Region
  // Continuous Assignment
  assign internal_en = en & ~rst;

  // Always Block (procedural)
  always @(posedge clk or posedge rst) begin
    if (rst) begin
      count = 0;
      reset_state(state);
      for (i = 0; i < 2; i = i + 1)
        mem[i] = 8'h00;
    end
    else if (internal_en) begin
      count = increment(count);
      case (state)
        IDLE:    state = (en) ? RUNNING : IDLE;
        RUNNING: state = (en) ? RUNNING : STOPPED;
        STOPPED: state = IDLE;
        default: state = IDLE;
      endcase
    end
  end

  // Initial Block
  initial begin
    count = 0;
    state = IDLE;
    mem[0] = 8'hFF;
    mem[1] = 8'hFF;
  end

  // Module Instantiation
  counter sub_inst (
    .clk(clk),
    .rst(rst),
    .en(en),
    .count(),
    .state()
  );

endmodule