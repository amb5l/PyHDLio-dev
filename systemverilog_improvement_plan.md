# SystemVerilog Parser Improvement Plan

## Current Status ✅
- **Basic parsing infrastructure**: WORKING
- **Interface declarations**: WORKING (basic)
- **Module declarations**: WORKING (with SystemVerilog ports)
- **Package declarations**: WORKING (basic structure)

## Critical Issues to Fix 🔥

### 1. Lexical Issues
- **Missing apostrophe token** (`'0`, `'1`) - SystemVerilog fill patterns
- **Missing dollar sign token** (`$display`, `$finish`) - System tasks
- **Missing dot notation** for interface instances (`interface.modport`)

### 2. Grammar Issues
- **Modport lists**: Need to handle comma-separated port lists in modports
- **Typedef declarations**: Not properly parsing struct/enum typedefs
- **Function parameters**: Missing support for function parameter lists
- **Generate parameters**: Module parameters with `#(parameter ...)` syntax
- **Interface instances**: `interface.modport` syntax in port lists

### 3. Advanced Features Needed
- **Class declarations**: Complete class syntax support
- **Struct/Union declarations**: Packed and unpacked variants
- **Enum declarations**: With explicit values
- **Always_ff/Always_comb**: SystemVerilog-specific always blocks
- **Generate blocks**: For loops with genvar

## Implementation Priority

### Phase 1: Critical Lexical Fixes
1. Add apostrophe token for fill patterns (`'0`, `'1`)
2. Add dollar token for system tasks (`$display`)
3. Fix dot notation for interface instances

### Phase 2: Grammar Enhancements
1. Fix modport port lists
2. Implement typedef declarations
3. Enhance function/task parameter handling
4. Support module parameters syntax

### Phase 3: Advanced Features
1. Complete class declaration support
2. Full struct/union implementation
3. Comprehensive enum support
4. Generate block enhancements

## Test Results Summary
- **Interfaces**: ✅ Basic working, ⚠️ Modports need fixes
- **Modules**: ✅ Working with SystemVerilog types
- **Packages**: ✅ Basic structure, ⚠️ Content parsing needs work
- **Classes**: ❌ Need complete implementation
- **Advanced types**: ❌ Struct/Union/Enum need fixes

## Next Steps
1. Fix critical lexical issues
2. Enhance grammar rules for complex constructs
3. Add comprehensive test coverage
4. Optimize parser performance