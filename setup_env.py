#!/usr/bin/env python3
"""
Environment Setup Script for PyHDLio-dev
Automates the creation and setup of a development environment.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description=None):
    """Run a command and handle errors."""
    if description:
        print(f">> {description}")

    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(f"   OK: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ERROR: {e.stderr.strip() if e.stderr else str(e)}")
        return False

def check_git_submodules():
    """Check if git submodules are initialized."""
    pyhdlio_path = Path("PyHDLio")
    pyvhdlmodel_path = Path("PyHDLioVHDLModel")

    if not (pyhdlio_path.exists() and pyvhdlmodel_path.exists()):
        print(">> Initializing git submodules...")
        if not run_command("git submodule update --init --recursive"):
            print("ERROR: Failed to initialize git submodules")
            return False
        print("   OK: Git submodules initialized")
    else:
        print("OK: Git submodules already present")

    return True

def setup_virtual_environment():
    """Set up virtual environment and install packages."""
    venv_path = Path(".venv")

    if not venv_path.exists():
        print(">> Creating virtual environment...")
        if not run_command(f"{sys.executable} -m venv .venv"):
            print("ERROR: Failed to create virtual environment")
            return False
        print("   OK: Virtual environment created")
    else:
        print("OK: Virtual environment already exists")

    # Determine activation command based on OS
    if os.name == 'nt':  # Windows
        activate_cmd = r".venv\Scripts\activate"
        pip_cmd = r".venv\Scripts\pip"
    else:  # Unix/Linux/macOS
        activate_cmd = "source .venv/bin/activate"
        pip_cmd = ".venv/bin/pip"

    print(">> Installing packages...")

    # Install all requirements (consolidated into one file)
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing all requirements"):
        return False

    print("   OK: All packages installed successfully")
    return True

def verify_installation():
    """Verify that the installation worked correctly."""
    print(">> Verifying installation...")

    # Determine python command in venv
    if os.name == 'nt':  # Windows
        python_cmd = r".venv\Scripts\python"
    else:  # Unix/Linux/macOS
        python_cmd = ".venv/bin/python"

    # Test basic imports
    imports_to_test = [
        "from pyhdlio.vhdl.model import Document, VHDLSyntaxError",
        "import pyVHDLModel",
    ]

    for test_import in imports_to_test:
        if not run_command(f'{python_cmd} -c "{test_import}"'):
            print(f"   ERROR: Failed to import: {test_import}")
            return False

    print("   OK: All imports successful")

    # Run a quick test
    if not run_command(f"{python_cmd} tests/run_tests.py -q", "Running integration tests"):
        print("   WARNING: Some tests failed, but basic installation is working")
    else:
        print("   OK: All tests passed!")

    return True

def main():
    """Main setup function."""
    print("PyHDLio-dev Environment Setup")
    print("=" * 40)

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("ERROR: Please run this script from the PyHDLio-dev root directory")
        sys.exit(1)

    # Step 1: Check git submodules
    if not check_git_submodules():
        sys.exit(1)

    # Step 2: Set up virtual environment and install packages
    if not setup_virtual_environment():
        sys.exit(1)

    # Step 3: Verify installation
    if not verify_installation():
        print("WARNING: Installation completed but verification failed")
        print("   You may need to debug the setup manually")

    print("\nSETUP COMPLETED SUCCESSFULLY!")
    print("\nNext steps:")
    if os.name == 'nt':  # Windows
        print("  1. Activate the environment: .venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("  1. Activate the environment: source .venv/bin/activate")
    print("  2. Run tests: python tests/run_tests.py")
    print("  3. Start developing!")

if __name__ == "__main__":
    main()
