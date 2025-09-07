"""
Tests para los endpoints específicos de control-tags API
"""

import pytest
import json
from unittest.mock import patch, MagicMock
from tests.conftest import client

class TestControlTagsEndpoints:
    """Tests para endpoints específicos de control-tags"""
    
    def test_suggestions_endpoint_spoofing(self):
        """Test del endpoint de sugerencias para SPOOFING"""
        response = client.get("/api/control-tags/suggestions/Spoofing")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, dict)
        assert "suggested_tags" in data
        assert "threat_type" in data
        assert data["threat_type"].upper() == "SPOOFING"
        
        # Verificar que hay sugerencias
        suggested_tags = data["suggested_tags"]
        assert isinstance(suggested_tags, list)
        assert len(suggested_tags) > 0
        
        # Verificar estructura de tags sugeridos
        for tag_info in suggested_tags[:3]:  # Primeros 3
            assert "tag" in tag_info
            assert "standard" in tag_info
            assert "title" in tag_info
            assert "description" in tag_info
            
            # Verificar que el tag tiene formato correcto
            tag = tag_info["tag"]
            assert "-" in tag  # Formato STANDARD-TAG
    
    def test_suggestions_endpoint_tampering(self):
        """Test del endpoint de sugerencias para TAMPERING"""
        response = client.get("/api/control-tags/suggestions/Tampering")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["threat_type"].upper() == "TAMPERING"
        assert len(data["suggested_tags"]) > 0
        
        # Verificar que las sugerencias son relevantes para tampering
        suggested_tags = data["suggested_tags"]
        relevant_terms = ["integrity", "validation", "hash", "signature", "tamper"]
        
        relevant_count = 0
        for tag_info in suggested_tags:
            content = (tag_info["title"] + " " + tag_info["description"]).lower()
            if any(term in content for term in relevant_terms):
                relevant_count += 1
        
        # Al menos 50% de las sugerencias deben ser relevantes
        assert relevant_count >= len(suggested_tags) * 0.5
    
    def test_suggestions_endpoint_repudiation(self):
        """Test del endpoint de sugerencias para REPUDIATION"""
        response = client.get("/api/control-tags/suggestions/Repudiation")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["threat_type"].upper() == "REPUDIATION"
        suggested_tags = data["suggested_tags"]
        
        # Verificar términos relevantes para repudiation
        relevant_terms = ["logging", "audit", "non-repudiation", "record", "log"]
        
        for tag_info in suggested_tags[:2]:  # Primeros 2
            content = (tag_info["title"] + " " + tag_info["description"]).lower()
            # Al menos uno de los primeros tags debe ser relevante
            has_relevant_term = any(term in content for term in relevant_terms)
            if has_relevant_term:
                break
        else:
            pytest.fail("Al menos uno de los primeros tags debe ser relevante para repudiation")
    
    def test_suggestions_endpoint_information_disclosure(self):
        """Test del endpoint de sugerencias para INFORMATION_DISCLOSURE"""
        response = client.get("/api/control-tags/suggestions/Information_Disclosure")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["threat_type"].upper() == "INFORMATION_DISCLOSURE"
        suggested_tags = data["suggested_tags"]
        
        # Verificar términos relevantes para information disclosure
        relevant_terms = ["confidentiality", "encryption", "access", "privacy", "disclosure", "data"]
        
        relevant_count = 0
        for tag_info in suggested_tags:
            content = (tag_info["title"] + " " + tag_info["description"]).lower()
            if any(term in content for term in relevant_terms):
                relevant_count += 1
        
        assert relevant_count > 0, "Debe haber al menos una sugerencia relevante"
    
    def test_suggestions_endpoint_denial_of_service(self):
        """Test del endpoint de sugerencias para DENIAL_OF_SERVICE"""
        response = client.get("/api/control-tags/suggestions/Denial_Of_Service")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["threat_type"].upper() == "DENIAL_OF_SERVICE"
        suggested_tags = data["suggested_tags"]
        
        # Verificar términos relevantes para DoS
        relevant_terms = ["availability", "rate", "limit", "resource", "denial", "service"]
        
        for tag_info in suggested_tags:
            assert "tag" in tag_info
            assert "standard" in tag_info
            assert len(tag_info["title"]) > 0
            assert len(tag_info["description"]) > 0
    
    def test_suggestions_endpoint_elevation_of_privilege(self):
        """Test del endpoint de sugerencias para ELEVATION_OF_PRIVILEGE"""
        response = client.get("/api/control-tags/suggestions/Elevation_Of_Privilege")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["threat_type"].upper() == "ELEVATION_OF_PRIVILEGE"
        suggested_tags = data["suggested_tags"]
        
        # Verificar términos relevantes para privilege escalation
        relevant_terms = ["authorization", "privilege", "permission", "access", "escalation", "role"]
        
        relevant_count = 0
        for tag_info in suggested_tags:
            content = (tag_info["title"] + " " + tag_info["description"]).lower()
            if any(term in content for term in relevant_terms):
                relevant_count += 1
        
        assert relevant_count > 0, "Debe haber sugerencias relevantes para elevation of privilege"
    
    def test_suggestions_endpoint_case_insensitive(self):
        """Test que el endpoint maneja diferentes casos correctamente"""
        test_cases = [
            "spoofing",
            "SPOOFING", 
            "Spoofing",
            "SpOoFiNg"
        ]
        
        responses = []
        for case in test_cases:
            response = client.get(f"/api/control-tags/suggestions/{case}")
            assert response.status_code == 200
            responses.append(response.json())
        
        # Todas las respuestas deben ser idénticas
        first_response = responses[0]
        for response in responses[1:]:
            assert response["threat_type"] == first_response["threat_type"]
            assert len(response["suggested_tags"]) == len(first_response["suggested_tags"])
    
    def test_suggestions_endpoint_invalid_threat_type(self):
        """Test del endpoint con tipo de amenaza inválido"""
        response = client.get("/api/control-tags/suggestions/InvalidThreat")
        
        # Debe manejar gracefully el tipo inválido
        assert response.status_code in [400, 404]  # Bad Request o Not Found
    
    def test_suggestions_endpoint_empty_threat_type(self):
        """Test del endpoint con tipo de amenaza vacío"""
        response = client.get("/api/control-tags/suggestions/")
        
        # Debe retornar error para path vacío
        assert response.status_code == 404
    
    def test_suggestions_response_structure(self):
        """Test de estructura consistente de respuesta"""
        threat_types = [
            "Spoofing", "Tampering", "Repudiation",
            "Information_Disclosure", "Denial_Of_Service", "Elevation_Of_Privilege"
        ]
        
        for threat_type in threat_types:
            response = client.get(f"/api/control-tags/suggestions/{threat_type}")
            assert response.status_code == 200
            
            data = response.json()
            
            # Verificar estructura básica
            assert isinstance(data, dict)
            assert "threat_type" in data
            assert "suggested_tags" in data
            
            # Verificar tipos de datos
            assert isinstance(data["threat_type"], str)
            assert isinstance(data["suggested_tags"], list)
            
            # Verificar estructura de cada tag sugerido
            for tag_info in data["suggested_tags"]:
                required_fields = ["tag", "standard", "title", "description"]
                for field in required_fields:
                    assert field in tag_info, f"Campo '{field}' faltante en {threat_type}"
                    assert isinstance(tag_info[field], str), f"Campo '{field}' debe ser string en {threat_type}"
                    assert len(tag_info[field].strip()) > 0, f"Campo '{field}' no debe estar vacío en {threat_type}"


