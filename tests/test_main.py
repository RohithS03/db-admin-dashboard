import pytest
from fastapi.testclient import TestClient
from app.main import app
import base64

client = TestClient(app)

def get_auth_headers():
    auth_str = "admin:secret"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    return {"Authorization": f"Basic {b64_auth}"}

def test_home_unauthorized():
    response = client.get("/")
    assert response.status_code == 401

def test_home_authorized():
    response = client.get("/", headers=get_auth_headers())
    assert response.status_code == 200

def test_query_page_authorized():
    response = client.get("/query", headers=get_auth_headers())
    assert response.status_code == 200
