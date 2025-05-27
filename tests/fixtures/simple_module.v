// Simple Verilog module for unit testing
module simple_module (
    input clk,
    input reset,
    input [7:0] data_in,
    output reg [7:0] data_out
);

always @(posedge clk or posedge reset) begin
    if (reset)
        data_out <= 8'h00;
    else
        data_out <= data_in;
end

endmodule 