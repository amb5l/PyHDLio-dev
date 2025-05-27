// Simple SystemVerilog interface and module for unit testing
interface simple_if;
    logic clk;
    logic reset;
    logic [7:0] data;
endinterface

module simple_sv_module (
    simple_if.master bus
);

always_ff @(posedge bus.clk or posedge bus.reset) begin
    if (bus.reset)
        bus.data <= 8'h00;
    else
        bus.data <= bus.data + 1;
end

endmodule 