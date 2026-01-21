"""Testes de integração da API."""
import pytest
from fastapi.testclient import TestClient

from src.interface.api.main import app


@pytest.fixture
def client():
    """Fixture para cliente de teste."""
    return TestClient(app)


class TestHealthEndpoint:
    """Testes para o endpoint de health check."""
    
    def test_health_check_returns_200(self, client):
        """Testa que o health check retorna 200."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
    
    def test_health_check_returns_correct_data(self, client):
        """Testa que o health check retorna dados corretos."""
        response = client.get("/api/v1/health")
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "version" in data
