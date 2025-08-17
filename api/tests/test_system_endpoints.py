"""
Tests para endpoints del sistema
"""
import pytest
from tests.conftest import client

class TestSystemEndpoints:
    """Tests para endpoints básicos del sistema"""
    
    def test_health_endpoint(self):
        """Test del endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy" or "ok" in data["status"].lower()
    
    def test_root_endpoint(self):
        """Test del endpoint raíz - ahora debería devolver 404"""
        # Como eliminamos el endpoint raíz, debería devolver 404
        response = client.get("/")
        assert response.status_code == 404
    
    def test_nonexistent_endpoint(self):
        """Test de endpoint que no existe"""
        response = client.get("/endpoint-que-no-existe")
        assert response.status_code == 404
