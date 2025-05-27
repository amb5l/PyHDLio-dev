#!/usr/bin/env python3
"""
Test runner script for PyHDLio-dev

This script provides convenient ways to run different types of tests
with pytest, automatically setting up the PyHDLio core dependency.
"""

import sys
import subprocess
import argparse
from pathlib import Path

# Setup development environment to use PyHDLio core
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
        print("❌ Cannot run tests without PyHDLio core package")
        return 1
    
    parser = argparse.ArgumentParser(description="PyHDLio Test Runner")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--port-groups", action="store_true", help="Run port grouping tests only")
    parser.add_argument("--parser", action="store_true", help="Run parser tests only")
    parser.add_argument("--slow", action="store_true", help="Include slow tests")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage reporting")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--no-warnings", action="store_true", help="Disable warnings")
    parser.add_argument("--real-world", action="store_true", help="Run real-world project tests (requires submodules)")
    parser.add_argument("--performance", action="store_true", help="Run performance benchmark tests")
    
    args = parser.parse_args()
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add coverage if requested
    if args.coverage:
        cmd.extend(["--cov=hdlio", "--cov-report=html", "--cov-report=term"])
    
    # Add verbosity
    if args.verbose:
        cmd.append("-v")
    
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
    elif args.real_world:
        cmd.extend(["-m", "real_world"])
    elif args.performance:
        cmd.extend(["-m", "performance"])
    else:
        # Run all tests by default
        if not args.slow:
            cmd.extend(["-m", "not slow"])
    
    # Add tests directory
    cmd.append("tests/")
    
    # Run the tests
    success = run_command(cmd, "Test Suite")
    
    if success:
        print(f"\n✓ All tests completed successfully!")
        return 0
    else:
        print(f"\n✗ Some tests failed. See output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 