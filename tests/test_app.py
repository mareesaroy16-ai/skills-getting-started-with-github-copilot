from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_register_activity():
    """Test registering for an activity"""
    test_data = {
        "activity": "Chess Club",
        "email": "test@example.com"
    }
    response = client.post("/activities/register", json=test_data)
    assert response.status_code == 200
    
def test_unregister_activity():
    """Test unregistering from an activity"""
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    
    # First register the user
    test_data = {
        "activity": activity,
        "email": email
    }
    register_response = client.post("/activities/register", json=test_data)
    assert register_response.status_code == 200
    
    # Then unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200