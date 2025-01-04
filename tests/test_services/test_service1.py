import pytest
from service1.service1 import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_service_response(client):
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "data"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        response = client.get('/')
        data = response.get_json()
        
        assert response.status_code == 200
        assert "Service1" in data
        assert "Service2" in data

def test_service2_error_handling(client):
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Service2 unavailable")
        
        response = client.get('/')
        data = response.get_json()
        
        assert response.status_code == 200
        assert "error" in data["Service2"]