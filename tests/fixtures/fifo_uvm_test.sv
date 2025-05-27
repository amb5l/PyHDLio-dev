//==============================================================================
// Advanced SystemVerilog FIFO with UVM Verification
// Demonstrates advanced SystemVerilog and verification constructs
//==============================================================================

`include "uvm_macros.svh"
import uvm_pkg::*;

//==============================================================================
// FIFO Interface
//==============================================================================
interface fifo_if #(parameter DATA_WIDTH = 32, parameter ADDR_WIDTH = 8) (input logic clk, input logic rst_n);

    logic [DATA_WIDTH-1:0] data_in;
    logic [DATA_WIDTH-1:0] data_out;
    logic write_en;
    logic read_en;
    logic full;
    logic empty;
    logic almost_full;
    logic almost_empty;
    logic [ADDR_WIDTH:0] count;

    // Clocking blocks for verification
    clocking driver_cb @(posedge clk);
        default input #1 output #1;
        output data_in, write_en, read_en;
        input full, empty, almost_full, almost_empty, count;
    endclocking

    clocking monitor_cb @(posedge clk);
        default input #1;
        input data_in, data_out, write_en, read_en, full, empty, almost_full, almost_empty, count;
    endclocking

    // Modport declarations
    modport dut (
        input clk, rst_n, data_in, write_en, read_en,
        output data_out, full, empty, almost_full, almost_empty, count
    );

    modport driver (clocking driver_cb, input clk, rst_n);
    modport monitor (clocking monitor_cb, input clk, rst_n);

    // Assertion properties
    property p_no_write_when_full;
        @(posedge clk) disable iff (!rst_n)
        full |-> !write_en;
    endproperty

    property p_no_read_when_empty;
        @(posedge clk) disable iff (!rst_n)
        empty |-> !read_en;
    endproperty

    property p_count_consistency;
        @(posedge clk) disable iff (!rst_n)
        (write_en && !read_en && !full) |=> (count == $past(count) + 1);
    endproperty

    assert property (p_no_write_when_full) else `uvm_error("FIFO_IF", "Write attempted when FIFO is full");
    assert property (p_no_read_when_empty) else `uvm_error("FIFO_IF", "Read attempted when FIFO is empty");
    assert property (p_count_consistency) else `uvm_error("FIFO_IF", "Count inconsistency detected");

endinterface

//==============================================================================
// FIFO DUT
//==============================================================================
module fifo_dut #(
    parameter DATA_WIDTH = 32,
    parameter ADDR_WIDTH = 8,
    parameter ALMOST_FULL_THRESHOLD = 2,
    parameter ALMOST_EMPTY_THRESHOLD = 2
) (
    fifo_if.dut intf
);

    localparam DEPTH = 2**ADDR_WIDTH;

    // Internal memory
    logic [DATA_WIDTH-1:0] memory [0:DEPTH-1];

    // Pointers
    logic [ADDR_WIDTH:0] write_ptr;
    logic [ADDR_WIDTH:0] read_ptr;

    // Internal signals
    logic write_enable_internal;
    logic read_enable_internal;

    assign write_enable_internal = intf.write_en && !intf.full;
    assign read_enable_internal = intf.read_en && !intf.empty;

    // Status flags
    assign intf.full = (intf.count == DEPTH);
    assign intf.empty = (intf.count == 0);
    assign intf.almost_full = (intf.count >= (DEPTH - ALMOST_FULL_THRESHOLD));
    assign intf.almost_empty = (intf.count <= ALMOST_EMPTY_THRESHOLD);
    assign intf.count = write_ptr - read_ptr;

    // Write operation
    always_ff @(posedge intf.clk or negedge intf.rst_n) begin
        if (!intf.rst_n) begin
            write_ptr <= '0;
        end else if (write_enable_internal) begin
            memory[write_ptr[ADDR_WIDTH-1:0]] <= intf.data_in;
            write_ptr <= write_ptr + 1;
        end
    end

    // Read operation
    always_ff @(posedge intf.clk or negedge intf.rst_n) begin
        if (!intf.rst_n) begin
            read_ptr <= '0;
            intf.data_out <= '0;
        end else if (read_enable_internal) begin
            intf.data_out <= memory[read_ptr[ADDR_WIDTH-1:0]];
            read_ptr <= read_ptr + 1;
        end
    end

endmodule

