import pytest
import requests

def test_get_initial_state():
    """Test if GET /state returns a valid initial state"""
    response = requests.get("http://localhost:8197/state")
    assert response.status_code == 200
    assert response.text in ["INIT", "RUNNING", "PAUSED", "SHUTDOWN"]

def test_put_valid_state():
    """Test if PUT /state accepts valid state"""
    response = requests.put(
        "http://localhost:8197/state",
        data="RUNNING",
        headers={"Content-Type": "text/plain"}
    )
    assert response.status_code == 200
    
    # Verify state was changed
    response = requests.get("http://localhost:8197/state")
    assert response.text == "RUNNING"

def test_put_invalid_state():
    """Test if PUT /state rejects invalid state"""
    response = requests.put(
        "http://localhost:8197/state",
        data="INVALID_STATE",
        headers={"Content-Type": "text/plain"}
    )
    assert response.status_code == 400