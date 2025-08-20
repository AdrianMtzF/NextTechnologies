import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_numbers():
    # Antes de cada test, reinicia el conjunto
    client.post("/numbers/reset/")


def test_extract_number():
    response = client.post("/numbers/extract/?number=20")
    assert response.status_code == 200
    assert "Número 20 extraído correctamente" in response.json()["message"]


def test_missing_number():
    # Se extrae el numero
    client.post("/numbers/extract/?number=55")

    # Busca el numero
    response = client.get("/numbers/missing/")
    assert response.status_code == 200
    assert response.json()["missing_number"] == 55


def test_invalid_number():
    response = client.post("/numbers/extract/?number=150")
    assert response.status_code == 422


def test_reset_allows_new_extraction():
    # Extraemos uno
    client.post("/numbers/extract/?number=30")

    # Reiniciamos
    client.post("/numbers/reset/")

    # Ahora debería permitir extraer el mismo número de nuevo
    response = client.post("/numbers/extract/?number=30")
    assert response.status_code == 200
    assert "Número 30 extraído correctamente" in response.json()["message"]
