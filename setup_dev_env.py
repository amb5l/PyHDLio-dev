#!/usr/bin/env python3
"""
PyHDLio Development Environment Setup

This script sets up the development environment to use the core PyHDLio package
from the adjacent directory.
"""

import os
import sys
from pathlib import Path

def check_pyhdlio_core():
    """Check if PyHDLio core package is available in local directory."""
    current_dir = Path(__file__).parent
    pyhdlio_core_path = current_dir / "PyHDLio"  # Local PyHDLio directory
    hdlio_package_path = pyhdlio_core_path / "hdlio"
    
    if not pyhdlio_core_path.exists():
        print(f"❌ PyHDLio core directory not found at: {pyhdlio_core_path}")
        print("   Please ensure PyHDLio is in the local directory.")
        return False
    
    if not hdlio_package_path.exists():
        print(f"❌ hdlio package not found at: {hdlio_package_path}")
        print("   Please ensure PyHDLio contains the hdlio package.")
        return False
    
    print(f"✅ Found PyHDLio core at: {pyhdlio_core_path}")
    print(f"✅ Found hdlio package at: {hdlio_package_path}")
    
    # Add PyHDLio to Python path if not already there
    pyhdlio_str = str(pyhdlio_core_path)
    if pyhdlio_str not in sys.path:
        sys.path.insert(0, pyhdlio_str)
        print(f"✅ Added {pyhdlio_str} to Python path")
    
    return True

def verify_import():
    """Verify that hdlio can be imported."""
    try:
        import hdlio
        print(f"✅ Successfully imported hdlio from: {hdlio.__file__}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import hdlio: {e}")
        return False

def main():
    """Main setup function."""
    print("PyHDLio Development Environment Setup")
    print("=" * 40)
    
    if not check_pyhdlio_core():
        sys.exit(1)
    
    if not verify_import():
        sys.exit(1)
    
    print("\n🎉 Development environment setup complete!")
    print("You can now run tests and development scripts.")

if __name__ == "__main__":
    main() 