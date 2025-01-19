import pytest
import requests

# authentication
auth = ('admin', 'admin123')

@pytest.fixture(autouse=True)
def ensure_running_state():
    """Ensure system is in RUNNING state before each test"""
    requests.put(
        "http://localhost:8198/state",
        data="RUNNING",
        headers={"Content-Type": "text/plain"},
        auth=auth
    )

def test_service2_data_in_response():
    """Test if service2's data is included in the response"""
    response = requests.get("http://localhost:8198/service1", auth=auth)
    data = response.json()
    
    assert response.status_code == 200
    assert "Service2" in data
    service2_data = data["Service2"]
    assert isinstance(service2_data, dict)

def test_service2_data_structure():
    """Test if service2's data has the expected structure"""
    response = requests.get("http://localhost:8198/service1", auth=auth)
    data = response.json()
    
    assert response.status_code == 200
    service2_data = data["Service2"]
    # Check for expected fields without checking specific values
    assert "IP Address" in service2_data
    assert "Running Processes" in service2_data
    assert "Disk Space" in service2_data
    assert "Uptime" in service2_data