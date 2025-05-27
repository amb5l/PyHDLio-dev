//==============================================================================
// DDR Memory Controller
// Complex example demonstrating memory controllers and bus interfaces
//==============================================================================

module ddr_controller #(
    parameter DATA_WIDTH = 32,
    parameter ADDR_WIDTH = 28,
    parameter BURST_LEN = 8,
    parameter ROW_WIDTH = 14,
    parameter COL_WIDTH = 10,
    parameter BANK_WIDTH = 3
) (
    // Clock and Reset
    input wire clk,
    input wire rst_n,

    // AXI4 Interface
    input wire [31:0] axi_awaddr,
    input wire [7:0] axi_awlen,
    input wire [2:0] axi_awsize,
    input wire [1:0] axi_awburst,
    input wire axi_awvalid,
    output reg axi_awready,

    input wire [DATA_WIDTH-1:0] axi_wdata,
    input wire [DATA_WIDTH/8-1:0] axi_wstrb,
    input wire axi_wlast,
    input wire axi_wvalid,
    output reg axi_wready,

    output reg [1:0] axi_bresp,
    output reg axi_bvalid,
    input wire axi_bready,

    input wire [31:0] axi_araddr,
    input wire [7:0] axi_arlen,
    input wire [2:0] axi_arsize,
    input wire [1:0] axi_arburst,
    input wire axi_arvalid,
    output reg axi_arready,

    output reg [DATA_WIDTH-1:0] axi_rdata,
    output reg [1:0] axi_rresp,
    output reg axi_rlast,
    output reg axi_rvalid,
    input wire axi_rready,

    // DDR Interface
    output reg ddr_clk_p,
    output reg ddr_clk_n,
    output reg ddr_cke,
    output reg ddr_cs_n,
    output reg ddr_ras_n,
    output reg ddr_cas_n,
    output reg ddr_we_n,
    output reg [BANK_WIDTH-1:0] ddr_ba,
    output reg [ROW_WIDTH-1:0] ddr_addr,
    inout wire [DATA_WIDTH-1:0] ddr_dq,
    inout wire [DATA_WIDTH/8-1:0] ddr_dqs,
    output reg [DATA_WIDTH/8-1:0] ddr_dm
);

// State machine states
localparam IDLE = 4'h0;
localparam PRECHARGE = 4'h1;
localparam ACTIVATE = 4'h2;
localparam READ = 4'h3;
localparam WRITE = 4'h4;
localparam AUTO_REFRESH = 4'h5;
localparam MODE_SET = 4'h6;
localparam WAIT_INIT = 4'h7;

// Internal registers
reg [3:0] state, next_state;
reg [15:0] init_counter;
reg [7:0] refresh_counter;
reg [4:0] timing_counter;

// Command queue
reg [63:0] cmd_queue [0:15];
reg [3:0] cmd_queue_head, cmd_queue_tail;
reg cmd_queue_empty, cmd_queue_full;

// Data buffer
reg [DATA_WIDTH-1:0] write_buffer [0:BURST_LEN-1];
reg [DATA_WIDTH-1:0] read_buffer [0:BURST_LEN-1];
reg [3:0] buffer_index;

// Address decode
wire [ROW_WIDTH-1:0] row_addr;
wire [COL_WIDTH-1:0] col_addr;
wire [BANK_WIDTH-1:0] bank_addr;

assign row_addr = axi_awaddr[ADDR_WIDTH-1:ADDR_WIDTH-ROW_WIDTH];
assign col_addr = axi_awaddr[COL_WIDTH+BANK_WIDTH-1:BANK_WIDTH];
assign bank_addr = axi_awaddr[BANK_WIDTH-1:0];

// DDR output enable
reg ddr_output_enable;
reg [DATA_WIDTH-1:0] ddr_output_data;

