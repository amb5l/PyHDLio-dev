//==============================================================================
// Simple 8-bit CPU Implementation
// Educational example demonstrating various Verilog constructs
//==============================================================================

module simple_cpu (
    input wire clk,
    input wire reset,
    input wire [7:0] data_in,
    output reg [7:0] data_out,
    output reg [7:0] addr_out,
    output reg read_enable,
    output reg write_enable
);

// Internal registers
reg [7:0] accumulator;
reg [7:0] program_counter;
reg [7:0] instruction_register;
reg [7:0] memory_address_register;
reg [7:0] memory_data_register;

// Control signals
reg [2:0] state;
reg [3:0] opcode;
reg [3:0] operand;

// State machine states
localparam FETCH = 3'b000;
localparam DECODE = 3'b001;
localparam EXECUTE = 3'b010;
localparam MEMORY_READ = 3'b011;
localparam MEMORY_WRITE = 3'b100;
localparam HALT = 3'b101;

// Instruction opcodes
localparam NOP = 4'b0000;
localparam LOAD_ACC = 4'b0001;
localparam STORE_ACC = 4'b0010;
localparam ADD = 4'b0011;
localparam SUB = 4'b0100;
localparam JUMP = 4'b0101;
localparam JUMP_ZERO = 4'b0110;
localparam HALT_OP = 4'b1111;

always @(posedge clk or posedge reset) begin
    if (reset) begin
        accumulator <= 8'h00;
        program_counter <= 8'h00;
        instruction_register <= 8'h00;
        memory_address_register <= 8'h00;
        memory_data_register <= 8'h00;
        state <= FETCH;
        data_out <= 8'h00;
        addr_out <= 8'h00;
        read_enable <= 1'b0;
        write_enable <= 1'b0;
    end else begin
        case (state)
            FETCH: begin
                addr_out <= program_counter;
                read_enable <= 1'b1;
                write_enable <= 1'b0;
                state <= DECODE;
            end

            DECODE: begin
                instruction_register <= data_in;
                opcode <= data_in[7:4];
                operand <= data_in[3:0];
                read_enable <= 1'b0;
                program_counter <= program_counter + 1;
                state <= EXECUTE;
            end

            EXECUTE: begin
                case (opcode)
                    NOP: begin
                        state <= FETCH;
                    end

                    LOAD_ACC: begin
                        memory_address_register <= {4'h0, operand};
                        state <= MEMORY_READ;
                    end

                    STORE_ACC: begin
                        memory_address_register <= {4'h0, operand};
                        memory_data_register <= accumulator;
                        state <= MEMORY_WRITE;
                    end

                    ADD: begin
                        memory_address_register <= {4'h0, operand};
                        state <= MEMORY_READ;
                    end

                    SUB: begin
                        memory_address_register <= {4'h0, operand};
                        state <= MEMORY_READ;
                    end

                    JUMP: begin
                        program_counter <= {4'h0, operand};
                        state <= FETCH;
                    end

                    JUMP_ZERO: begin
                        if (accumulator == 8'h00) begin
                            program_counter <= {4'h0, operand};
                        end
                        state <= FETCH;
                    end

                    HALT_OP: begin
                        state <= HALT;
                    end

                    default: begin
                        state <= FETCH;
                    end
                endcase
            end

            MEMORY_READ: begin
                addr_out <= memory_address_register;
                read_enable <= 1'b1;
                write_enable <= 1'b0;

                case (opcode)
                    LOAD_ACC: begin
                        accumulator <= data_in;
                    end
                    ADD: begin
                        accumulator <= accumulator + data_in;
                    end
                    SUB: begin
                        accumulator <= accumulator - data_in;
                    end
                endcase

                read_enable <= 1'b0;
                state <= FETCH;
            end

            MEMORY_WRITE: begin
                addr_out <= memory_address_register;
                data_out <= memory_data_register;
                read_enable <= 1'b0;
                write_enable <= 1'b1;
                write_enable <= 1'b0;
                state <= FETCH;
            end

            HALT: begin
                // Stay in halt state
                read_enable <= 1'b0;
                write_enable <= 1'b0;
            end

            default: begin
                state <= FETCH;
            end
        endcase
    end
end

endmodule

//==============================================================================
// ALU Module
//==============================================================================
module alu (
    input wire [7:0] a,
    input wire [7:0] b,
    input wire [2:0] operation,
    output reg [7:0] result,
    output reg zero_flag,
    output reg carry_flag,
    output reg overflow_flag
);

localparam ALU_ADD = 3'b000;
localparam ALU_SUB = 3'b001;
localparam ALU_AND = 3'b010;
localparam ALU_OR = 3'b011;
localparam ALU_XOR = 3'b100;
localparam ALU_SHL = 3'b101;
localparam ALU_SHR = 3'b110;

always @(*) begin
    case (operation)
        ALU_ADD: begin
            {carry_flag, result} = a + b;
            overflow_flag = (a[7] == b[7]) && (result[7] != a[7]);
        end
        ALU_SUB: begin
            {carry_flag, result} = a - b;
            overflow_flag = (a[7] != b[7]) && (result[7] != a[7]);
        end
        ALU_AND: begin
            result = a & b;
            carry_flag = 1'b0;
            overflow_flag = 1'b0;
        end
        ALU_OR: begin
            result = a | b;
            carry_flag = 1'b0;
            overflow_flag = 1'b0;
        end
        ALU_XOR: begin
            result = a ^ b;
            carry_flag = 1'b0;
            overflow_flag = 1'b0;
        end
        ALU_SHL: begin
            {carry_flag, result} = {a, 1'b0};
            overflow_flag = 1'b0;
        end
        ALU_SHR: begin
            result = {1'b0, a[7:1]};
            carry_flag = a[0];
            overflow_flag = 1'b0;
        end
        default: begin
            result = 8'h00;
            carry_flag = 1'b0;
            overflow_flag = 1'b0;
        end
    endcase

    zero_flag = (result == 8'h00);
end

endmodule