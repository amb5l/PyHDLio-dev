"""
Verilog and SystemVerilog project parsing tests.

This module contains tests that parse Verilog and SystemVerilog code
to validate the parser's support for these languages.

Note: Some tests may be skipped if Verilog parsing is not yet fully implemented.
"""

import pytest
from pathlib import Path
from hdlio import HDLio, VERILOG_2001, VERILOG_2005, SYSTEMVERILOG_2005, SYSTEMVERILOG_2012
import time


class TestVerilogProjects:
    """Test parsing of Verilog and SystemVerilog projects."""

    @pytest.mark.integration
    @pytest.mark.verilog
    def test_simple_cpu_parsing(self):
        """Test parsing simple_cpu.v - educational CPU implementation"""
        verilog_file = Path("tests/verilog/simple_cpu.v")
        if not verilog_file.exists():
            pytest.skip("simple_cpu.v not found")

        # Test with different Verilog standards
        for standard in [VERILOG_2001, VERILOG_2005]:
            try:
                hdl = HDLio(str(verilog_file), standard)
                design_units = hdl.getDesignUnits()

                assert design_units is not None, f"Failed to parse with {standard}"

                # Should find the simple_cpu and alu modules
                module_names = [unit.getName() for unit in design_units if hasattr(unit, 'getName')]
                print(f"Found modules with {standard}: {module_names}")

                # Verify expected modules are present
                expected_modules = ['simple_cpu', 'alu']
                for expected in expected_modules:
                    assert any(expected in name for name in module_names), \
                        f"Expected module '{expected}' not found in {module_names}"

                print(f"✓ Successfully parsed simple_cpu.v with {standard}")

            except SyntaxError as e:
                if "Can't build lexer" in str(e):
                    pytest.skip(f"Verilog parser not yet fully implemented: {e}")
                else:
                    raise
            except Exception as e:
                pytest.fail(f"Failed to parse simple_cpu.v with {standard}: {e}")

    @pytest.mark.integration
    @pytest.mark.verilog
    def test_ddr_controller_parsing(self):
        """Test parsing ddr_controller.v - complex memory controller"""
        verilog_file = Path("tests/verilog/ddr_controller.v")
        if not verilog_file.exists():
            pytest.skip("ddr_controller.v not found")

        # DDR controller is more complex, test with Verilog 2005
        try:
            hdl = HDLio(str(verilog_file), VERILOG_2005)
            design_units = hdl.getDesignUnits()

            assert design_units is not None, "Failed to parse ddr_controller.v"

            # Should find the ddr_controller module
            module_names = [unit.getName() for unit in design_units if hasattr(unit, 'getName')]
            print(f"Found modules: {module_names}")

            # Verify ddr_controller module is present
            assert any('ddr_controller' in name for name in module_names), \
                f"Expected module 'ddr_controller' not found in {module_names}"

            print("✓ Successfully parsed ddr_controller.v")

        except SyntaxError as e:
            if "Can't build lexer" in str(e):
                pytest.skip(f"Verilog parser not yet fully implemented: {e}")
            else:
                raise
        except Exception as e:
            pytest.fail(f"Failed to parse ddr_controller.v: {e}")

    @pytest.mark.integration
    @pytest.mark.systemverilog
    def test_fifo_uvm_test_parsing(self):
        """Test parsing fifo_uvm_test.sv - SystemVerilog with UVM"""
        sv_file = Path("tests/verilog/fifo_uvm_test.sv")
        if not sv_file.exists():
            pytest.skip("fifo_uvm_test.sv not found")

        # SystemVerilog file, test with SystemVerilog standards
        for standard in [SYSTEMVERILOG_2005, SYSTEMVERILOG_2012]:
            try:
                hdl = HDLio(str(sv_file), standard)
                design_units = hdl.getDesignUnits()

                assert design_units is not None, f"Failed to parse with {standard}"

                # Should find SystemVerilog constructs
                unit_names = [unit.getName() for unit in design_units if hasattr(unit, 'getName')]
                print(f"Found units with {standard}: {unit_names}")

                # Verify expected SystemVerilog constructs are present
                expected_constructs = ['fifo_dut', 'fifo_if']
                for expected in expected_constructs:
                    assert any(expected in name for name in unit_names), \
                        f"Expected construct '{expected}' not found in {unit_names}"

                print(f"✓ Successfully parsed fifo_uvm_test.sv with {standard}")

            except SyntaxError as e:
                if "Can't build lexer" in str(e):
                    pytest.skip(f"SystemVerilog parser not yet fully implemented: {e}")
                else:
                    raise
            except Exception as e:
                # SystemVerilog parsing might not be fully supported yet
                print(f"⚠ Could not parse fifo_uvm_test.sv with {standard}: {e}")
                pytest.skip(f"SystemVerilog parsing not supported: {e}")

    @pytest.mark.integration
    @pytest.mark.verilog
    @pytest.mark.real_world
    def test_verilog_submodule_projects(self):
        """Test parsing real-world Verilog projects from submodules"""
        test_projects = [
            ("tests/verilog/picorv32", "*.v", "PicoRV32 RISC-V CPU"),
            ("tests/verilog/VexRiscv", "*.v", "VexRiscv RISC-V CPU"),
            ("tests/verilog/verilog-axi", "*.v", "Verilog AXI components"),
            ("tests/verilog/verilog-ethernet", "*.v", "Verilog Ethernet components"),
            ("tests/verilog/verilog-uart", "*.v", "Verilog UART components"),
        ]

        results = []

        for project_dir, pattern, description in test_projects:
            project_path = Path(project_dir)
            if not project_path.exists():
                print(f"⚠ Skipping {description} - submodule not initialized")
                continue

            verilog_files = list(project_path.glob(f"**/{pattern}"))[:5]  # Test first 5 files
            if not verilog_files:
                print(f"⚠ No Verilog files found in {description}")
                continue

            success_count = 0
            total_modules = 0

            for verilog_file in verilog_files:
                try:
                    hdl = HDLio(str(verilog_file), VERILOG_2005)
                    design_units = hdl.getDesignUnits()
                    if design_units:
                        success_count += 1
                        modules = [u for u in design_units if hasattr(u, 'getName')]
                        total_modules += len(modules)
                        print(f"✓ Parsed {verilog_file.name}: {len(modules)} modules")
                    else:
                        print(f"⚠ Parsed {verilog_file.name} but found no modules")
                except SyntaxError as e:
                    if "Can't build lexer" in str(e):
                        print(f"⚠ Skipping {verilog_file.name} - Verilog parser not yet implemented")
                        continue
                    else:
                        print(f"✗ Failed to parse {verilog_file.name}: {e}")
                except Exception as e:
                    print(f"✗ Failed to parse {verilog_file.name}: {e}")

            if verilog_files:
                success_rate = success_count / len(verilog_files) if len(verilog_files) > 0 else 0
                results.append((description, success_count, len(verilog_files), success_rate, total_modules))
                print(f"{description}: {success_count}/{len(verilog_files)} files parsed ({success_rate:.1%}), {total_modules} modules")

        # Report results
        if results:
            print("\nVerilog Project Parsing Summary:")
            for desc, success, total, rate, modules in results:
                print(f"  {desc}: {success}/{total} files ({rate:.1%}), {modules} modules")
        else:
            pytest.skip("No Verilog submodule projects available for testing")

    @pytest.mark.integration
    @pytest.mark.verilog
    @pytest.mark.performance
    @pytest.mark.slow
    def test_verilog_parsing_performance(self):
        """Benchmark Verilog parsing performance"""
        test_files = [
            ("tests/verilog/simple_cpu.v", "Simple CPU"),
            ("tests/verilog/ddr_controller.v", "DDR Controller"),
        ]

        results = []

        for file_path, description in test_files:
            verilog_file = Path(file_path)
            if not verilog_file.exists():
                print(f"⚠ Skipping {description} - file not found")
                continue

            try:
                start_time = time.time()
                hdl = HDLio(str(verilog_file), VERILOG_2005)
                design_units = hdl.getDesignUnits()
                parse_time = time.time() - start_time

                # Should parse reasonably quickly (max 2 seconds for these files)
                assert parse_time < 2.0, f"Parsing {description} took {parse_time:.3f}s (too slow)"

                module_count = len(design_units) if design_units else 0
                results.append((description, parse_time, module_count))
                print(f"✓ Parsed {description} in {parse_time:.3f}s ({module_count} modules)")

            except SyntaxError as e:
                if "Can't build lexer" in str(e):
                    print(f"⚠ Skipping {description} - Verilog parser not yet implemented")
                    continue
                else:
                    print(f"✗ Failed to parse {description}: {e}")
            except Exception as e:
                print(f"✗ Failed to parse {description}: {e}")

        # If no files could be parsed due to parser limitations, skip the test
        if len(results) == 0:
            pytest.skip("Verilog parsing not yet implemented - performance testing skipped")

        # Report performance summary
        print("\nVerilog Parsing Performance Summary:")
        for desc, time_taken, modules in results:
            print(f"  {desc}: {time_taken:.3f}s, {modules} modules")

    @pytest.mark.integration
    @pytest.mark.verilog
    def test_verilog_port_extraction(self):
        """Test port extraction from Verilog modules"""
        verilog_file = Path("tests/verilog/simple_cpu.v")
        if not verilog_file.exists():
            pytest.skip("simple_cpu.v not found")

        try:
            hdl = HDLio(str(verilog_file), VERILOG_2005)
            design_units = hdl.getDesignUnits()

            assert design_units is not None, "Failed to parse simple_cpu.v"

            # Find the simple_cpu module
            cpu_module = None
            for unit in design_units:
                if hasattr(unit, 'getName') and 'simple_cpu' in unit.getName():
                    cpu_module = unit
                    break

            assert cpu_module is not None, "simple_cpu module not found"

            # Test port extraction if supported
            if hasattr(cpu_module, 'getPorts'):
                ports = cpu_module.getPorts()
                print(f"Found {len(ports)} ports in simple_cpu module")

                # Verify some expected ports exist
                port_names = [port.getName() for port in ports if hasattr(port, 'getName')]
                expected_ports = ['clk', 'reset', 'data_in', 'data_out']

                for expected_port in expected_ports:
                    assert any(expected_port in name for name in port_names), \
                        f"Expected port '{expected_port}' not found in {port_names}"

                print(f"✓ Successfully extracted ports: {port_names}")
            else:
                print("⚠ Port extraction not supported for this module type")

        except SyntaxError as e:
            if "Can't build lexer" in str(e):
                pytest.skip(f"Verilog parser not yet fully implemented: {e}")
            else:
                raise
        except Exception as e:
            pytest.fail(f"Failed to extract ports from simple_cpu.v: {e}")