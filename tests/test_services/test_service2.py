import pytest
import requests

def test_service2_system_info():
    """Test if service2's system info endpoint responds"""
    response = requests.get("http://localhost:5000/system_info")
    data = response.json()
    
    assert response.status_code == 200
    assert "IP Address" in data
    assert "Running Processes" in data
    assert "Disk Space" in data
    assert "Uptime" in data

def test_service2_stop():
    """Test if service2's stop endpoint responds correctly"""
    response = requests.post("http://localhost:5000/stop")
    data = response.json()
    
    assert response.status_code == 200
    assert "message" in data
    assert "Stopping service2..." in data["message"]