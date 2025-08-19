import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_extract_number():
    response = client.post("/numbers/extract/?number=20")
    assert response.status_code == 200
    assert "Número 20 extraído correctamente" in response.json()["message"]

def test_missing_number():
    response = client.get("/numbers/missing/")
    assert response.status_code == 200
    assert "missing_number" in response.json()
