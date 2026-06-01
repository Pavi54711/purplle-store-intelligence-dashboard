from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_events():
    response = client.get("/events")

    assert response.status_code == 200