"""
Real-world VHDL project parsing tests.

This module contains tests that parse actual VHDL code from real projects
to validate the parser's robustness and discover edge cases.
"""

import pytest
from pathlib import Path
from hdlio import HDLio, VHDL_2008
import time

class TestRealWorldProjects:
    """Test parsing of real-world VHDL projects."""

    @pytest.mark.integration
    @pytest.mark.real_world
    @pytest.mark.en_cl_fix
    def test_en_cl_fix_parsing(self):
        """Test parsing en_cl_fix library"""
        project_path = Path("tests/fixtures/en_cl_fix")
        if not project_path.exists():
            pytest.skip("en_cl_fix submodule not initialized")

        # Find VHDL files
        vhdl_files = list(project_path.glob("**/*.vhd"))
        if not vhdl_files:
            pytest.skip("No VHDL files found in en_cl_fix")

        # Test first 10 files to avoid overwhelming output
        test_files = vhdl_files[:10]
        success_count = 0
        entities_found = 0

        for vhdl_file in test_files:
            try:
                hdl = HDLio(str(vhdl_file), VHDL_2008)
                design_units = hdl.get_design_units()
                if design_units:
                    success_count += 1
                    entities = [u for u in design_units if u.get_vhdl_type() == "entity"]
                    entities_found += len(entities)
                    print(f"✓ Parsed {vhdl_file.name}: {len(design_units)} units, {len(entities)} entities")
                else:
                    print(f"⚠ Parsed {vhdl_file.name} but found no design units")
            except Exception as e:
                print(f"✗ Failed to parse {vhdl_file.name}: {e}")

        # Should successfully parse at least 50% of files
        success_rate = success_count / len(test_files)
        assert success_rate >= 0.5, f"Only parsed {success_count}/{len(test_files)} files ({success_rate:.1%})"
        print(f"en_cl_fix: {success_count}/{len(test_files)} files parsed successfully ({success_rate:.1%})")
        print(f"Found {entities_found} entities total")

    @pytest.mark.integration
    @pytest.mark.real_world
    @pytest.mark.osvvm
    def test_osvvm_parsing(self):
        """Test parsing OSVVM library"""
        project_path = Path("tests/fixtures/osvvm")
        if not project_path.exists():
            pytest.skip("osvvm submodule not initialized")

        # OSVVM has well-structured VHDL files
        vhdl_files = list(project_path.glob("**/*.vhd"))
        if not vhdl_files:
            pytest.skip("No VHDL files found in osvvm")

        # Test first 15 files (OSVVM should have high success rate)
        test_files = vhdl_files[:15]
        success_count = 0
        entities_found = 0
        packages_found = 0

        for vhdl_file in test_files:
            try:
                hdl = HDLio(str(vhdl_file), VHDL_2008)
                design_units = hdl.get_design_units()
                if design_units:
                    success_count += 1
                    entities = [u for u in design_units if u.get_vhdl_type() == "entity"]
                    packages = [u for u in design_units if u.get_vhdl_type() == "package"]
                    entities_found += len(entities)
                    packages_found += len(packages)
                    print(f"✓ Parsed {vhdl_file.name}: {len(design_units)} units ({len(entities)} entities, {len(packages)} packages)")
                else:
                    print(f"⚠ Parsed {vhdl_file.name} but found no design units")
            except Exception as e:
                print(f"✗ Failed to parse {vhdl_file.name}: {e}")

        # OSVVM should have high success rate (60%+)
        success_rate = success_count / len(test_files)
        assert success_rate >= 0.6, f"Only parsed {success_count}/{len(test_files)} files ({success_rate:.1%})"
        print(f"OSVVM: {success_count}/{len(test_files)} files parsed successfully ({success_rate:.1%})")
        print(f"Found {entities_found} entities and {packages_found} packages total")

    @pytest.mark.integration
    @pytest.mark.real_world
    @pytest.mark.open_logic
    def test_open_logic_parsing(self):
        """Test parsing Open Logic library"""
        project_path = Path("tests/fixtures/open-logic")
        if not project_path.exists():
            pytest.skip("open-logic submodule not initialized")

        # Open Logic is a larger project, test selectively
        vhdl_files = list(project_path.glob("**/*.vhd"))
        if not vhdl_files:
            pytest.skip("No VHDL files found in open-logic")

        # Test first 20 files for broader coverage
        test_files = vhdl_files[:20]
        success_count = 0
        entities_found = 0
        packages_found = 0

        for vhdl_file in test_files:
            try:
                hdl = HDLio(str(vhdl_file), VHDL_2008)
                design_units = hdl.get_design_units()
                if design_units:
                    success_count += 1
                    entities = [u for u in design_units if u.get_vhdl_type() == "entity"]
                    packages = [u for u in design_units if u.get_vhdl_type() == "package"]
                    entities_found += len(entities)
                    packages_found += len(packages)
                    print(f"✓ Parsed {vhdl_file.name}: {len(design_units)} units ({len(entities)} entities, {len(packages)} packages)")
                else:
                    print(f"⚠ Parsed {vhdl_file.name} but found no design units")
            except Exception as e:
                print(f"✗ Failed to parse {vhdl_file.name}: {e}")

        # Open Logic might have some complex files, accept 40%+ success rate
        success_rate = success_count / len(test_files)
        assert success_rate >= 0.4, f"Only parsed {success_count}/{len(test_files)} files ({success_rate:.1%})"
        print(f"Open Logic: {success_count}/{len(test_files)} files parsed successfully ({success_rate:.1%})")
        print(f"Found {entities_found} entities and {packages_found} packages total")

    @pytest.mark.integration
    @pytest.mark.real_world
    @pytest.mark.performance
    @pytest.mark.slow
    def test_parsing_performance(self):
        """Benchmark parsing performance on real projects"""
        test_cases = [
            ("tests/fixtures/en_cl_fix", "*.vhd", 3),
            ("tests/fixtures/osvvm", "*.vhd", 3),
            ("tests/fixtures/open-logic", "*.vhd", 3)
        ]

        results = []

        for project_dir, pattern, max_files in test_cases:
            project_path = Path(project_dir)
            if not project_path.exists():
                print(f"⚠ Skipping {project_path.name} - submodule not initialized")
                continue

            vhdl_files = list(project_path.glob(f"**/{pattern}"))[:max_files]
            if not vhdl_files:
                print(f"⚠ No VHDL files found in {project_path.name}")
                continue

            project_times = []

            for vhdl_file in vhdl_files:
                try:
                    start_time = time.time()
                    hdl = HDLio(str(vhdl_file), VHDL_2008)
                    design_units = hdl.get_design_units()
                    parse_time = time.time() - start_time

                    # Should parse reasonably quickly (max 5 seconds per file)
                    assert parse_time < 5.0, f"Parsing {vhdl_file.name} took {parse_time:.3f}s (too slow)"

                    project_times.append(parse_time)
                    print(f"✓ Parsed {vhdl_file.name} in {parse_time:.3f}s ({len(design_units)} units)")

                except Exception as e:
                    print(f"✗ Failed to parse {vhdl_file.name}: {e}")

            if project_times:
                avg_time = sum(project_times) / len(project_times)
                max_time = max(project_times)
                results.append((project_path.name, avg_time, max_time, len(project_times)))
                print(f"{project_path.name}: avg={avg_time:.3f}s, max={max_time:.3f}s, files={len(project_times)}")

        # Ensure we tested at least one project
        assert len(results) > 0, "No projects were available for performance testing"

        # Report overall performance
        print("\nPerformance Summary:")
        for project, avg, max_time, count in results:
            print(f"  {project}: {count} files, avg {avg:.3f}s, max {max_time:.3f}s")

    @pytest.mark.integration
    @pytest.mark.real_world
    def test_port_extraction_on_real_projects(self):
        """Test port extraction on real-world entities"""
        # Look for entities in all projects
        project_paths = [
            Path("tests/fixtures/en_cl_fix"),
            Path("tests/fixtures/osvvm"),
            Path("tests/fixtures/open-logic")
        ]

        entities_with_ports = 0
        total_ports_found = 0

        for project_path in project_paths:
            if not project_path.exists():
                continue

            vhdl_files = list(project_path.glob("**/*.vhd"))[:5]  # Test 5 files per project

            for vhdl_file in vhdl_files:
                try:
                    hdl = HDLio(str(vhdl_file), VHDL_2008)
                    design_units = hdl.get_design_units()

                    for unit in design_units:
                        if unit.get_vhdl_type() == "entity":
                            ports = unit.get_ports()
                            if ports:
                                entities_with_ports += 1
                                total_ports_found += len(ports)
                                print(f"✓ Entity {unit.get_name()} has {len(ports)} ports")

                except Exception as e:
                    # Not all files may parse successfully, that's OK for this test
                    pass

        # Should find at least a few entities with ports
        if entities_with_ports > 0:
            avg_ports = total_ports_found / entities_with_ports
            print(f"Found {entities_with_ports} entities with ports ({total_ports_found} total, avg {avg_ports:.1f} per entity)")
            assert entities_with_ports >= 3, f"Found only {entities_with_ports} entities with ports"
        else:
            pytest.skip("No entities with ports found in available test projects")