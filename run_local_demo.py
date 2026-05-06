import subprocess
import os

def run_command(cmd):
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result

def main():
    print("Starting Local AI Log Analysis Demo\n")
    
    # 1. Run Tests
    print("Step 1: Running tests and capturing logs...")
    run_command("pytest --tb=short > pytest.log 2>&1")
    
    if os.path.exists("pytest.log"):
        print("[OK] Captured pytest.log")
    else:
        print("[ERROR] Failed to capture pytest.log")
        return

    # 2. Analyze Logs
    print("\nStep 2: Analyzing logs with AI...")
    analysis_result = run_command("python scripts/analyze_log.py pytest.log")
    print(analysis_result.stdout)
    
    if os.path.exists("summary.md"):
        print("\n[OK] Analysis Complete! Summary:")
        print("--------------------------------------------------")
        with open("summary.md", "r") as f:
            print(f.read())
        print("--------------------------------------------------")
    else:
        print("[ERROR] AI analysis failed to generate summary.md")
        print("Error Details:", analysis_result.stderr)

    print("\nTip: Run 'python run_dashboard.py' to see this in your browser!")

if __name__ == "__main__":
    main()
