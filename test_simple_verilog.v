module test_module (
    input wire clk,
    input wire reset,
    output reg [7:0] data_out
);

// Simple register
reg [7:0] counter;

// Simple always block
always @(posedge clk) begin
    if (reset) begin
        counter <= 8'h00;
    end else begin
        counter <= counter + 1;
    end
end

assign data_out = counter;

endmodule 