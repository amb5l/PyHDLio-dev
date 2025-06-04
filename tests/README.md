# PyHDLio Integration Test Suite

This directory contains comprehensive tests for the PyHDLio + pyVHDLModel integration implementation.

## Test Structure

### Core Test Modules

1. **`test_integration/test_pyvhdlmodel_converter.py`** - Tests the PyVHDLModel converter
   - Entity conversion (AST → pyVHDLModel)
   - Generic conversion with proper Expression types
   - Port conversion with Mode mapping
   - Port group preservation
   - Error handling and edge cases

2. **`test_integration/test_enhanced_reporter.py`** - Tests the enhanced reporter with function overloads
   - AST entity reporting
   - pyVHDLModel entity reporting
   - Function overload dispatch
   - Type detection accuracy
   - Port grouping consistency across approaches

3. **`test_integration/test_full_integration.py`** - Tests complete integration pipeline
   - End-to-end AST pipeline (Parse → Report)
   - End-to-end pyVHDLModel pipeline (Parse → Convert → Report)
   - Dual pipeline consistency
   - Information preservation
   - Performance baseline

## Running Tests

### Quick Run
```bash
python tests/run_tests.py
```

### With Verbose Output
```bash
python tests/run_tests.py -v
```

### Individual Test Modules
```bash
python -m unittest tests.test_integration.test_pyvhdlmodel_converter
python -m unittest tests.test_integration.test_enhanced_reporter
python -m unittest tests.test_integration.test_full_integration
```

### From Project Root
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_integration/test_pyvhdlmodel_converter.py

# Run with verbose output
python -m pytest tests/ -v
```

## Test Coverage

### ✅ PyVHDLModel Converter (`test_pyvhdlmodel_converter.py`)
- **Converter Initialization**: Mode mapping setup
- **Entity Conversion**: Complete entity structure conversion
- **Generic Conversion**: Integer, string, and enumeration literals
- **Port Conversion**: Mode mapping (in/out/inout)
- **Port Grouping**: Source proximity preservation
- **Error Handling**: Graceful handling of invalid data
- **Edge Cases**: Empty values, whitespace, negative numbers
- **End-to-End**: Complete parsing → conversion pipeline

### ✅ Enhanced Reporter (`test_enhanced_reporter.py`)
- **AST Reporting**: All reporter functions with AST entities
- **pyVHDLModel Reporting**: All reporter functions with pyVHDLModel entities
- **Function Overloads**: Type-based dispatch verification
- **Consistency**: Same API across object types
- **Port Grouping**: Consistent grouping between approaches
- **Error Handling**: Empty entities and invalid inputs
- **Formatting**: Indentation and structure consistency

### ✅ Full Integration (`test_full_integration.py`)
- **AST Pipeline**: Parse → Report (lightweight approach)
- **pyVHDLModel Pipeline**: Parse → Convert → Report (rich approach)
- **Consistency**: Both pipelines produce equivalent results
- **Information Preservation**: No data loss in conversion
- **Port Grouping**: Perfect preservation through pipeline
- **Generic Preservation**: Types and defaults maintained
- **Port Mode Preservation**: Correct mode mapping
- **Error Resilience**: Graceful degradation
- **Performance**: Baseline timing checks

## Test Results Summary

**Total Tests**: 29
**Categories**:
- Converter Tests: 12
- Reporter Tests: 11
- Integration Tests: 6

**Dependencies Handled**:
- Tests automatically skip when pyVHDLModel not available
- Tests skip when test files missing
- Graceful error handling throughout

## Key Validation Points

### 🔧 Converter Validation
- ✅ Entity names preserved
- ✅ Generic count and types correct
- ✅ Port count and modes correct
- ✅ Port grouping structure maintained
- ✅ Default value expressions properly typed
- ✅ Error conditions handled gracefully

### 📊 Reporter Validation
- ✅ Same function names work with both AST and pyVHDLModel
- ✅ Function overload dispatch works correctly
- ✅ Report content consistent between approaches
- ✅ Port grouping visualization identical
- ✅ Indentation and formatting consistent

### 🔄 Integration Validation
- ✅ Complete pipeline from VHDL file to final report
- ✅ No information loss in AST → pyVHDLModel conversion
- ✅ Port groups perfectly preserved
- ✅ Both approaches produce equivalent meaningful results
- ✅ Performance acceptable for target use cases

## Expected Output

When all tests pass, you should see:
```
🧪 PyHDLio Integration Test Suite
==================================================
✅ pyVHDLModel available - full test suite will run
✅ Test VHDL files found

.............................
----------------------------------------------------------------------
Ran 29 tests in 0.114s

OK

==================================================
🎯 Test Results Summary:
   Tests run: 29
   Failures: 0
   Errors: 0
   Skipped: 0

🎉 All tests passed!
```

This validates that the complete PyHDLio + pyVHDLModel integration is working correctly with port grouping preservation, function overloads, and seamless dual-mode VHDL analysis.