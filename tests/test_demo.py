# Test run trigger
import pytest

def test_success():
    """A test that passes."""
    assert 1 + 1 == 2

def test_failure():
    """A test that intentionally fails to trigger AI analysis."""
    expected = 42
    actual = 0
    print(f"Debug Info: Expected {expected}, but got {actual}")
    assert actual == expected, "Intentionally failing this test for AI analysis demonstration."

def test_error():
    """A test that raises an error."""
    raise ValueError("Something went wrong in the application logic!")

def test_math_error():
    """A test that causes a division by zero."""
    x = 10
    y = 0
    result = x / y
    assert result == 10

def test_data_error():
    """A test that accesses a missing key in a dictionary."""
    data = {"name": "Antigravity", "version": "1.0"}
    # Accessing a key that doesn't exist
    key = "license"
    print(f"Checking for key: {key}")
    value = data[key]
    assert value is not None

def test_type_mismatch():
    """A test that performs an invalid type operation."""
    a = "100"
    b = 50
    # This will fail because you can't add a string and an integer
    total = a + b
    assert total == 150

def test_large_output_success():
    """A test that passes but generates a lot of log output."""
    for i in range(50):
        print(f"Processing item {i}... Status: [OK]")
    assert True

def test_deep_traceback_failure():
    """A test that fails deep in a call stack to test AI's root cause analysis."""
    def level_3():
        raise RuntimeError("Critical failure in deep application logic!")
    
    def level_2():
        level_3()
        
    def level_1():
        level_2()
        
    level_1()
