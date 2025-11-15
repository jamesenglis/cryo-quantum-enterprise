#!/usr/bin/env python3
"""
Enterprise Dependency Verification Script
"""
import importlib
import sys

def check_package(package_name, import_name=None):
    name = import_name or package_name
    try:
        module = importlib.import_module(name)
        version = getattr(module, '__version__', 'Unknown version')
        print(f"✅ {package_name:20} {version:15} - OK")
        return True
    except ImportError as e:
        print(f"❌ {package_name:20} {'':15} - FAILED: {e}")
        return False

def main():
    print("🔬 Verifying Enterprise Quantum Computing Stack")
    print("=" * 50)
    
    packages = [
        ("numpy", "numpy"),
        ("scipy", "scipy"), 
        ("matplotlib", "matplotlib"),
        ("pandas", "pandas"),
        ("qutip", "qutip"),
        ("jax", "jax"),
        ("fastapi", "fastapi"),
        ("pydantic", "pydantic"),
        ("pytest", "pytest"),
    ]
    
    success = all(check_package(*pkg) for pkg in packages)
    
    if success:
        print("\n🎉 ALL DEPENDENCIES INSTALLED SUCCESSFULLY!")
    else:
        print("\n⚠️  Some dependencies failed to install.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
