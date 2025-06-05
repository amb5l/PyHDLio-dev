#!/usr/bin/env python3
"""
Test Runner for PyHDLio Integration Tests
Runs comprehensive tests for the PyHDLio + pyVHDLModel integration.
"""

import unittest
import sys
import os



# Add PyHDLio package to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'PyHDLio'))

# Import all test modules
from integration.test_pyvhdlmodel_converter import TestPyVHDLModelConverter
from integration.test_enhanced_reporter import TestEnhancedReporter
from integration.test_full_integration import TestFullIntegration

def create_test_suite():
    """Create a comprehensive test suite."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add converter tests
    suite.addTests(loader.loadTestsFromTestCase(TestPyVHDLModelConverter))

    # Add reporter tests
    suite.addTests(loader.loadTestsFromTestCase(TestEnhancedReporter))

    # Add full integration tests
    suite.addTests(loader.loadTestsFromTestCase(TestFullIntegration))

    return suite

def run_tests(verbosity=2):
    """Run all tests with specified verbosity."""
    print("PyHDLio Integration Test Suite")
    print("=" * 50)

    # Check dependencies
    try:
        from pyVHDLModel.DesignUnit import Entity as PyVHDLModelEntity
        print("OK: pyVHDLModel available - full test suite will run")
    except ImportError:
        print("WARNING: pyVHDLModel not available - some tests will be skipped")

    # Check test files
    simple_vhdl = os.path.join(
        os.path.dirname(__file__), '..', 'PyHDLio', 'examples', 'vhdl', 'simple', 'simple.vhd'
    )
    if os.path.exists(simple_vhdl):
        print("OK: Test VHDL files found")
    else:
        print("WARNING: Test VHDL files missing - some tests will be skipped")

    print()

    # Create and run test suite
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    # Summary
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Skipped: {len(result.skipped)}")

    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback.split(chr(10))[-2]}")

    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback.split(chr(10))[-2]}")

    if result.skipped:
        print(f"\nSkipped {len(result.skipped)} tests (missing dependencies/files)")

    # Overall result
    if result.wasSuccessful():
        print("\nAll tests passed!")
        return True
    else:
        print("\nSome tests failed!")
        return False

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Run PyHDLio integration tests")
    parser.add_argument('-v', '--verbose', action='count', default=1,
                       help="Increase verbosity")
    parser.add_argument('-q', '--quiet', action='store_true',
                       help="Minimal output")

    args = parser.parse_args()

    if args.quiet:
        verbosity = 0
    else:
        verbosity = args.verbose

    success = run_tests(verbosity)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()