import requests

auth = ('admin', 'admin123')

def test_stop_endpoint():
    """Test if stop endpoint returns correct response structure"""
    response = requests.post("http://localhost:8198/stop", auth=auth)
    data = response.json()
    
    assert response.status_code == 200
    assert "message" in data
    assert "Stopping services..." in data["message"]