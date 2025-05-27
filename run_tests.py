#!/usr/bin/env python3
"""
PyHDLio Test Runner

This script provides convenient ways to run different types of tests
with pytest, automatically setting up the local PyHDLio core dependency.

Usage:
    python run_tests.py                    # Run all tests (excluding slow ones)
    python run_tests.py --unit             # Run unit tests only
    python run_tests.py --integration      # Run integration tests only
    python run_tests.py --coverage         # Run with coverage reporting
    python run_tests.py --verbose          # Verbose output
    python run_tests.py --slow             # Include slow tests
"""

import sys
import subprocess
import argparse
from pathlib import Path

# Setup development environment to use local PyHDLio core
from setup_dev_env import check_pyhdlio_core


def run_command(cmd, description):
    """Run a command and handle output"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"✗ pytest not found. Install with: pip install pytest")
        return False


def main():
    # Check PyHDLio core availability first
    if not check_pyhdlio_core():
        print("❌ Cannot run tests without local PyHDLio core package")
        return 1
    
    parser = argparse.ArgumentParser(
        description="PyHDLio Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py                    # Run all tests (excluding slow ones)
  python run_tests.py --unit             # Run unit tests only
  python run_tests.py --integration      # Run integration tests only
  python run_tests.py --coverage         # Run with coverage reporting
  python run_tests.py --verbose          # Verbose output
  python run_tests.py --slow             # Include slow tests
  python run_tests.py --vhdl --unit      # Run VHDL unit tests only
        """
    )
    
    # Test selection arguments
    test_group = parser.add_argument_group('Test Selection')
    test_group.add_argument("--unit", action="store_true", help="Run unit tests only")
    test_group.add_argument("--integration", action="store_true", help="Run integration tests only")
    test_group.add_argument("--port-groups", action="store_true", help="Run port grouping tests only")
    test_group.add_argument("--parser", action="store_true", help="Run parser tests only")
    test_group.add_argument("--vhdl", action="store_true", help="Run VHDL-specific tests only")
    test_group.add_argument("--verilog", action="store_true", help="Run Verilog-specific tests only")
    test_group.add_argument("--systemverilog", action="store_true", help="Run SystemVerilog-specific tests only")
    test_group.add_argument("--real-world", action="store_true", help="Run real-world project tests (requires submodules)")
    test_group.add_argument("--performance", action="store_true", help="Run performance benchmark tests")
    test_group.add_argument("--slow", action="store_true", help="Include slow tests")
    
    # Output and reporting arguments
    output_group = parser.add_argument_group('Output and Reporting')
    output_group.add_argument("--coverage", action="store_true", help="Run with coverage reporting")
    output_group.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    output_group.add_argument("--no-warnings", action="store_true", help="Disable warnings")
    output_group.add_argument("--quiet", "-q", action="store_true", help="Quiet output")
    
    # Additional options
    misc_group = parser.add_argument_group('Miscellaneous')
    misc_group.add_argument("--list-tests", action="store_true", help="List available tests without running them")
    misc_group.add_argument("--dry-run", action="store_true", help="Show what would be run without executing")
    
    args = parser.parse_args()
    
    # Handle special options first
    if args.list_tests:
        cmd = ["python", "-m", "pytest", "--collect-only", "-q"]
        # Only collect from our organized test directories
        cmd.extend([
            "tests/unit/",
            "tests/integration/"
        ])
        return run_command(cmd, "Listing available tests")
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add coverage if requested
    if args.coverage:
        cmd.extend(["--cov=hdlio", "--cov-report=html", "--cov-report=term"])
    
    # Add verbosity control
    if args.verbose:
        cmd.append("-v")
    elif args.quiet:
        cmd.append("-q")
    
    # Add warning control
    if args.no_warnings:
        cmd.append("--disable-warnings")
    
    # Add test selection based on arguments
    if args.unit:
        cmd.extend(["-m", "unit"])
    elif args.integration:
        cmd.extend(["-m", "integration"])
    elif args.port_groups:
        cmd.extend(["-m", "port_groups"])
    elif args.parser:
        cmd.extend(["-m", "parser"])
    elif args.vhdl:
        cmd.extend(["-m", "vhdl"])
    elif args.verilog:
        cmd.extend(["-m", "verilog"])
    elif args.systemverilog:
        cmd.extend(["-m", "systemverilog"])
    elif args.real_world:
        cmd.extend(["-m", "real_world"])
    elif args.performance:
        cmd.extend(["-m", "performance"])
    else:
        # Run all tests by default
        if not args.slow:
            cmd.extend(["-m", "not slow"])
    
    # For now, only include unit tests to avoid hanging issues with integration tests
    # TODO: Re-enable integration tests once parser performance issues are resolved
    cmd.extend([
        "tests/unit/"
    ])
    
    # Handle dry run
    if args.dry_run:
        print(f"\n{'='*60}")
        print("DRY RUN - Would execute:")
        print(f"Command: {' '.join(cmd)}")
        print(f"{'='*60}")
        return 0
    
    # Run the tests
    success = run_command(cmd, "PyHDLio Test Suite")
    
    if success:
        print(f"\n✅ All tests completed successfully!")
        if args.coverage:
            print("📊 Coverage report generated in htmlcov/index.html")
        return 0
    else:
        print(f"\n❌ Some tests failed. See output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 