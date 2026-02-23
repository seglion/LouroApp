from fastapi.testclient import TestClient
from src.infrastructure.api.main import app

client = TestClient(app)

def test_health_check_returns_ok_and_db_status():
    """Prueba unitaria TDD para el endpoint de Health Check"""
    response = client.get("/health")
    
    # Assert HTTP Status Code
    assert response.status_code == 200
    
    # Assert JSON payload
    data = response.json()
    assert "status" in data
    assert "db_connected" in data
    assert data["status"] == "ok"
    # En entorno real conectará a test db o estará mockeado,
    # para TDD asumiremos que la API responde el bool correctamente
    assert isinstance(data["db_connected"], bool)
