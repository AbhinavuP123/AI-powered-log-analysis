import pytest
import time
import random

def test_api_integration_failure():
    """Simulates a failure in a 3rd party API integration."""
    print("Connecting to API endpoint: https://api.payments.internal/v1/charge")
    time.sleep(0.5)
    print("Request Payload: {'amount': 500, 'currency': 'USD', 'customer_id': 'cust_9928'}")
    
    # Simulate a 500 Internal Server Error
    status_code = 500
    if status_code != 200:
        print(f"ERROR: API returned status code {status_code}")
        print("Response: {'error': 'Internal Server Error', 'message': 'Upstream timeout in payment gateway'}")
        raise ConnectionError(f"Failed to process payment: Upstream service returned {status_code}")

def test_database_deadlock():
    """Simulates a database deadlock during a heavy transaction."""
    print("Starting transaction for user_id: 404")
    print("Acquiring lock on 'inventory' table...")
    time.sleep(0.3)
    print("Acquiring lock on 'orders' table...")
    
    # Simulate a deadlock error
    error_msg = "Deadlock found when trying to get lock; try restarting transaction"
    print(f"DB Error: {error_msg}")
    raise RuntimeError(f"Database transaction failed: {error_msg}")

def test_config_validation_error():
    """Simulates a configuration error (missing required environment variable)."""
    required_vars = ["DB_HOST", "API_KEY", "SECRET_TOKEN"]
    current_vars = {"DB_HOST": "localhost", "API_KEY": "sk_test_123"}
    
    for var in required_vars:
        print(f"Checking environment variable: {var}")
        if var not in current_vars:
            print(f"CRITICAL: Missing required configuration: {var}")
            raise KeyError(f"Configuration Error: '{var}' is not set in the environment.")

def test_resource_leak_simulation():
    """Simulates an OS-level resource exhaustion error."""
    print("Initializing file processor...")
    open_handles = []
    try:
        for i in range(100):
            # We don't actually want to crash the system, just simulate the error log
            if i > 50:
                print(f"Failed to open handle {i}: Too many open files")
                raise OSError(24, "Too many open files")
            print(f"Opened file handle: /tmp/proc_data_{i}.tmp")
    finally:
        for h in open_handles:
            h.close()

def test_flaky_service_dependency():
    """A test that might pass or fail, showing a 'Warning' state in logs."""
    latency = random.uniform(0.1, 2.5)
    print(f"External service latency: {latency:.2f}s")
    if latency > 2.0:
        print("WARNING: Service response time is above threshold (2.0s)")
        # We fail it here for the demo
        assert latency <= 2.0, f"Service SLA breached: {latency:.2f}s > 2.0s"
    else:
        print("Service performance within limits.")
        assert True
