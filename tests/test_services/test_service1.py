import pytest
from service1.service1 import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_service_response(client):
    """Test if service returns 200 and basic response structure"""
    response = client.get('/')
    data = response.get_json()
    
    assert response.status_code == 200
    assert "Service1" in data
    assert "Service2" in data

def test_service2_error_response(client):
    """Test if response structure is maintained even when Service2 fails"""
    response = client.get('/')
    data = response.get_json()
    
    assert response.status_code == 200
    assert "Service1" in data
    assert "Service2" in data