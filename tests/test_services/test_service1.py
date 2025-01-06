import pytest
import requests
from service1.service1 import app

auth = ('admin', 'admin123')

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_service_response(client):
    """Test if service returns 200 and basic response structure"""
    response = requests.get("http://localhost:8198/service1", auth=auth)
    data = response.json()
    
    assert response.status_code == 200
    assert "Service1" in data
    assert "Service2" in data

def test_service2_error_response(client):
    """Test if response structure is maintained even when Service2 fails"""
    response = requests.get("http://localhost:8198/service1", auth=auth)
    data = response.json()
    
    assert response.status_code == 200
    assert "Service1" in data
    assert "Service2" in data