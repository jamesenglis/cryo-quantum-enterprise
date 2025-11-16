#!/usr/bin/env python3
"""
Verify GitHub push was successful
"""
import subprocess
import sys

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🔍 Verifying GitHub Push Status")
    print("=" * 40)
    
    # Check git status
    success, stdout, stderr = run_cmd("git status")
    if success:
        if "Your branch is up to date with 'origin/main'" in stdout:
            print("✅ Git Status: Up to date with origin/main")
        else:
            print("⚠️  Git Status: Not up to date")
            print(stdout)
    else:
        print("❌ Git Status: Failed to check")
    
    # Check last commit
    success, stdout, stderr = run_cmd("git log --oneline -1")
    if success:
        print(f"✅ Last Commit: {stdout.strip()}")
    else:
        print("❌ Failed to get last commit")
    
    # Check remote
    success, stdout, stderr = run_cmd("git remote -v")
    if success:
        print("✅ Remote configured:")
        for line in stdout.strip().split('\n'):
            if 'origin' in line:
                print(f"   {line}")
    
    print("\n🎯 GitHub Repository:")
    print("   https://github.com/jamesenglis/cryo-quantum-enterprise")
    print("\n🚀 Your quantum computing project is ready to share!")

if __name__ == "__main__":
    main()
