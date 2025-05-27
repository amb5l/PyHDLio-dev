# Quick Start: Adding VHDL Test Projects

## Phase 1: Start with the Best (Recommended Order)

### 1. Add en_cl_fix (Small, Professional, Well-Tested)
```bash
# Create projects directory
mkdir -p tests/projects

# Add en_cl_fix (MIT License - safe for commercial use)
git submodule add --depth 1 https://github.com/enclustra/en_cl_fix tests/projects/en_cl_fix
```

### 2. Add OSVVM Core Library (Industry Standard)
```bash
# Add OSVVM utility library (Apache 2.0 License)
git submodule add --depth 1 https://github.com/OSVVM/OSVVM tests/projects/osvvm
```

### 3. Add Open Logic (Modern Standard Library)
```bash
# Add Open Logic (LGPL modified for FPGA - commercial friendly)
git submodule add --depth 1 https://github.com/open-logic/open-logic tests/projects/open-logic
```

## Quick Test Implementation

### 1. Update .gitignore
```bash
# Add to .gitignore
echo "" >> .gitignore
echo "# Test project build artifacts" >> .gitignore
echo "tests/projects/*/build/" >> .gitignore
echo "tests/projects/*/simulation/" >> .gitignore
echo "tests/projects/*/*.log" >> .gitignore
echo "tests/projects/*/work/" >> .gitignore
```

### 2. Update pytest.ini
```bash
# Add these markers to pytest.ini:
# real_world: Real-world project parsing tests
# performance: Performance benchmark tests  
# en_cl_fix: en_cl_fix library tests
# osvvm: OSVVM library tests
# open_logic: Open Logic library tests
```

### 3. Create Basic Real-World Test
Create `tests/integration/test_real_world_projects.py`:

```python
import pytest
from pathlib import Path
from hdlio import HDLio, VHDL_2008

class TestRealWorldProjects:
    
    @pytest.mark.integration
    @pytest.mark.real_world
    @pytest.mark.en_cl_fix
    def test_en_cl_fix_parsing(self):
        """Test parsing en_cl_fix library"""
        project_path = Path("tests/projects/en_cl_fix")
        if not project_path.exists():
            pytest.skip("en_cl_fix submodule not initialized")
        
        # Find VHDL files
        vhdl_files = list(project_path.glob("**/*.vhd"))[:10]  # Test first 10
        
        if not vhdl_files:
            pytest.skip("No VHDL files found in en_cl_fix")
        
        success_count = 0
        for vhdl_file in vhdl_files:
            try:
                hdl = HDLio(str(vhdl_file), VHDL_2008)
                design_units = hdl.getDesignUnits()
                if design_units:
                    success_count += 1
                    print(f"✓ Parsed {vhdl_file.name}: {len(design_units)} design units")
            except Exception as e:
                print(f"✗ Failed to parse {vhdl_file.name}: {e}")
        
        # Should successfully parse at least 50% of files
        assert success_count >= len(vhdl_files) * 0.5, f"Only parsed {success_count}/{len(vhdl_files)} files"
    
    @pytest.mark.integration  
    @pytest.mark.real_world
    @pytest.mark.osvvm
    def test_osvvm_parsing(self):
        """Test parsing OSVVM library"""
        project_path = Path("tests/projects/osvvm")
        if not project_path.exists():
            pytest.skip("osvvm submodule not initialized")
        
        # OSVVM has well-structured VHDL files
        vhdl_files = list(project_path.glob("**/*.vhd"))[:15]  # Test first 15
        
        if not vhdl_files:
            pytest.skip("No VHDL files found in osvvm")
        
        success_count = 0
        entities_found = 0
        
        for vhdl_file in vhdl_files:
            try:
                hdl = HDLio(str(vhdl_file), VHDL_2008)
                design_units = hdl.getDesignUnits()
                if design_units:
                    success_count += 1
                    entities = [u for u in design_units if u.getVhdlType() == "entity"]
                    entities_found += len(entities)
                    print(f"✓ Parsed {vhdl_file.name}: {len(design_units)} units, {len(entities)} entities")
            except Exception as e:
                print(f"✗ Failed to parse {vhdl_file.name}: {e}")
        
        # OSVVM should have high success rate
        assert success_count >= len(vhdl_files) * 0.6, f"Only parsed {success_count}/{len(vhdl_files)} files"
        print(f"Found {entities_found} entities total")
```

## Update Test Runner

Add to `run_tests.py`:
```python
# Add these arguments
parser.add_argument("--real-world", action="store_true", 
                   help="Run real-world project tests (requires submodules)")

# In the command building section:
if args.real_world:
    cmd.extend(["-m", "real_world"])
```

## Usage Examples

```bash
# Initialize and test a specific project
git submodule update --init tests/projects/en_cl_fix
python run_tests.py --real-world --no-warnings

# Run only en_cl_fix tests
python -m pytest -m "real_world and en_cl_fix" -v

# Run all real-world tests (if submodules are initialized)
python run_tests.py --real-world --verbose
```

## Benefits You'll Get

1. **Real-World Testing**: Test against production VHDL code
2. **Diverse Patterns**: Different coding styles and language features
3. **Edge Case Discovery**: Find parser limitations with actual code
4. **Performance Testing**: Measure parsing speed on larger codebases
5. **Regression Prevention**: Ensure improvements don't break existing functionality

## License Safety

All recommended projects use permissive licenses:
- ✅ **MIT** (en_cl_fix): Can be used anywhere
- ✅ **Apache 2.0** (OSVVM): Can be used anywhere  
- ✅ **LGPL modified for FPGA** (Open Logic): Commercial-friendly for HDL

## Next Steps

1. **Start small**: Add just `en_cl_fix` first
2. **Test the integration**: Run the tests and ensure they work
3. **Gradually expand**: Add more projects as needed
4. **Monitor repository size**: Use `git submodule status` to check impact
5. **Document findings**: Track which projects work best for testing

This approach gives you comprehensive real-world testing while maintaining manageable complexity. 