#!/usr/bin/env python3
"""
Build script for fiasto-py
This script helps build and install the Python extension module.
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False

def main():
    """Main build function"""
    print("🚀 Building fiasto-py Python extension...")
    
    # Check if maturin is installed
    if not run_command("maturin --version", "Checking maturin installation"):
        print("📦 Installing maturin...")
        if not run_command("pip install maturin", "Installing maturin"):
            print("❌ Failed to install maturin. Please install it manually: pip install maturin")
            sys.exit(1)
    
    # Build in development mode with Python 3.13 compatibility
    if not run_command("PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin develop", "Building and installing in development mode"):
        print("❌ Build failed")
        sys.exit(1)
    
    print("🎉 Build completed successfully!")
    print("\n📝 You can now import and use fiasto_py:")
    print("   import fiasto_py")
    print("   result = fiasto_py.parse_formula('y ~ x1 + x2')")
    print("   tokens = fiasto_py.lex_formula('y ~ x1 + x2')")

if __name__ == "__main__":
    main()
