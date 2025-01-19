import pytest
import requests

def test_get_initial_state():
    """Test if GET /state returns a valid initial state"""
    response = requests.get("http://localhost:8198/state")
    assert response.status_code == 200
    assert response.text in ["INIT", "RUNNING", "PAUSED", "SHUTDOWN"]

def test_put_valid_state():
    """Test if PUT /state accepts valid state"""
    response = requests.put(
        "http://localhost:8198/state",
        data="RUNNING",
        headers={"Content-Type": "text/plain"}
    )
    assert response.status_code == 200
    
    # Verify state was changed
    response = requests.get("http://localhost:8198/state")
    assert response.text == "RUNNING"

def test_put_invalid_state():
    """Test if PUT /state rejects invalid state"""
    response = requests.put(
        "http://localhost:8198/state",
        data="INVALID_STATE",
        headers={"Content-Type": "text/plain"}
    )
    assert response.status_code == 400
    
def test_run_log():
    """Test if run-log records state transitions"""
    # Set state to RUNNING
    requests.put(
        "http://localhost:8198/state",
        data="RUNNING",
        headers={"Content-Type": "text/plain"}
    )
    
    # Verify state transition was recorded
    response = requests.get("http://localhost:8198/run-log")
    assert response.status_code == 200
    assert "INIT->RUNNING" in response.text
    
def test_paused_state_behavior():
    """Test if system doesn't respond when PAUSED"""
    # Set state to PAUSED
    requests.put(
        "http://localhost:8198/state",
        data="PAUSED",
        headers={"Content-Type": "text/plain"}
    )
    
    # Verify system doesn't respond
    response = requests.get("http://localhost:8198/service1")
    assert response.status_code == 503  # Service Unavailable

def test_running_state_behavior():
    """Test if system responds normally when RUNNING"""
    # Set state to RUNNING
    requests.put(
        "http://localhost:8198/state",
        data="RUNNING",
        headers={"Content-Type": "text/plain"}
    )
    
    # Verify system responds normally
    response = requests.get("http://localhost:8198/service1")
    assert response.status_code == 200