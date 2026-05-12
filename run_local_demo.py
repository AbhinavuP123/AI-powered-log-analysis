import subprocess
import os

def run_command(cmd):
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result

def main():
    print("Starting Enhanced Local AI Log Analysis Demo\n")
    
    # 1. Run Standard Tests
    print("Step 1a: Running standard tests...")
    run_command("python -m pytest tests/test_demo.py -vv --show-capture=all > pytest.log 2>&1")
    
    # 2. Run Complex Tests
    print("Step 1b: Running complex failure scenarios...")
    run_command("python -m pytest tests/test_complex.py -vv --show-capture=all > complex_tests.log 2>&1")
    
    # 3. Generate Service Logs
    print("Step 1c: Generating simulated backend service logs...")
    run_command("python scripts/generate_service_logs.py")
    
    # 4. Analyze All Logs
    print("\nStep 2: Analyzing all logs with AI...")
    
    log_files = ["pytest.log", "complex_tests.log", "service.log"]
    for log_file in log_files:
        if os.path.exists(log_file):
            print(f"-> Analyzing {log_file}...")
            # We don't print the full output here to keep the console clean
            analysis_result = run_command(f"python scripts/analyze_log.py {log_file}")
            print(f"   [OK] Analysis finished for {log_file}")
        else:
            print(f"   [SKIP] {log_file} not found.")

    if os.path.exists("summary.md"):
        print("\n[OK] Demo Run Complete! Check summary.md for the latest report.")
    else:
        print("\n[ERROR] AI analysis failed to generate summary.md")

    print("\nSUCCESS: Your dashboard is now populated with rich diagnostic data!")
    print("Run 'python run_dashboard.py' to see the premium visualization.")

if __name__ == "__main__":
    main()
