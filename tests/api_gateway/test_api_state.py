import pytest
import requests
import time

auth = ('admin', 'admin123')

def test_get_initial_state():
    """Test if GET /state returns a valid initial state"""
    response = requests.get("http://localhost:8198/state", auth=auth)
    assert response.status_code == 200
    assert response.text in ["INIT", "RUNNING", "PAUSED", "SHUTDOWN"]

def test_put_valid_state():
    """Test if PUT /state accepts valid state"""
    response = requests.put(
        "http://localhost:8198/state",
        data="RUNNING",
        headers={"Content-Type": "text/plain"},
        auth=auth
    )
    assert response.status_code == 200
    
    # Verify state was changed
    response = requests.get("http://localhost:8198/state", auth=auth)
    assert response.text == "RUNNING"

def test_put_invalid_state():
    """Test if PUT /state rejects invalid state"""
    response = requests.put(
        "http://localhost:8198/state",
        data="INVALID_STATE",
        headers={"Content-Type": "text/plain"},
        auth=auth
    )
    assert response.status_code == 400
    
def test_run_log():
    """Test if run-log records state transitions"""
    # Set state to RUNNING
    requests.put(
        "http://localhost:8198/state",
        data="RUNNING",
        headers={"Content-Type": "text/plain"},
        auth=auth 
    )
    
    # Verify state transition was recorded
    response = requests.get("http://localhost:8198/run-log", auth=auth)
    assert response.status_code == 200
    assert "INIT->RUNNING" in response.text
    
def test_paused_state_behavior():
    """Test if system doesn't respond when PAUSED"""
    # Set state to PAUSED
    requests.put(
        "http://localhost:8198/state",
        data="PAUSED",
        headers={"Content-Type": "text/plain"},
        auth=auth
    )
    
    # Verify system doesn't respond
    response = requests.get("http://localhost:8198/service1", auth=auth)
    assert response.status_code == 503  # Service Unavailable

def test_running_state_behavior():
    """Test if system responds normally when RUNNING"""
    # Set state to RUNNING
    requests.put(
        "http://localhost:8198/state",
        data="RUNNING",
        headers={"Content-Type": "text/plain"},
        auth=auth
    )
    
    # Verify system responds normally
    response = requests.get("http://localhost:8198/service1", auth=auth)
    assert response.status_code == 200

def test_init_state_behavior():
    """Test if system requires new login in INIT state"""
    
    # Set state to INIT
    requests.put(
        "http://localhost:8198/state",
        data="INIT",
        headers={"Content-Type": "text/plain"},
        auth=auth
    )
    
    # Verify system requires login
    response = requests.get("http://localhost:8198/service1", auth=auth)
    assert response.status_code == 401  # Unauthorized

def test_shutdown_state_behavior():
    """Test if system stops containers in SHUTDOWN state"""
    # Set state to SHUTDOWN
    requests.put(
        "http://localhost:8198/state",
        data="SHUTDOWN",
        headers={"Content-Type": "text/plain"},
        auth=auth
    )
    
    # Give time for shutdown
    time.sleep(2)
    
    # Verify system is not responding - should raise ConnectionError
    try:
        requests.get("http://localhost:8198/service1", auth=auth)
        assert False, "Server should not be responding"
    except requests.exceptions.ConnectionError:
        assert True  # Expected behavior when server shuts down