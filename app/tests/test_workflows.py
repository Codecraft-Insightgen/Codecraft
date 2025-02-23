import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to CodeCraft API"}

# we can add tests for each endpoint
# will probably as Aum or Sarthak to do it