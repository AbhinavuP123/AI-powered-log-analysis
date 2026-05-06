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