assign ddr_dq = ddr_output_enable ? ddr_output_data : {DATA_WIDTH{1'bz}};

// Initialize state machine
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        state <= WAIT_INIT;
        init_counter <= 16'd0;
        refresh_counter <= 8'd0;
        timing_counter <= 5'd0;
        cmd_queue_head <= 4'd0;
        cmd_queue_tail <= 4'd0;
        cmd_queue_empty <= 1'b1;
        cmd_queue_full <= 1'b0;

        // AXI default values
        axi_awready <= 1'b0;
        axi_wready <= 1'b0;
        axi_bresp <= 2'b00;
        axi_bvalid <= 1'b0;
        axi_arready <= 1'b0;
        axi_rdata <= {DATA_WIDTH{1'b0}};
        axi_rresp <= 2'b00;
        axi_rlast <= 1'b0;
        axi_rvalid <= 1'b0;

        // DDR default values
        ddr_clk_p <= 1'b0;
        ddr_clk_n <= 1'b1;
        ddr_cke <= 1'b0;
        ddr_cs_n <= 1'b1;
        ddr_ras_n <= 1'b1;
        ddr_cas_n <= 1'b1;
        ddr_we_n <= 1'b1;
        ddr_ba <= {BANK_WIDTH{1'b0}};
        ddr_addr <= {ROW_WIDTH{1'b0}};
        ddr_dm <= {DATA_WIDTH/8{1'b0}};
        ddr_output_enable <= 1'b0;
        ddr_output_data <= {DATA_WIDTH{1'b0}};

    end else begin
        state <= next_state;

        // Generate DDR clock
        ddr_clk_p <= ~ddr_clk_p;
        ddr_clk_n <= ~ddr_clk_n;

        // Timing counter
        if (timing_counter > 0)
            timing_counter <= timing_counter - 1;

        // Refresh counter
        refresh_counter <= refresh_counter + 1;
    end
end

// State machine logic
always @(*) begin
    next_state = state;

    case (state)
        WAIT_INIT: begin
            if (init_counter >= 16'd40000) // Wait 200us at 200MHz
                next_state = MODE_SET;
        end

        MODE_SET: begin
            if (timing_counter == 0)
                next_state = IDLE;
        end

        IDLE: begin
            if (refresh_counter >= 8'd156) // 7.8us refresh period
                next_state = AUTO_REFRESH;
            else if (!cmd_queue_empty)
                next_state = PRECHARGE;
        end

        PRECHARGE: begin
            if (timing_counter == 0)
                next_state = ACTIVATE;
        end

        ACTIVATE: begin
            if (timing_counter == 0) begin
                if (cmd_queue[cmd_queue_head][63]) // Read command
                    next_state = READ;
                else
                    next_state = WRITE;
            end
        end

        READ: begin
            if (timing_counter == 0 && buffer_index == BURST_LEN-1)
                next_state = IDLE;
        end

        WRITE: begin
            if (timing_counter == 0 && buffer_index == BURST_LEN-1)
                next_state = IDLE;
        end

        AUTO_REFRESH: begin
            if (timing_counter == 0)
                next_state = IDLE;
        end

        default: next_state = IDLE;
    endcase
end

// DDR command generation
always @(posedge clk) begin
    case (state)
        WAIT_INIT: begin
            ddr_cke <= 1'b0;
            ddr_cs_n <= 1'b1;
            init_counter <= init_counter + 1;
        end

        MODE_SET: begin
            ddr_cke <= 1'b1;
            ddr_cs_n <= 1'b0;
            ddr_ras_n <= 1'b0;
            ddr_cas_n <= 1'b0;
            ddr_we_n <= 1'b0;
            ddr_ba <= 3'b000;
            ddr_addr <= {ROW_WIDTH{1'b0}} | 14'h133; // Mode register value
            timing_counter <= 5'd2; // tMRD
        end

        PRECHARGE: begin
            ddr_cs_n <= 1'b0;
            ddr_ras_n <= 1'b0;
            ddr_cas_n <= 1'b1;
            ddr_we_n <= 1'b0;
            ddr_addr[10] <= 1'b1; // Precharge all banks
            timing_counter <= 5'd3; // tRP
        end

        ACTIVATE: begin
            ddr_cs_n <= 1'b0;
            ddr_ras_n <= 1'b0;
            ddr_cas_n <= 1'b1;
            ddr_we_n <= 1'b1;
            ddr_ba <= bank_addr;
            ddr_addr <= row_addr;
            timing_counter <= 5'd3; // tRCD
        end

        READ: begin
            if (timing_counter == 3) begin
                ddr_cs_n <= 1'b0;
                ddr_ras_n <= 1'b1;
                ddr_cas_n <= 1'b0;
                ddr_we_n <= 1'b1;
                ddr_ba <= bank_addr;
                ddr_addr <= {{ROW_WIDTH-COL_WIDTH{1'b0}}, col_addr};
                ddr_output_enable <= 1'b0;
                buffer_index <= 4'd0;
            end else if (timing_counter <= 2 && timing_counter > 0) begin
                // Read data from DDR
                read_buffer[buffer_index] <= ddr_dq;
                buffer_index <= buffer_index + 1;
            end
        end

        WRITE: begin
            if (timing_counter == 3) begin
                ddr_cs_n <= 1'b0;
                ddr_ras_n <= 1'b1;
                ddr_cas_n <= 1'b0;
                ddr_we_n <= 1'b0;
                ddr_ba <= bank_addr;
                ddr_addr <= {{ROW_WIDTH-COL_WIDTH{1'b0}}, col_addr};
                ddr_output_enable <= 1'b1;
                buffer_index <= 4'd0;
                ddr_output_data <= write_buffer[0];
            end else if (timing_counter <= 2 && timing_counter > 0) begin
                // Write data to DDR
                buffer_index <= buffer_index + 1;
                if (buffer_index < BURST_LEN-1)
                    ddr_output_data <= write_buffer[buffer_index + 1];
                else
                    ddr_output_enable <= 1'b0;
            end
        end

        AUTO_REFRESH: begin
            ddr_cs_n <= 1'b0;
            ddr_ras_n <= 1'b0;
            ddr_cas_n <= 1'b0;
            ddr_we_n <= 1'b1;
            timing_counter <= 5'd12; // tRFC
            refresh_counter <= 8'd0;
        end
    endcase
end

// AXI Write Address Channel
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        axi_awready <= 1'b0;
    end else begin
        if (axi_awvalid && !cmd_queue_full) begin
            axi_awready <= 1'b1;
            // Add write command to queue
            cmd_queue[cmd_queue_tail] <= {1'b0, 31'h0, axi_awaddr}; // Write command
            cmd_queue_tail <= cmd_queue_tail + 1;
            cmd_queue_empty <= 1'b0;
            if ((cmd_queue_tail + 1) == cmd_queue_head)
                cmd_queue_full <= 1'b1;
        end else begin
            axi_awready <= 1'b0;
        end
    end
end

// AXI Write Data Channel
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        axi_wready <= 1'b0;
    end else begin
        if (axi_wvalid && state == WRITE) begin
            axi_wready <= 1'b1;
            write_buffer[buffer_index] <= axi_wdata;
        end else begin
            axi_wready <= 1'b0;
        end
    end
end

// AXI Write Response Channel
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        axi_bvalid <= 1'b0;
        axi_bresp <= 2'b00;
    end else begin
        if (state == WRITE && next_state == IDLE) begin
            axi_bvalid <= 1'b1;
            axi_bresp <= 2'b00; // OKAY
        end else if (axi_bready && axi_bvalid) begin
            axi_bvalid <= 1'b0;
        end
    end
end

// AXI Read Address Channel
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        axi_arready <= 1'b0;
    end else begin
        if (axi_arvalid && !cmd_queue_full) begin
            axi_arready <= 1'b1;
            // Add read command to queue
            cmd_queue[cmd_queue_tail] <= {1'b1, 31'h0, axi_araddr}; // Read command
            cmd_queue_tail <= cmd_queue_tail + 1;
            cmd_queue_empty <= 1'b0;
            if ((cmd_queue_tail + 1) == cmd_queue_head)
                cmd_queue_full <= 1'b1;
        end else begin
            axi_arready <= 1'b0;
        end
    end
end

// AXI Read Data Channel
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        axi_rvalid <= 1'b0;
        axi_rdata <= {DATA_WIDTH{1'b0}};
        axi_rresp <= 2'b00;
        axi_rlast <= 1'b0;
    end else begin
        if (state == READ && buffer_index < BURST_LEN) begin
            axi_rvalid <= 1'b1;
            axi_rdata <= read_buffer[buffer_index];
            axi_rresp <= 2'b00; // OKAY
            axi_rlast <= (buffer_index == BURST_LEN-1);
        end else if (axi_rready && axi_rvalid) begin
            axi_rvalid <= 1'b0;
            axi_rlast <= 1'b0;
        end
    end
end

// Command queue management
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        cmd_queue_head <= 4'd0;
        cmd_queue_empty <= 1'b1;
        cmd_queue_full <= 1'b0;
    end else begin
        if (state == ACTIVATE && next_state != ACTIVATE) begin
            cmd_queue_head <= cmd_queue_head + 1;
            cmd_queue_full <= 1'b0;
            if ((cmd_queue_head + 1) == cmd_queue_tail)
                cmd_queue_empty <= 1'b1;
        end
    end
end

endmodule