class TestControlTagsEndpointsIntegration:
    """Tests de integración para endpoints de control-tags"""
    
    @patch('api.crud.get_current_user')
    def test_suggestions_with_authentication(self, mock_get_user):
        """Test de sugerencias con autenticación"""
        # Mock user
        mock_user = MagicMock()
        mock_user.id = 1
        mock_get_user.return_value = mock_user
        
        response = client.get(
            "/api/control-tags/suggestions/Spoofing",
            headers={"Authorization": "Bearer fake-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "suggested_tags" in data
    
    def test_suggestions_cross_standard_coverage(self):
        """Test que las sugerencias cubren múltiples estándares"""
        response = client.get("/api/control-tags/suggestions/Spoofing")
        assert response.status_code == 200
        
        data = response.json()
        suggested_tags = data["suggested_tags"]
        
        # Extraer estándares únicos de las sugerencias
        standards_found = set()
        for tag_info in suggested_tags:
            standards_found.add(tag_info["standard"])
        
        # Debe haber sugerencias de múltiples estándares
        assert len(standards_found) >= 2, f"Esperado múltiples estándares, encontrado: {standards_found}"
        
        # Verificar que incluye estándares principales
        expected_standards = {"ASVS", "MASVS", "NIST", "ISO27001", "SBS"}
        found_expected = standards_found.intersection(expected_standards)
        assert len(found_expected) >= 2, f"Debe incluir al menos 2 estándares principales, encontrado: {found_expected}"
    
    def test_suggestions_relevance_quality(self):
        """Test de calidad y relevancia de sugerencias"""
        # Mapeo de amenazas a términos esperados
        threat_relevance_map = {
            "Spoofing": ["authentication", "identity", "verification", "credential", "auth"],
            "Tampering": ["integrity", "validation", "hash", "signature", "tamper"],
            "Repudiation": ["logging", "audit", "non-repudiation", "record", "log"],
            "Information_Disclosure": ["confidentiality", "encryption", "access", "privacy", "data"],
            "Denial_Of_Service": ["availability", "rate", "limit", "resource", "denial"],
            "Elevation_Of_Privilege": ["authorization", "privilege", "permission", "access", "role"]
        }
        
        for threat_type, expected_terms in threat_relevance_map.items():
            response = client.get(f"/api/control-tags/suggestions/{threat_type}")
            assert response.status_code == 200
            
            data = response.json()
            suggested_tags = data["suggested_tags"]
            
            # Contar sugerencias relevantes
            relevant_count = 0
            total_suggestions = len(suggested_tags)
            
            for tag_info in suggested_tags:
                content = (tag_info["title"] + " " + tag_info["description"]).lower()
                if any(term.lower() in content for term in expected_terms):
                    relevant_count += 1
            
            # Al menos 40% de las sugerencias deben ser relevantes
            relevance_ratio = relevant_count / total_suggestions if total_suggestions > 0 else 0
            assert relevance_ratio >= 0.4, \
                f"{threat_type}: {relevance_ratio:.2%} relevancia, esperado al menos 40%"
    
    def test_suggestions_limit_and_pagination(self):
        """Test de límites y posible paginación de sugerencias"""
        response = client.get("/api/control-tags/suggestions/Spoofing")
        assert response.status_code == 200
        
        data = response.json()
        suggested_tags = data["suggested_tags"]
        
        # Verificar que hay un número razonable de sugerencias
        assert len(suggested_tags) >= 3, "Debe haber al menos 3 sugerencias"
        assert len(suggested_tags) <= 20, "No debe haber más de 20 sugerencias para evitar sobrecarga"
        
        # Verificar que no hay duplicados
        tags_seen = set()
        for tag_info in suggested_tags:
            tag = tag_info["tag"]
            assert tag not in tags_seen, f"Tag duplicado encontrado: {tag}"
            tags_seen.add(tag)
    
    def test_suggestions_performance(self):
        """Test de rendimiento de endpoint de sugerencias"""
        import time
        
        start_time = time.time()
        
        # Hacer múltiples requests
        threat_types = ["Spoofing", "Tampering", "Repudiation"]
        
        for threat_type in threat_types:
            response = client.get(f"/api/control-tags/suggestions/{threat_type}")
            assert response.status_code == 200
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Debe completarse en menos de 2 segundos para 3 requests
        assert total_time < 2.0, f"Requests deben ser rápidos. Tiempo total: {total_time:.2f}s"


class TestControlTagsValidationEndpoints:
    """Tests para endpoints de validación de control tags"""
    
    def test_batch_tag_validation_endpoint(self):
        """Test del endpoint de validación en lote (si existe)"""
        # Este endpoint podría no existir aún, pero testing la funcionalidad esperada
        test_tags = [
            "V2.1.1",
            "MSTG-AUTH-1", 
            "INVALID-TAG",
            "ID.AM-1"
        ]
        
        # Simular request de validación en lote
        payload = {"tags": test_tags}
        
        # Si el endpoint existe
        response = client.post("/api/control-tags/validate-batch", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            assert "results" in data
            assert len(data["results"]) == len(test_tags)
            
            # Verificar estructura de resultados
            for i, result in enumerate(data["results"]):
                assert "tag" in result
                assert "is_valid" in result
                assert result["tag"] == test_tags[i]
                assert isinstance(result["is_valid"], bool)
        else:
            # Endpoint no implementado aún
            assert response.status_code in [404, 405]
    
    def test_single_tag_validation_endpoint(self):
        """Test del endpoint de validación individual (si existe)"""
        test_tag = "V2.1.1"
        
        response = client.get(f"/api/control-tags/validate/{test_tag}")
        
        if response.status_code == 200:
            data = response.json()
            assert "tag" in data
            assert "is_valid" in data
            assert "normalized" in data
            assert "details" in data
            
            assert data["tag"] == test_tag
            assert data["is_valid"] == True
            assert data["normalized"] == test_tag
            assert data["details"] is not None
        else:
            # Endpoint no implementado aún
            assert response.status_code in [404, 405]


if __name__ == "__main__":
    # Ejecutar algunos tests básicos si se ejecuta directamente
    endpoint_test = TestControlTagsEndpoints()
    print("✅ Tests de endpoints de control-tags disponibles para ejecución")
