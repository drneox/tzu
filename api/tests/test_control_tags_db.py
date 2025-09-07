"""
Tests para la funcionalidad de tags de control con base de datos
"""

import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Threat, InformationSystem, User
from database import SessionLocal
import crud
import schemas
from control_tags import (
    ALL_CONTROLS,
    validate_control_tag,
    normalize_tag_for_lookup,
    get_tag_details,
    search_predefined_tags,
    format_tag_for_display
)

class TestControlTagsWithDatabase:
    """Tests para tags de control con integración de base de datos"""
    
    def test_create_threat_with_control_tags(self, test_client, auth_headers, test_information_system):
        """Test crear una amenaza con tags de control"""
        threat_data = {
            "title": "Test Threat with Control Tags",
            "description": "Una amenaza de prueba con tags de control",
            "control_tags": ["V2.1.1", "MSTG-AUTH-1", "ID.AM-1"],
            "severity": "High",
            "category": "Authentication",
            "information_system_id": test_information_system.id
        }
        
        response = test_client.post("/api/threats/", json=threat_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["title"] == threat_data["title"]
        assert data["control_tags"] == threat_data["control_tags"]
        assert len(data["control_tags"]) == 3
        
    def test_update_threat_control_tags(self, test_client, auth_headers, test_information_system):
        """Test actualizar tags de control de una amenaza"""
        # Crear amenaza inicial
        threat_data = {
            "title": "Test Threat for Update",
            "description": "Amenaza para actualizar tags",
            "control_tags": ["V2.1.1"],
            "severity": "Medium",
            "category": "Authentication",
            "information_system_id": test_information_system.id
        }
        
        create_response = test_client.post("/api/threats/", json=threat_data, headers=auth_headers)
        assert create_response.status_code == 201
        threat_id = create_response.json()["id"]
        
        # Actualizar tags
        update_data = {
            "title": "Test Threat for Update",
            "description": "Amenaza con tags actualizados",
            "control_tags": ["V2.1.1", "MSTG-AUTH-1", "A.5.1.1"],
            "severity": "High",
            "category": "Authentication",
            "information_system_id": test_information_system.id
        }
        
        update_response = test_client.put(f"/api/threats/{threat_id}", json=update_data, headers=auth_headers)
        assert update_response.status_code == 200
        
        updated_data = update_response.json()
        assert len(updated_data["control_tags"]) == 3
        assert "V2.1.1" in updated_data["control_tags"]
        assert "MSTG-AUTH-1" in updated_data["control_tags"]
        assert "A.5.1.1" in updated_data["control_tags"]
        
    def test_get_threat_with_control_tags_details(self, test_client, auth_headers, test_information_system):
        """Test obtener amenaza con detalles de tags de control"""
        threat_data = {
            "title": "Threat with Tag Details",
            "description": "Amenaza para probar detalles de tags",
            "control_tags": ["V2.1.1", "NIST-ID.AM-1"],
            "severity": "High",
            "category": "Access Control",
            "information_system_id": test_information_system.id
        }
        
        create_response = test_client.post("/api/threats/", json=threat_data, headers=auth_headers)
        threat_id = create_response.json()["id"]
        
        # Obtener amenaza
        get_response = test_client.get(f"/api/threats/{threat_id}", headers=auth_headers)
        assert get_response.status_code == 200
        
        data = get_response.json()
        assert "control_tags" in data
        
        # Verificar que los tags son válidos
        for tag in data["control_tags"]:
            normalized_tag = normalize_tag_for_lookup(tag)
            assert validate_control_tag(normalized_tag), f"Tag {tag} debe ser válido"
            
    def test_search_threats_by_control_tags(self, test_client, auth_headers, test_information_system):
        """Test buscar amenazas por tags de control"""
        # Crear varias amenazas con diferentes tags
        threats_data = [
            {
                "title": "Auth Threat 1",
                "description": "Amenaza de autenticación 1",
                "control_tags": ["V2.1.1", "V2.2.1"],
                "severity": "High",
                "category": "Authentication",
                "information_system_id": test_information_system.id
            },
            {
                "title": "Auth Threat 2", 
                "description": "Amenaza de autenticación 2",
                "control_tags": ["V2.1.1", "MSTG-AUTH-1"],
                "severity": "Medium",
                "category": "Authentication",
                "information_system_id": test_information_system.id
            },
            {
                "title": "Network Threat",
                "description": "Amenaza de red",
                "control_tags": ["ID.AM-1", "PR.AC-1"],
                "severity": "Low",
                "category": "Network",
                "information_system_id": test_information_system.id
            }
        ]
        
        # Crear amenazas
        for threat_data in threats_data:
            response = test_client.post("/api/threats/", json=threat_data, headers=auth_headers)
            assert response.status_code == 201
            
        # Buscar amenazas con tag específico
        search_response = test_client.get("/api/threats/?control_tag=V2.1.1", headers=auth_headers)
        assert search_response.status_code == 200
        
        search_results = search_response.json()
        
        # Verificar que encontró las amenazas correctas
        found_titles = [threat["title"] for threat in search_results]
        assert "Auth Threat 1" in found_titles
        assert "Auth Threat 2" in found_titles
        assert "Network Threat" not in found_titles


class TestControlTagValidationEndpoints:
    """Tests para endpoints de validación de tags"""
    
    def test_validate_single_control_tag_endpoint(self, test_client):
        """Test endpoint de validación de un tag individual"""
        # Tag válido
        response = test_client.post("/api/control-tags/validate", json={"tag": "V2.1.1"})
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_valid"] == True
        assert data["normalized_tag"] == "V2.1.1"
        assert data["formatted_tag"] == "ASVS-V2.1.1"
        assert "details" in data
        assert data["details"] is not None
        
    def test_validate_invalid_control_tag_endpoint(self, test_client):
        """Test endpoint con tag inválido"""
        response = test_client.post("/api/control-tags/validate", json={"tag": "INVALID-TAG-123"})
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_valid"] == False
        assert data["details"] is None
        
    def test_validate_control_tag_with_normalization_endpoint(self, test_client):
        """Test endpoint con tag que requiere normalización"""
        response = test_client.post("/api/control-tags/validate", json={"tag": "asvs-v2.1.1"})
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_valid"] == True
        assert data["normalized_tag"] == "V2.1.1"
        assert data["formatted_tag"] == "ASVS-V2.1.1"
        
    def test_batch_validate_control_tags_endpoint(self, test_client):
        """Test endpoint de validación en lote"""
        tags_to_validate = [
            "V2.1.1",
            "MSTG-AUTH-1", 
            "INVALID-TAG",
            "ID.AM-1",
            "asvs-v2.2.1"
        ]
        
        response = test_client.post("/api/control-tags/batch-validate", json={"tags": tags_to_validate})
        
        assert response.status_code == 200
        data = response.json()
        
        assert "results" in data
        assert len(data["results"]) == len(tags_to_validate)
        
        # Verificar resultados específicos
        results_by_tag = {result["original_tag"]: result for result in data["results"]}
        
        assert results_by_tag["V2.1.1"]["is_valid"] == True
        assert results_by_tag["MSTG-AUTH-1"]["is_valid"] == True
        assert results_by_tag["INVALID-TAG"]["is_valid"] == False
        assert results_by_tag["ID.AM-1"]["is_valid"] == True
        assert results_by_tag["asvs-v2.2.1"]["is_valid"] == True
        
    def test_search_control_tags_endpoint(self, test_client):
        """Test endpoint de búsqueda de tags"""
        response = test_client.get("/api/control-tags/search?query=authentication")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) > 0
        assert len(data) <= 20  # Verificar límite
        
        # Verificar que los resultados contienen información de tags
        for result in data[:3]:  # Verificar primeros 3
            assert "tag" in result
            assert "details" in result
            assert "formatted_tag" in result
            
    def test_get_all_control_tags_endpoint(self, test_client):
        """Test endpoint para obtener todos los tags"""
        response = test_client.get("/api/control-tags/all")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) == 313  # Total de controles
        
    def test_get_control_tags_by_standard_endpoint(self, test_client):
        """Test endpoint para obtener tags por estándar"""
        response = test_client.get("/api/control-tags/standards/ASVS")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) == 93  # Tags de ASVS
        
        # Verificar que todos son tags de ASVS
        for tag in data[:5]:  # Verificar primeros 5
            assert tag.startswith("V") or tag.startswith("ASVS-V")


