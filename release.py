#!/usr/bin/env python3
"""
Release script for fiasto-py
This script helps prepare and publish a new release to PyPI and GitHub.
"""

import subprocess
import sys
import os
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

def get_version():
    """Get current version from pyproject.toml"""
    with open("pyproject.toml", "r") as f:
        for line in f:
            if line.startswith("version ="):
                return line.split('"')[1]
    return None

def main():
    """Main release function"""
    print("🚀 fiasto-py Release Script")
    print("=" * 50)
    
    # Get current version
    version = get_version()
    if not version:
        print("❌ Could not determine version from pyproject.toml")
        sys.exit(1)
    
    print(f"📦 Preparing release version: {version}")
    
    # Check if we're in a git repository
    if not run_command("git status", "Checking git status", check=False):
        print("❌ Not in a git repository")
        sys.exit(1)
    
    # Check for uncommitted changes
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("⚠️  You have uncommitted changes:")
        print(result.stdout)
        response = input("Continue anyway? (yes/no): ")
        if response.lower() != "yes":
            print("❌ Release cancelled")
            sys.exit(0)
    
    # Build and test
    print("\n🔨 Building and testing...")
    if not run_command("source .venv/bin/activate && PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin develop", "Building package"):
        print("❌ Build failed")
        sys.exit(1)
    
    # Test the package
    if not run_command("source .venv/bin/activate && python -c \"import fiasto_py; print('Package works!')\"", "Testing package"):
        print("❌ Package test failed")
        sys.exit(1)
    
    # Commit changes
    print(f"\n📝 Committing changes for version {version}...")
    if not run_command("git add .", "Staging changes"):
        sys.exit(1)
    
    if not run_command(f"git commit -m \"Release version {version}\"", "Committing changes"):
        sys.exit(1)
    
    # Create tag
    print(f"\n🏷️  Creating tag v{version}...")
    if not run_command(f"git tag v{version}", "Creating git tag"):
        sys.exit(1)
    
    # Push to GitHub
    print(f"\n📤 Pushing to GitHub...")
    if not run_command("git push origin main", "Pushing commits"):
        sys.exit(1)
    
    if not run_command(f"git push origin v{version}", "Pushing tag"):
        sys.exit(1)
    
    # Publish to PyPI
    print(f"\n📦 Publishing to PyPI...")
    print("⚠️  Make sure you have configured your PyPI credentials!")
    response = input("Continue with PyPI publishing? (yes/no): ")
    if response.lower() == "yes":
        if not run_command("python publish.py", "Publishing to PyPI"):
            print("❌ PyPI publishing failed")
            sys.exit(1)
    
    print(f"\n🎉 Release {version} completed successfully!")
    print(f"📦 PyPI: https://pypi.org/project/fiasto-py/")
    print(f"🏷️  GitHub: https://github.com/alexhallam/fiasto-py/releases/tag/v{version}")

if __name__ == "__main__":
    main()
