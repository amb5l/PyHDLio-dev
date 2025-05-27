# VHDL Test Projects Integration Plan

## Overview
Plan for integrating popular VHDL projects as git submodules to enhance testing coverage with real-world code.

## Proposed Directory Structure
```
PyHDLio/
├── tests/
│   ├── projects/                    # Test project submodules
│   │   ├── README.md               # Documentation of test projects
│   │   ├── opencores/              # OpenCores projects
│   │   │   ├── uart/               # UART implementation
│   │   │   ├── spi/                # SPI controller
│   │   │   └── cpu/                # Simple CPU core
│   │   ├── vhdl-extras/            # VHDL utility libraries
│   │   ├── neorv32/                # RISC-V processor (if VHDL)
│   │   └── ghdl-examples/          # GHDL example projects
│   └── integration/
│       └── test_real_world_projects.py  # Tests for project parsing
```

## Recommended VHDL Projects

### 1. **OpenCores Projects** (Various Licenses - Check Individual)
```bash
# UART Controller
git submodule add https://github.com/openrisc/uart tests/projects/opencores/uart

# SPI Controller  
git submodule add https://github.com/openrisc/spi tests/projects/opencores/spi

# Simple CPU cores
git submodule add https://github.com/openrisc/mor1kx tests/projects/opencores/cpu
```

### 2. **VHDL-Extras** (Apache 2.0 License - Good)
```bash
git submodule add https://github.com/kevinpt/vhdl-extras tests/projects/vhdl-extras
```

### 3. **GHDL Examples** (Various - Check)
```bash
git submodule add https://github.com/ghdl/ghdl-examples tests/projects/ghdl-examples
```

### 4. **NEORV32** (BSD-3-Clause - Good)
```bash
git submodule add https://github.com/stnolting/neorv32 tests/projects/neorv32
```

## Implementation Strategy

### Phase 1: Small Projects (Start Here)
1. **vhdl-extras** - Well-structured utility library
2. **Simple OpenCores modules** - UART, SPI controllers
3. **GHDL examples** - Small, focused examples

### Phase 2: Medium Projects
1. **Larger OpenCores projects**
2. **Academic VHDL projects**

### Phase 3: Large Projects (Performance Testing)
1. **NEORV32** - Full processor core
2. **Complex SoC projects**

## Git Submodule Best Practices

### 1. **Shallow Clones for Size**
```bash
# Add submodule with specific depth
git submodule add --depth 1 <url> <path>

# Update existing submodules with shallow fetch
git submodule update --depth 1
```

### 2. **Pin to Specific Commits**
```bash
# Navigate to submodule and checkout specific commit
cd tests/projects/vhdl-extras
git checkout <specific-commit-hash>
cd ../../..
git add tests/projects/vhdl-extras
git commit -m "Pin vhdl-extras to stable commit"
```

### 3. **Optional Submodules for CI**
```bash
# In CI, clone without submodules initially
git clone <repo-url>

# Only init submodules when needed for specific tests
git submodule update --init tests/projects/vhdl-extras
```

## Testing Integration

### 1. **Create Project-Specific Tests**
```python
# tests/integration/test_real_world_projects.py
import pytest
from pathlib import Path
from hdlio import HDLio, VHDL_2008

class TestRealWorldProjects:
    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.real_world
    def test_vhdl_extras_parsing(self):
        """Test parsing VHDL-extras library"""
        project_path = Path("tests/projects/vhdl-extras")
        if not project_path.exists():
            pytest.skip("vhdl-extras submodule not initialized")
        
        vhdl_files = list(project_path.glob("**/*.vhd"))
        assert len(vhdl_files) > 0
        
        success_count = 0
        for vhdl_file in vhdl_files[:10]:  # Test first 10 files
            try:
                hdl = HDLio(str(vhdl_file), VHDL_2008)
                design_units = hdl.getDesignUnits()
                if design_units:
                    success_count += 1
            except Exception as e:
                # Log but don't fail - some files may have dependencies
                print(f"Parsing failed for {vhdl_file}: {e}")
        
        # Should successfully parse at least 50% of files
        assert success_count >= len(vhdl_files[:10]) * 0.5
```

### 2. **Performance Benchmarks**
```python
@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.performance
def test_parsing_performance(self):
    """Benchmark parsing performance on real projects"""
    import time
    
    project_files = [
        "tests/projects/vhdl-extras/src/packages/string_ops.vhd",
        "tests/projects/opencores/uart/rtl/uart_core.vhd"
    ]
    
    for vhdl_file in project_files:
        if Path(vhdl_file).exists():
            start_time = time.time()
            hdl = HDLio(vhdl_file, VHDL_2008)
            design_units = hdl.getDesignUnits()
            parse_time = time.time() - start_time
            
            # Should parse reasonably quickly
            assert parse_time < 5.0  # 5 seconds max
            print(f"Parsed {vhdl_file} in {parse_time:.3f}s")
```

## Configuration Updates

### 1. **Update .gitignore**
```gitignore
# Test project build artifacts
tests/projects/*/build/
tests/projects/*/simulation/
tests/projects/*/*.log
tests/projects/*/work/
```

### 2. **Update pytest.ini**
```ini
markers =
    real_world: Real-world project parsing tests
    performance: Performance benchmark tests
```

### 3. **Update run_tests.py**
```python
parser.add_argument("--real-world", action="store_true", 
                   help="Run real-world project tests (requires submodules)")
parser.add_argument("--performance", action="store_true",
                   help="Run performance benchmark tests")

if args.real_world:
    cmd.extend(["-m", "real_world"])
if args.performance:
    cmd.extend(["-m", "performance"])
```

## License Compliance

### Create LICENSES.md
```markdown
# Third-Party Project Licenses

## Test Projects
- **vhdl-extras**: Apache License 2.0
- **NEORV32**: BSD 3-Clause License  
- **OpenCores UART**: LGPL (check specific project)

These projects are included only for testing purposes.
See individual project directories for full license texts.
```

## Maintenance Guidelines

### 1. **Regular Updates**
- Review submodule updates quarterly
- Test parser against updated versions
- Pin to stable releases when possible

### 2. **Size Management**
- Use `git submodule update --depth 1` for CI
- Consider archiving old test projects
- Monitor repository size impact

### 3. **Documentation**
- Document which projects are used for which test scenarios
- Maintain compatibility matrix
- Update test documentation when adding projects

## Benefits vs. Risks Assessment

### ✅ **High Benefits, Low Risk** (Recommended)
- Small, well-maintained projects (vhdl-extras)
- Projects with permissive licenses
- Active projects with good documentation

### ⚠️ **Medium Benefits, Medium Risk** (Consider Carefully)
- Large projects (full CPU cores)
- Projects with complex dependencies
- LGPL licensed projects

### ❌ **Low Benefits, High Risk** (Avoid)
- Unmaintained projects
- Projects with restrictive licenses
- Projects requiring complex build systems

## Conclusion

Adding VHDL test projects as submodules is **recommended** with careful selection and proper implementation. Start with small, well-licensed projects and gradually expand based on testing needs and parser capabilities. 