class TestSTRIDEControlMapping:
    """Tests para el mapeo de controles STRIDE"""
    
    def test_get_stride_suggestions_endpoint(self, test_client):
        """Test endpoint de sugerencias STRIDE"""
        stride_categories = [
            "Spoofing", "Tampering", "Repudiation", 
            "Information_Disclosure", "Denial_of_Service", "Elevation_of_Privilege"
        ]
        
        for category in stride_categories:
            response = test_client.get(f"/api/control-tags/suggestions/{category}")
            
            assert response.status_code == 200
            data = response.json()
            
            assert isinstance(data, list)
            assert len(data) > 0
            
            # Verificar estructura de respuesta
            for suggestion in data[:3]:  # Verificar primeros 3
                assert "tag" in suggestion
                assert "details" in suggestion
                assert "formatted_tag" in suggestion
                assert "standard" in suggestion
                
    def test_stride_suggestions_invalid_category(self, test_client):
        """Test endpoint con categoría STRIDE inválida"""
        response = test_client.get("/api/control-tags/suggestions/InvalidCategory")
        
        assert response.status_code == 404
        
    def test_stride_mapping_completeness(self, test_client):
        """Test que verifica la completitud del mapeo STRIDE"""
        stride_categories = [
            "Spoofing", "Tampering", "Repudiation",
            "Information_Disclosure", "Denial_of_Service", "Elevation_of_Privilege"
        ]
        
        total_suggestions = 0
        all_suggested_tags = set()
        
        for category in stride_categories:
            response = test_client.get(f"/api/control-tags/suggestions/{category}")
            assert response.status_code == 200
            
            suggestions = response.json()
            total_suggestions += len(suggestions)
            
            # Recopilar todos los tags sugeridos
            for suggestion in suggestions:
                all_suggested_tags.add(suggestion["tag"])
                
                # Verificar que cada tag sugerido es válido
                normalized_tag = normalize_tag_for_lookup(suggestion["tag"])
                assert validate_control_tag(normalized_tag), f"Tag sugerido {suggestion['tag']} debe ser válido"
                
        # Verificar que hay una cobertura razonable
        assert total_suggestions >= 30, f"Debe haber al menos 30 sugerencias STRIDE totales, encontrado {total_suggestions}"
        assert len(all_suggested_tags) >= 20, f"Debe haber al menos 20 tags únicos sugeridos, encontrado {len(all_suggested_tags)}"


