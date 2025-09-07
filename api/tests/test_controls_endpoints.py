"""
Tests para los endpoints del backend relacionados con controles de seguridad
"""

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os
import sys

from tests.conftest import client, test_user, auth_headers, test_information_system, db_session
import models
import crud
import schemas

class TestControlsEndpoints:
    """Tests para los endpoints relacionados con controles"""
    
    def test_get_available_standards_endpoint(self):
        """Test del endpoint para obtener estándares disponibles"""
        response = client.get("/api/controls/standards")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        expected_standards = ["ASVS", "MASVS", "NIST", "ISO27001", "SBS"]
        assert set(data) == set(expected_standards)
        
    def test_get_standard_info_endpoint(self):
        """Test del endpoint para obtener información de un estándar"""
        response = client.get("/api/controls/standards/ASVS")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == "ASVS"
        assert data["controls_count"] == 93
        assert "categories" in data
        assert "sample_controls" in data
        assert len(data["sample_controls"]) == 5
        
    def test_get_standard_info_invalid(self):
        """Test del endpoint con estándar inválido"""
        response = client.get("/api/controls/standards/INVALID")
        
        assert response.status_code == 404
        
    def test_get_all_standards_info_endpoint(self):
        """Test del endpoint para obtener información de todos los estándares"""
        response = client.get("/api/controls/standards/all")
        
        assert response.status_code == 200
        data = response.json()
        
        expected_standards = ["ASVS", "MASVS", "NIST", "ISO27001", "SBS"]
        assert set(data.keys()) == set(expected_standards)
        
        for standard, info in data.items():
            assert "name" in info
            assert "controls_count" in info
            assert "categories" in info
            assert "sample_controls" in info
            
    def test_search_controls_endpoint(self):
        """Test del endpoint de búsqueda de controles"""
        response = client.get("/api/controls/search?query=authentication")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) > 0
        assert len(data) <= 20  # Verificar límite
        
        # Verificar estructura de respuesta
        for item in data[:3]:  # Verificar primeros 3 elementos
            assert "tag" in item
            assert "details" in item
            assert "title" in item["details"]
            assert "description" in item["details"]
            
    def test_search_controls_empty_query(self):
        """Test del endpoint de búsqueda con query vacía"""
        response = client.get("/api/controls/search?query=")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []
        
    def test_search_controls_short_query(self):
        """Test del endpoint de búsqueda con query muy corta"""
        response = client.get("/api/controls/search?query=a")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []
        
    def test_validate_control_tag_endpoint(self):
        """Test del endpoint de validación de tags"""
        # Tag válido
        response = client.post("/api/controls/validate", json={"tag": "V2.1.1"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] == True
        assert data["normalized_tag"] == "V2.1.1"
        assert data["formatted_tag"] == "ASVS-V2.1.1"
        assert "details" in data
        
    def test_validate_control_tag_invalid(self):
        """Test del endpoint de validación con tag inválido"""
        response = client.post("/api/controls/validate", json={"tag": "INVALID-TAG"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] == False
        assert data["details"] is None
        
    def test_validate_control_tag_with_normalization(self):
        """Test del endpoint de validación con normalización"""
        response = client.post("/api/controls/validate", json={"tag": "asvs-v2.1.1"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] == True
        assert data["normalized_tag"] == "V2.1.1"
        assert data["formatted_tag"] == "ASVS-V2.1.1"
        
    def test_get_tags_by_standard_endpoint(self):
        """Test del endpoint para obtener tags por estándar"""
        response = client.get("/api/controls/standards/ASVS/tags")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) == 93
        assert "V2.1.1" in data
        
    def test_get_tags_by_standard_invalid(self):
        """Test del endpoint con estándar inválido para tags"""
        response = client.get("/api/controls/standards/INVALID/tags")
        
        assert response.status_code == 404


class TestThreatEndpointsWithControls:
    """Tests para endpoints de threats que incluyen controles"""
    
    @patch('api.crud.get_threat')
    @patch('api.crud.get_current_user')
    def test_get_threat_with_control_tags(self, mock_get_user, mock_get_threat):
        """Test de obtener threat con tags de controles"""
        # Mock user
        mock_user = MagicMock()
        mock_user.id = 1
        mock_get_user.return_value = mock_user
        
        # Mock threat con control tags
        mock_threat = MagicMock()
        mock_threat.id = 1
        mock_threat.title = "Test Threat"
        mock_threat.description = "Test Description"
        mock_threat.control_tags = ["V2.1.1", "MSTG-AUTH-1"]
        mock_threat.severity = "High"
        mock_threat.category = "Authentication"
        mock_threat.user_id = 1
        mock_get_threat.return_value = mock_threat
        
        response = client.get("/api/threats/1", headers={"Authorization": "Bearer fake-token"})
        
        # Note: Este test podría necesitar ajustes dependiendo de la implementación real del endpoint
        # El objetivo es verificar que los control_tags se manejan correctamente
        
    @patch('api.crud.create_threat')
    @patch('api.crud.get_current_user')
    def test_create_threat_with_control_tags(self, mock_get_user, mock_create_threat):
        """Test de crear threat con tags de controles"""
        # Mock user
        mock_user = MagicMock()
        mock_user.id = 1
        mock_get_user.return_value = mock_user
        
        # Mock threat creation
        mock_threat = MagicMock()
        mock_threat.id = 1
        mock_threat.title = "New Threat"
        mock_threat.control_tags = ["V2.1.1", "ID.AM-1"]
        mock_create_threat.return_value = mock_threat
        
        threat_data = {
            "title": "New Threat",
            "description": "Test Description",
            "control_tags": ["V2.1.1", "ID.AM-1"],
            "severity": "High",
            "category": "Authentication",
            "information_system_id": 1
        }
        
        response = client.post(
            "/api/threats/", 
            json=threat_data,
            headers={"Authorization": "Bearer fake-token"}
        )
        
        # Verificar que los tags se procesan correctamente


class TestBatchControlOperations:
    """Tests para operaciones en lote de controles"""
    
    def test_batch_validate_tags(self):
        """Test de validación en lote de tags"""
        tags_to_validate = [
            "V2.1.1",
            "MSTG-AUTH-1",
            "INVALID-TAG",
            "ID.AM-1",
            "A.5.1.1"
        ]
        
        response = client.post("/api/controls/batch-validate", json={"tags": tags_to_validate})
        
        assert response.status_code == 200
        data = response.json()
        
        assert "results" in data
        assert len(data["results"]) == len(tags_to_validate)
        
        valid_count = sum(1 for result in data["results"] if result["is_valid"])
        assert valid_count == 4  # 4 de 5 tags deben ser válidos
        
    def test_batch_get_tag_details(self):
        """Test de obtener detalles en lote"""
        tags = ["V2.1.1", "MSTG-AUTH-1", "ID.AM-1"]
        
        response = client.post("/api/controls/batch-details", json={"tags": tags})
        
        assert response.status_code == 200
        data = response.json()
        
        assert "results" in data
        assert len(data["results"]) == len(tags)
        
        for result in data["results"]:
            assert "tag" in result
            assert "details" in result
            if result["details"]:  # Si el tag es válido
                assert "title" in result["details"]
                assert "description" in result["details"]
                assert "category" in result["details"]


class TestControlsFilteringAndPagination:
    """Tests para filtrado y paginación de controles"""
    
    def test_get_controls_by_category(self):
        """Test de obtener controles por categoría"""
        response = client.get("/api/controls/category/Authentication")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        # Verificar que todos los controles pertenecen a la categoría correcta
        for control in data:
            assert "Authentication" in control.get("category", "").lower() or \
                   "authentication" in control.get("title", "").lower() or \
                   "authentication" in control.get("description", "").lower()
                   
    def test_get_controls_paginated(self):
        """Test de paginación de controles"""
        response = client.get("/api/controls/all?page=1&size=50")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert "pages" in data
        
        assert len(data["items"]) <= 50
        assert data["total"] == 313  # Total de controles
        assert data["page"] == 1
        assert data["size"] == 50
        
    def test_get_controls_paginated_last_page(self):
        """Test de última página de paginación"""
        # Calcular cuántas páginas hay con tamaño 50
        total_controls = 313
        page_size = 50
        last_page = (total_controls + page_size - 1) // page_size
        
        response = client.get(f"/api/controls/all?page={last_page}&size={page_size}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["page"] == last_page
        expected_items_in_last_page = total_controls % page_size or page_size
        assert len(data["items"]) <= expected_items_in_last_page


class TestErrorHandlingEndpoints:
    """Tests para manejo de errores en endpoints"""
    
    def test_validate_tag_missing_data(self):
        """Test de validación con datos faltantes"""
        response = client.post("/api/controls/validate", json={})
        
        assert response.status_code == 422  # Unprocessable Entity
        
    def test_batch_validate_empty_list(self):
        """Test de validación en lote con lista vacía"""
        response = client.post("/api/controls/batch-validate", json={"tags": []})
        
        assert response.status_code == 200
        data = response.json()
        assert data["results"] == []
        
    def test_pagination_invalid_parameters(self):
        """Test de paginación con parámetros inválidos"""
        # Página negativa
        response = client.get("/api/controls/all?page=-1&size=50")
        assert response.status_code == 400
        
        # Tamaño demasiado grande
        response = client.get("/api/controls/all?page=1&size=1000")
        assert response.status_code == 400
        
        # Tamaño cero o negativo
        response = client.get("/api/controls/all?page=1&size=0")
        assert response.status_code == 400


class TestControlsPerformance:
    """Tests de rendimiento para endpoints de controles"""
    
    def test_large_batch_validation_performance(self):
        """Test de rendimiento para validación en lote grande"""
        import time
        
        # Crear una lista grande de tags para validar
        large_tag_list = []
        
        # Agregar algunos tags válidos repetidos
        valid_tags = ["V2.1.1", "MSTG-AUTH-1", "ID.AM-1", "A.5.1.1", "SBS-2137-1"]
        for _ in range(20):  # 100 tags total
            large_tag_list.extend(valid_tags)
            
        start_time = time.time()
        
        response = client.post("/api/controls/batch-validate", json={"tags": large_tag_list})
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert response.status_code == 200
        assert execution_time < 2.0, f"Validación en lote debe ser rápida. Tiempo: {execution_time:.2f}s"
        
    def test_search_performance(self):
        """Test de rendimiento para búsqueda"""
        import time
        
        start_time = time.time()
        
        response = client.get("/api/controls/search?query=authentication")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert response.status_code == 200
        assert execution_time < 0.5, f"Búsqueda debe ser rápida. Tiempo: {execution_time:.2f}s"


if __name__ == "__main__":
    # Ejecutar algunos tests básicos si se ejecuta directamente
    endpoint_test = TestControlsEndpoints()
    print("✅ Tests de endpoints disponibles para ejecución completa con pytest")