//==============================================================================
// UVM Sequence Item
//==============================================================================
class fifo_item extends uvm_sequence_item;

    rand bit [31:0] data;
    rand bit write_en;
    rand bit read_en;

    // Status outputs (for monitoring)
    bit [31:0] data_out;
    bit full;
    bit empty;
    bit almost_full;
    bit almost_empty;
    bit [8:0] count;

    constraint c_valid_operation {
        write_en dist {1 := 70, 0 := 30};
        read_en dist {1 := 70, 0 := 30};
        !(write_en && read_en); // Don't do both simultaneously for simplicity
    }

    `uvm_object_utils_begin(fifo_item)
        `uvm_field_int(data, UVM_ALL_ON)
        `uvm_field_int(write_en, UVM_ALL_ON)
        `uvm_field_int(read_en, UVM_ALL_ON)
        `uvm_field_int(data_out, UVM_ALL_ON | UVM_NOCOMPARE)
        `uvm_field_int(full, UVM_ALL_ON | UVM_NOCOMPARE)
        `uvm_field_int(empty, UVM_ALL_ON | UVM_NOCOMPARE)
        `uvm_field_int(almost_full, UVM_ALL_ON | UVM_NOCOMPARE)
        `uvm_field_int(almost_empty, UVM_ALL_ON | UVM_NOCOMPARE)
        `uvm_field_int(count, UVM_ALL_ON | UVM_NOCOMPARE)
    `uvm_object_utils_end

    function new(string name = "fifo_item");
        super.new(name);
    endfunction

endclass

//==============================================================================
// UVM Driver
//==============================================================================
class fifo_driver extends uvm_driver #(fifo_item);

    `uvm_component_utils(fifo_driver)

    virtual fifo_if vif;

    function new(string name = "fifo_driver", uvm_component parent = null);
        super.new(name, parent);
    endfunction

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if (!uvm_config_db#(virtual fifo_if)::get(this, "", "fifo_vif", vif))
            `uvm_fatal("DRIVER", "Could not get interface from config db")
    endfunction

    virtual task run_phase(uvm_phase phase);
        fifo_item item;

        forever begin
            seq_item_port.get_next_item(item);
            drive_item(item);
            seq_item_port.item_done();
        end
    endtask

    virtual task drive_item(fifo_item item);
        @(vif.driver_cb);
        vif.driver_cb.data_in <= item.data;
        vif.driver_cb.write_en <= item.write_en;
        vif.driver_cb.read_en <= item.read_en;
    endtask

endclass

//==============================================================================
// UVM Monitor
//==============================================================================
class fifo_monitor extends uvm_monitor;

    `uvm_component_utils(fifo_monitor)

    virtual fifo_if vif;
    uvm_analysis_port #(fifo_item) analysis_port;

    function new(string name = "fifo_monitor", uvm_component parent = null);
        super.new(name, parent);
    endfunction

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if (!uvm_config_db#(virtual fifo_if)::get(this, "", "fifo_vif", vif))
            `uvm_fatal("MONITOR", "Could not get interface from config db")
        analysis_port = new("analysis_port", this);
    endfunction

    virtual task run_phase(uvm_phase phase);
        fifo_item item;

        forever begin
            @(vif.monitor_cb);
            item = fifo_item::type_id::create("item");
            item.data = vif.monitor_cb.data_in;
            item.write_en = vif.monitor_cb.write_en;
            item.read_en = vif.monitor_cb.read_en;
            item.data_out = vif.monitor_cb.data_out;
            item.full = vif.monitor_cb.full;
            item.empty = vif.monitor_cb.empty;
            item.almost_full = vif.monitor_cb.almost_full;
            item.almost_empty = vif.monitor_cb.almost_empty;
            item.count = vif.monitor_cb.count;

            analysis_port.write(item);
        end
    endtask

endclass

//==============================================================================
// UVM Test
//==============================================================================
class fifo_test extends uvm_test;

    `uvm_component_utils(fifo_test)

    fifo_driver driver;
    fifo_monitor monitor;
    uvm_sequencer #(fifo_item) sequencer;

    function new(string name = "fifo_test", uvm_component parent = null);
        super.new(name, parent);
    endfunction

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        driver = fifo_driver::type_id::create("driver", this);
        monitor = fifo_monitor::type_id::create("monitor", this);
        sequencer = uvm_sequencer#(fifo_item)::type_id::create("sequencer", this);
    endfunction

    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        driver.seq_item_port.connect(sequencer.seq_item_export);
    endfunction

    virtual task run_phase(uvm_phase phase);
        fifo_sequence seq;
        phase.raise_objection(this);

        seq = fifo_sequence::type_id::create("seq");
        seq.start(sequencer);

        #1000;
        phase.drop_objection(this);
    endtask

endclass

//==============================================================================
// UVM Sequence
//==============================================================================
class fifo_sequence extends uvm_sequence #(fifo_item);

    `uvm_object_utils(fifo_sequence)

    function new(string name = "fifo_sequence");
        super.new(name);
    endfunction

    virtual task body();
        fifo_item item;

        repeat(100) begin
            item = fifo_item::type_id::create("item");
            start_item(item);
            assert(item.randomize());
            finish_item(item);
        end
    endtask

endclass