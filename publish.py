#!/usr/bin/env python3
"""
Publish script for fiasto-py
This script helps build and publish the package to PyPI.
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def run_command(cmd, description, check=True):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
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

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if maturin is installed
    if not run_command("maturin --version", "Checking maturin installation", check=False):
        print("📦 Installing maturin...")
        if not run_command("pip install maturin", "Installing maturin"):
            print("❌ Failed to install maturin. Please install it manually: pip install maturin")
            return False
    
    # Check if twine is installed
    if not run_command("twine --version", "Checking twine installation", check=False):
        print("📦 Installing twine...")
        if not run_command("pip install twine", "Installing twine"):
            print("❌ Failed to install twine. Please install it manually: pip install twine")
            return False
    
    return True

def clean_build(skip_build=False):
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous build artifacts...")
    
    # Remove dist directory only if not skipping build
    if not skip_build and os.path.exists("dist"):
        shutil.rmtree("dist")
        print("✅ Removed dist/ directory")
    
    # Remove target directory only if not skipping build
    if not skip_build and os.path.exists("target"):
        shutil.rmtree("target")
        print("✅ Removed target/ directory")
    
    # Remove any .egg-info directories
    for item in Path(".").glob("*.egg-info"):
        if item.is_dir():
            shutil.rmtree(item)
            print(f"✅ Removed {item} directory")

def build_package():
    """Build the package for distribution"""
    print("🔨 Building package for distribution...")
    
    # Build with maturin (with Python 3.13 compatibility)
    cmd = "PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin build --release"
    if not run_command(cmd, "Building package with maturin"):
        return False
    
    # Create dist directory and copy wheels
    if not os.path.exists("dist"):
        os.makedirs("dist")
    
    # Copy wheels from target/wheels to dist
    wheels_dir = Path("target/wheels")
    if wheels_dir.exists():
        for wheel_file in wheels_dir.glob("*.whl"):
            shutil.copy2(wheel_file, "dist/")
            print(f"✅ Copied {wheel_file.name} to dist/")
    
    return True

def check_package():
    """Check the built package"""
    print("🔍 Checking built package...")
    
    # Check if dist directory exists and has files
    if not os.path.exists("dist"):
        print("❌ dist/ directory not found")
        return False
    
    dist_files = list(Path("dist").glob("*"))
    if not dist_files:
        print("❌ No files found in dist/ directory")
        return False
    
    print(f"✅ Found {len(dist_files)} files in dist/:")
    for file in dist_files:
        print(f"   - {file.name}")
    
    # Check package with twine
    if not run_command("twine check dist/*", "Checking package with twine"):
        return False
    
    return True

def publish_to_pypi(test=False):
    """Publish to PyPI"""
    if test:
        print("🚀 Publishing to Test PyPI...")
        cmd = "twine upload --repository testpypi dist/*"
        url = "https://test.pypi.org/project/fiasto-py/"
    else:
        print("🚀 Publishing to PyPI...")
        cmd = "twine upload dist/*"
        url = "https://pypi.org/project/fiasto-py/"
    
    if not run_command(cmd, f"Publishing to {'Test PyPI' if test else 'PyPI'}"):
        return False
    
    print(f"🎉 Package published successfully!")
    print(f"📦 View your package at: {url}")
    
    if test:
        print("\n📝 To install from Test PyPI:")
        print("   pip install --index-url https://test.pypi.org/simple/ fiasto-py")
    else:
        print("\n📝 To install from PyPI:")
        print("   pip install fiasto-py")
    
    return True

def main():
    """Main publish function"""
    print("🚀 fiasto-py PyPI Publishing Script")
    print("=" * 50)
    
    # Parse command line arguments
    test_pypi = "--test" in sys.argv
    skip_build = "--skip-build" in sys.argv
    skip_check = "--skip-check" in sys.argv
    
    if test_pypi:
        print("🧪 Publishing to Test PyPI")
    else:
        print("📦 Publishing to PyPI")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Clean previous builds
    clean_build(skip_build=skip_build)
    
    # Build package
    if not skip_build:
        if not build_package():
            print("❌ Build failed")
            sys.exit(1)
    
    # Check package
    if not skip_check:
        if not check_package():
            print("❌ Package check failed")
            sys.exit(1)
    
    # Confirm before publishing
    if not test_pypi:
        print("\n⚠️  You are about to publish to PyPI!")
        print("   This will make the package publicly available.")
        response = input("   Are you sure you want to continue? (yes/no): ")
        if response.lower() != "yes":
            print("❌ Publishing cancelled")
            sys.exit(0)
    
    # Publish
    if not publish_to_pypi(test=test_pypi):
        print("❌ Publishing failed")
        sys.exit(1)
    
    print("\n🎉 All done!")

if __name__ == "__main__":
    print("Usage:")
    print("  python publish.py              # Publish to PyPI")
    print("  python publish.py --test       # Publish to Test PyPI")
    print("  python publish.py --skip-build # Skip building (use existing dist/)")
    print("  python publish.py --skip-check # Skip package checking")
    print()
    main()
