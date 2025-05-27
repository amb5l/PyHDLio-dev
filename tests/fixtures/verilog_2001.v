`define CLK_PERIOD 10
`include "defines.v" // Assume defines.v contains `define MAX_COUNT 10

// Module Declaration: Counter (Verilog-2001)
module counter (
  input wire clk,            // ANSI-style port (Verilog-2001, fails 1995 parser)
  input wire rst,
  input wire en,
  output reg [3:0] count,
  output reg [1:0] state
);
  // Declarative Region
  parameter WIDTH = 4;
  localparam IDLE = 2'b00,
             RUNNING = 2'b01,
             STOPPED = 2'b10;
  wire internal_en;
  integer i;
  reg [7:0] mem [0:1];

  // Function Declaration
  function automatic [WIDTH-1:0] increment; // Automatic function (Verilog-2001)
    input [WIDTH-1:0] val;
    begin
      increment = (val < `MAX_COUNT) ? val + 1 : 0;
    end
  endfunction

  // Task Declaration
  task automatic reset_state;
    output [1:0] out_state;
    begin
      out_state = IDLE;
    end
  endtask

  // Body Region
  // Continuous Assignment
  assign internal_en = en & ~rst;

  // Always Block (combinational, Verilog-2001, fails 1995 parser)
  always @* begin
    if (en)
      internal_en = 1'b1;
    else
      internal_en = 1'b0;
  end

  // Always Block (sequential)
  always @(posedge clk or posedge rst) begin
    if (rst) begin
      count <= 0;
      reset_state(state);
      for (i = 0; i < 2; i = i + 1)
        mem[i] <= 8'h00;
    end
    else if (internal_en) begin
      count <= increment(count);
      case (state)
        IDLE:    state <= (en) ? RUNNING : IDLE;
        RUNNING: state <= (en) ? RUNNING : STOPPED;
        STOPPED: state <= IDLE;
        default: state <= IDLE;
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

  // Generate Statement (Verilog-2001)
  genvar j;
  generate
    for (j = 0; j < 2; j = j + 1) begin : mem_gen
      always @(posedge clk) begin
        if (rst)
          mem[j] <= 8'h00;
      end
    end
  endgenerate

  // Module Instantiation (named mapping)
  counter sub_inst (
    .clk(clk),
    .rst(rst),
    .en(en),
    .count(),
    .state()
  );

endmodule