class TestControlTagsPerformance:
    """Tests de rendimiento para operaciones de tags"""
    
    def test_bulk_tag_validation_performance(self, test_client):
        """Test de rendimiento para validación en lote"""
        import time
        
        # Crear lista grande de tags para validar
        large_tag_list = []
        valid_tags = ["V2.1.1", "MSTG-AUTH-1", "ID.AM-1", "A.5.1.1", "SBS-2137-1"]
        
        # Repetir tags válidos 20 veces (100 tags total)
        for _ in range(20):
            large_tag_list.extend(valid_tags)
            
        start_time = time.time()
        
        response = test_client.post("/api/control-tags/batch-validate", json={"tags": large_tag_list})
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert response.status_code == 200
        assert execution_time < 2.0, f"Validación en lote debe ser rápida. Tiempo: {execution_time:.2f}s"
        
        data = response.json()
        assert len(data["results"]) == len(large_tag_list)
        
    def test_search_performance(self, test_client):
        """Test de rendimiento para búsquedas"""
        import time
        
        search_terms = ["auth", "access", "control", "security", "data"]
        
        start_time = time.time()
        
        for term in search_terms:
            response = test_client.get(f"/api/control-tags/search?query={term}")
            assert response.status_code == 200
            
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert execution_time < 1.0, f"Búsquedas múltiples deben ser rápidas. Tiempo: {execution_time:.2f}s"


class TestControlTagsErrorHandling:
    """Tests de manejo de errores para tags"""
    
    def test_validate_empty_tag(self, test_client):
        """Test validación con tag vacío"""
        response = test_client.post("/api/control-tags/validate", json={"tag": ""})
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] == False
        
    def test_validate_null_tag(self, test_client):
        """Test validación con tag nulo"""
        response = test_client.post("/api/control-tags/validate", json={"tag": None})
        
        # Podría ser 422 (Unprocessable Entity) dependiendo de la validación
        assert response.status_code in [200, 422]
        
    def test_batch_validate_empty_list(self, test_client):
        """Test validación en lote con lista vacía"""
        response = test_client.post("/api/control-tags/batch-validate", json={"tags": []})
        
        assert response.status_code == 200
        data = response.json()
        assert data["results"] == []
        
    def test_search_with_very_short_query(self, test_client):
        """Test búsqueda con query muy corta"""
        response = test_client.get("/api/control-tags/search?query=a")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []  # Debe retornar lista vacía para queries muy cortas
        
    def test_search_with_empty_query(self, test_client):
        """Test búsqueda con query vacía"""
        response = test_client.get("/api/control-tags/search?query=")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []


if __name__ == "__main__":
    print("✅ Tests de control tags con base de datos creados exitosamente")
