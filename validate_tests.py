#!/usr/bin/env python3
"""
Test Validation Script

Quick validation that the test environment is properly set up
and can access the local PyHDLio directory.
"""

import sys
import os
from pathlib import Path

def validate_environment():
    """Validate that the test environment is properly configured"""
    print("PyHDLio Test Environment Validation")
    print("=" * 40)
    
    # Check if local PyHDLio directory exists
    current_dir = Path(__file__).parent
    pyhdlio_path = current_dir / "PyHDLio"
    hdlio_package_path = pyhdlio_path / "hdlio"
    
    if not pyhdlio_path.exists():
        print(f"❌ Local PyHDLio directory not found at: {pyhdlio_path}")
        return False
    
    if not hdlio_package_path.exists():
        print(f"❌ hdlio package not found at: {hdlio_package_path}")
        return False
    
    print(f"✅ Found local PyHDLio at: {pyhdlio_path}")
    print(f"✅ Found hdlio package at: {hdlio_package_path}")
    
    # Add to path and test import
    sys.path.insert(0, str(pyhdlio_path))
    
    try:
        import hdlio
        print(f"✅ Successfully imported hdlio from: {hdlio.__file__}")
    except ImportError as e:
        print(f"❌ Failed to import hdlio: {e}")
        return False
    
    # Check test directory structure
    tests_dir = current_dir / "tests"
    if not tests_dir.exists():
        print(f"❌ Tests directory not found at: {tests_dir}")
        return False
    
    print(f"✅ Found tests directory at: {tests_dir}")
    
    # Check for key test files
    key_test_files = [
        "tests/conftest.py",
        "tests/unit/test_parser.py",
        "tests/unit/test_port_groups.py",
        "tests/integration/test_comprehensive_parsing.py",
        "tests/integration/test_hdlio_integration.py"
    ]
    
    for test_file in key_test_files:
        test_path = current_dir / test_file
        if test_path.exists():
            print(f"✅ Found {test_file}")
        else:
            print(f"❌ Missing {test_file}")
            return False
    
    # Check that root-level test files have been removed
    legacy_files = [
        "test_current_implementation.py",
        "test_entity_only.py", 
        "test_unified_parser.py",
        "test_comprehensive.py",
        "test_comprehensive_vhdl.py"
    ]
    
    removed_count = 0
    for legacy_file in legacy_files:
        legacy_path = current_dir / legacy_file
        if not legacy_path.exists():
            removed_count += 1
        else:
            print(f"⚠️  Legacy file still exists: {legacy_file}")
    
    print(f"✅ Removed {removed_count}/{len(legacy_files)} legacy test files")
    
    # Check test runner
    test_runner = current_dir / "run_tests.py"
    if test_runner.exists():
        print(f"✅ Found test runner at: {test_runner}")
    else:
        print(f"❌ Test runner not found at: {test_runner}")
        return False
    
    return True

def main():
    """Main validation function"""
    if validate_environment():
        print("\n🎉 Test environment validation successful!")
        print("✅ Tests are configured to use local PyHDLio directory")
        print("✅ Legacy test files have been cleaned up")
        print("✅ Organized test structure is in place")
        print("\nYou can now run tests with:")
        print("  python run_tests.py")
        print("  python run_tests.py --help")
        return 0
    else:
        print("\n❌ Test environment validation failed!")
        print("Please check the issues above and fix them.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 