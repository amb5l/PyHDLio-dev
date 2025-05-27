# Submodule Configuration Summary

## Overview

The PyHDLio repository now has a properly configured submodule structure for all test projects, with real-world HDL projects configured as git submodules and simple example projects as regular directories.

## Current Submodule Structure

### VHDL Submodules (`tests/vhdl/`)
All VHDL test projects are configured as git submodules:

- **en_cl_fix** - Enclustra fixed-point library
  - URL: https://github.com/enclustra/en_cl_fix
  - License: MIT
  - Professional VHDL fixed-point arithmetic library

- **osvvm** - OSVVM verification library
  - URL: https://github.com/OSVVM/OSVVM
  - License: Apache 2.0
  - Advanced VHDL verification methodology

- **open-logic** - Open Logic library
  - URL: https://github.com/open-logic/open-logic
  - License: LGPL+FPGA
  - Collection of VHDL components and utilities

### Verilog/SystemVerilog Submodules (`tests/verilog/`)
Real-world Verilog/SystemVerilog projects are configured as git submodules:

- **picorv32** - Size-optimized RISC-V CPU
  - URL: https://github.com/YosysHQ/picorv32.git
  - Maintainer: YosysHQ
  - Compact RISC-V processor implementation

- **VexRiscv** - FPGA-friendly RISC-V CPU
  - URL: https://github.com/SpinalHDL/VexRiscv.git
  - Maintainer: SpinalHDL
  - High-performance RISC-V processor

- **opentitan** - Google's OpenTitan security chip
  - URL: https://github.com/lowRISC/opentitan.git
  - Maintainer: lowRISC
  - Open-source silicon root of trust


  - Maintainer: Princeton University
  - Research manycore processor platform

- **basejump_stl** - SystemVerilog Template Library
  - URL: https://github.com/bespoke-silicon-group/basejump_stl.git
  - Maintainer: Bespoke Silicon Group
  - ASIC design template library

- **verilog-axi** - AXI4 bus components
  - URL: https://github.com/alexforencich/verilog-axi.git
  - Maintainer: Alex Forencich
  - Collection of AXI4 interface components

- **verilog-ethernet** - Ethernet components
  - URL: https://github.com/alexforencich/verilog-ethernet.git
  - Maintainer: Alex Forencich
  - Ethernet MAC and PHY implementations

- **verilog-uart** - UART communication modules
  - URL: https://github.com/alexforencich/verilog-uart.git
  - Maintainer: Alex Forencich
  - UART transmitter and receiver modules

### Regular Directories (Non-Submodules)
Simple example projects remain as regular directories:

- **simple_cpu** - Basic CPU implementation for testing
- **memory_controller** - DDR memory controller example
- **systemverilog_advanced** - Advanced SystemVerilog features demo

### Core Dependencies
- **hdlio/submodules/ply** - PLY (Python Lex-Yacc) parser library
  - URL: https://github.com/dabeaz/ply.git
  - Required for HDL parsing functionality

## Benefits of This Configuration

### 1. **Proper Version Control**
- Real-world projects track upstream changes
- Easy to update to latest versions
- Maintains project history and attribution

### 2. **Reduced Repository Size**
- Submodules are not included in main repository size
- Users can choose which projects to clone
- Faster initial clone times

### 3. **Clear Separation**
- Real-world projects (submodules) vs examples (regular dirs)
- Easy to identify external vs internal code
- Proper licensing attribution

### 4. **Easy Maintenance**
- Upstream updates can be pulled easily
- No need to manually sync changes
- Consistent with git best practices

## Usage Instructions

### Fresh Clone
```bash
git clone https://github.com/your-org/PyHDLio.git
cd PyHDLio
git submodule update --init --recursive
```

### Update Submodules
```bash
git submodule update --remote
```

### Add New Submodule
```bash
git submodule add <repository-url> <path>
```

## Troubleshooting

### Submodule Initialization Issues
If you encounter submodule initialization errors:

1. Ensure you have proper network access to GitHub
2. Check if SSH keys are configured (some submodules may use SSH)
3. Use `git submodule update --init --recursive` to initialize all submodules
4. For specific submodule issues, check the individual project's requirements

### SSH vs HTTPS
Most submodules use HTTPS URLs for broader compatibility. Some nested submodules within projects may use SSH and require proper SSH key configuration.

## Project Statistics

- **Total Submodules**: 12
- **VHDL Projects**: 3 submodules
- **Verilog/SystemVerilog Projects**: 8 submodules + 3 regular directories
- **Core Dependencies**: 1 submodule (PLY)

This configuration provides comprehensive test coverage while maintaining clean separation between external projects and internal examples.