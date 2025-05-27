#!/usr/bin/env python3
"""
PEP-8 checking script for PyHDLio
Excludes PLY and submodules as requested.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_pep8_check():
    """Run PEP-8 checking on PyHDLio main code."""
    print("🔍 Running PEP-8 checks on PyHDLio (excluding PLY and submodules)...")
    print("=" * 70)
    
    # Ensure we're in the right directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if flake8 is available
    try:
        result = subprocess.run(['python', '-m', 'flake8', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"Using flake8: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ flake8 not found. Install with: pip install flake8")
        return False
    
    # Run flake8 on main PyHDLio code
    targets = [
        'PyHDLio/',  # Main PyHDLio package
        'run_tests.py'  # Root test runner
    ]
    
    cmd = ['python', '-m', 'flake8'] + targets
    
    try:
        result = subprocess.run(cmd, check=False, capture_output=False)
        
        if result.returncode == 0:
            print("\n✅ No PEP-8 violations found!")
            return True
        else:
            print(f"\n⚠️  Found PEP-8 violations (exit code: {result.returncode})")
            print("\nTo fix these issues:")
            print("1. Review the violations above")
            print("2. Fix them manually or use autopep8:")
            print("   pip install autopep8")
            print("   autopep8 --in-place --recursive PyHDLio/")
            print("3. Re-run this script to verify fixes")
            return False
            
    except Exception as e:
        print(f"❌ Error running flake8: {e}")
        return False


def main():
    """Main function."""
    print("PyHDLio PEP-8 Checker")
    print("Excludes PLY and submodules as configured in .flake8")
    print()
    
    success = run_pep8_check()
    
    if success:
        print("\n🎉 PEP-8 checking completed successfully!")
        return 0
    else:
        print("\n💡 Tip: The .flake8 configuration file controls what is checked.")
        print("   It excludes PLY-related code and submodules as requested.")
        return 1


if __name__ == '__main__':
    sys.exit(main()) 