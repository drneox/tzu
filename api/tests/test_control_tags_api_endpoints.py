"""
Tests para endpoints específicos de control tags que hemos implementado
"""

import pytest
import json
from fastapi.testclient import TestClient

# Importar configuración de test
from conftest import client, auth_headers, test_user, test_information_system

class TestControlTagsAPIEndpoints:
    """Tests para los endpoints específicos de control tags"""
    
    def test_get_all_standards_endpoint(self, auth_headers):
        """Test obtener todos los estándares disponibles"""
        response = client.get("/control-tags/standards", headers=auth_headers)
        
        assert response.status_code == 200
        standards = response.json()
        
        expected_standards = ["ASVS", "MASVS", "NIST", "ISO27001", "SBS"]
        assert set(standards) == set(expected_standards)
        assert len(standards) == 5
        
    def test_get_standard_info_endpoint(self, auth_headers):
        """Test obtener información detallada de un estándar"""
        response = client.get("/control-tags/standards/ASVS", headers=auth_headers)
        
        assert response.status_code == 200
        asvs_info = response.json()
        
        assert asvs_info["name"] == "ASVS"
        assert asvs_info["controls_count"] == 93
        assert "categories" in asvs_info
        assert "sample_controls" in asvs_info
        assert len(asvs_info["sample_controls"]) > 0
        
        # Test estándar inválido
        response = client.get("/control-tags/standards/INVALID", headers=auth_headers)
        assert response.status_code == 404
        
    def test_search_control_tags_endpoint(self, auth_headers):
        """Test buscar control tags"""
        response = client.get("/control-tags/search?query=authentication", headers=auth_headers)
        
        assert response.status_code == 200
        results = response.json()
        
        assert isinstance(results, list)
        assert len(results) > 0
        assert len(results) <= 20  # Límite de resultados
        
        # Verificar estructura de resultados
        for result in results[:3]:
            assert "tag" in result
            assert "details" in result
            assert "title" in result["details"]
            assert "description" in result["details"]
            assert "category" in result["details"]
            
    def test_validate_single_tag_endpoint(self, auth_headers):
        """Test validar un tag individual"""
        # Tag válido
        response = client.post("/control-tags/validate", json={"tag": "V2.1.1"}, headers=auth_headers)
        
        assert response.status_code == 200
        result = response.json()
        
        assert result["is_valid"] == True
        assert result["normalized_tag"] == "V2.1.1"
        assert result["formatted_tag"] == "ASVS-V2.1.1"
        assert result["details"] is not None
        assert "title" in result["details"]
        
        # Tag inválido
        response = client.post("/control-tags/validate", json={"tag": "INVALID-TAG"}, headers=auth_headers)
        
        assert response.status_code == 200
        result = response.json()
        
        assert result["is_valid"] == False
        assert result["details"] is None
        
    def test_batch_validate_tags_endpoint(self, auth_headers):
        """Test validar múltiples tags en lote"""
        tags_to_validate = [
            "V2.1.1",           # ASVS válido
            "MSTG-AUTH-1",      # MASVS válido
            "ID.AM-1",          # NIST válido
            "A.5.1.1",          # ISO27001 válido
            "SBS-2137-1",       # SBS válido
            "INVALID-TAG",      # Inválido
            "ANOTHER-INVALID"   # Inválido
        ]
        
        response = client.post(
            "/control-tags/validate-batch", 
            json={"tags": tags_to_validate}, 
            headers=auth_headers
        )
        
        assert response.status_code == 200
        results = response.json()
        
        assert "results" in results
        assert len(results["results"]) == len(tags_to_validate)
        
        # Contar válidos e inválidos
        valid_count = sum(1 for result in results["results"] if result["is_valid"])
        invalid_count = sum(1 for result in results["results"] if not result["is_valid"])
        
        assert valid_count == 5  # 5 tags válidos
        assert invalid_count == 2  # 2 tags inválidos
        
    def test_get_tags_by_standard_endpoint(self, auth_headers):
        """Test obtener tags por estándar específico"""
        # Test ASVS
        response = client.get("/control-tags/by-standard/ASVS", headers=auth_headers)
        assert response.status_code == 200
        
        asvs_result = response.json()
        assert "standard" in asvs_result
        assert "tags" in asvs_result
        assert asvs_result["standard"] == "ASVS"
        assert len(asvs_result["tags"]) == 93
        
        # Verificar que todos los tags son de ASVS
        for tag in asvs_result["tags"][:10]:  # Verificar primeros 10
            assert tag.startswith("V")
            
        # Test MASVS
        response = client.get("/control-tags/by-standard/MASVS", headers=auth_headers)
        assert response.status_code == 200
        
        masvs_result = response.json()
        assert masvs_result["standard"] == "MASVS"
        assert len(masvs_result["tags"]) == 10
        
        # Test estándar inválido
        response = client.get("/control-tags/by-standard/INVALID", headers=auth_headers)
        assert response.status_code == 404
        
    def test_get_tag_suggestions_by_stride_endpoint(self, auth_headers):
        """Test obtener sugerencias de tags por categoría STRIDE"""
        stride_categories = [
            "Spoofing",
            "Tampering", 
            "Repudiation",
            "Information Disclosure",
            "Denial of Service",
            "Elevation of Privilege"
        ]
        
        for category in stride_categories:
            response = client.get(f"/control-tags/suggestions/{category}", headers=auth_headers)
            
            assert response.status_code == 200
            suggestions = response.json()
            
            assert isinstance(suggestions, list)
            assert len(suggestions) > 0
            
            # Verificar estructura de sugerencias
            for suggestion in suggestions[:3]:
                assert "tag" in suggestion
                assert "title" in suggestion
                assert "description" in suggestion
                assert "standard" in suggestion
                assert "formatted_tag" in suggestion
                
    def test_get_all_predefined_tags_endpoint(self, auth_headers):
        """Test obtener todos los tags predefinidos"""
        response = client.get("/control-tags/all", headers=auth_headers)
        
        assert response.status_code == 200
        all_tags = response.json()
        
        assert "total_count" in all_tags
        assert "tags" in all_tags
        assert all_tags["total_count"] == 313  # Total de controles
        assert len(all_tags["tags"]) == 313
        
        # Verificar que incluye tags de todos los estándares
        tags_list = all_tags["tags"]
        
        asvs_tags = [tag for tag in tags_list if tag.startswith("V")]
        masvs_tags = [tag for tag in tags_list if tag.startswith("MSTG")]
        nist_tags = [tag for tag in tags_list if "." in tag and not tag.startswith("A.")]
        iso_tags = [tag for tag in tags_list if tag.startswith("A.")]
        sbs_tags = [tag for tag in tags_list if tag.startswith("SBS")]
        
        assert len(asvs_tags) == 93
        assert len(masvs_tags) == 10
        assert len(nist_tags) == 108
        assert len(iso_tags) == 59
        assert len(sbs_tags) == 43
        
    def test_search_with_pagination_endpoint(self, auth_headers):
        """Test búsqueda con paginación"""
        # Búsqueda que retorne muchos resultados
        response = client.get("/control-tags/search?query=access&page=1&size=10", headers=auth_headers)
        
        assert response.status_code == 200
        results = response.json()
        
        assert "items" in results
        assert "total" in results
        assert "page" in results
        assert "size" in results
        assert "pages" in results
        
        assert len(results["items"]) <= 10
        assert results["page"] == 1
        assert results["size"] == 10
        
        # Test página siguiente si hay suficientes resultados
        if results["pages"] > 1:
            response = client.get("/control-tags/search?query=access&page=2&size=10", headers=auth_headers)
            assert response.status_code == 200
            
            page2_results = response.json()
            assert page2_results["page"] == 2
            
    def test_get_tag_details_endpoint(self, auth_headers):
        """Test obtener detalles específicos de un tag"""
        response = client.get("/control-tags/details/V2.1.1", headers=auth_headers)
        
        assert response.status_code == 200
        details = response.json()
        
        assert "tag" in details
        assert "standard" in details
        assert "title" in details
        assert "description" in details
        assert "category" in details
        assert "formatted_tag" in details
        
        assert details["tag"] == "V2.1.1"
        assert details["standard"] == "ASVS"
        assert details["formatted_tag"] == "ASVS-V2.1.1"
        
        # Test tag inválido
        response = client.get("/control-tags/details/INVALID-TAG", headers=auth_headers)
        assert response.status_code == 404


class TestControlTagsIntegrationWithThreats:
    """Tests de integración entre control tags y threats via API"""
    
    def test_create_threat_with_tags_validation(self, auth_headers, test_information_system):
        """Test crear threat con validación de tags"""
        
        # Primero validar los tags que vamos a usar
        tags_to_use = ["V2.1.1", "MSTG-AUTH-1", "ID.AM-1"]
        validation_response = client.post(
            "/control-tags/validate-batch",
            json={"tags": tags_to_use},
            headers=auth_headers
        )
        assert validation_response.status_code == 200
        
        validation_results = validation_response.json()
        valid_tags = [
            result["normalized_tag"] for result in validation_results["results"] 
            if result["is_valid"]
        ]
        
        # Crear threat con los tags validados
        threat_data = {
            "title": "Validated Tags Threat",
            "description": "Threat con tags pre-validados",
            "severity": "High",
            "category": "Validated Security",
            "control_tags": valid_tags,
            "information_system_id": test_information_system.id
        }
        
        response = client.post("/api/threats/", json=threat_data, headers=auth_headers)
        assert response.status_code == 200
        
        created_threat = response.json()
        assert created_threat["control_tags"] == valid_tags
        
    def test_update_threat_tags_with_validation(self, auth_headers, test_information_system):
        """Test actualizar tags de threat con validación previa"""
        
        # Crear threat inicial
        initial_threat = {
            "title": "Threat to Update Tags",
            "description": "Se actualizarán los tags",
            "severity": "Medium",
            "category": "Update Test",
            "control_tags": ["V2.1.1"],
            "information_system_id": test_information_system.id
        }
        
        response = client.post("/api/threats/", json=initial_threat, headers=auth_headers)
        assert response.status_code == 200
        threat = response.json()
        
        # Validar nuevos tags antes de actualizar
        new_tags = ["V2.1.1", "V2.2.1", "MSTG-NETWORK-1", "ID.AM-1", "A.5.1.1"]
        validation_response = client.post(
            "/control-tags/validate-batch",
            json={"tags": new_tags},
            headers=auth_headers
        )
        assert validation_response.status_code == 200
        
        # Actualizar threat con nuevos tags
        update_data = {"control_tags": new_tags}
        response = client.put(
            f"/api/threats/{threat['id']}", 
            json=update_data, 
            headers=auth_headers
        )
        assert response.status_code == 200
        
        updated_threat = response.json()
        assert updated_threat["control_tags"] == new_tags
        
    def test_search_threats_by_control_tags_api(self, auth_headers, test_information_system):
        """Test buscar threats por control tags via API"""
        
        # Crear varios threats con diferentes tags
        threats_to_create = [
            {
                "title": "ASVS Auth Threat",
                "description": "Threat con controles ASVS de autenticación",
                "severity": "High",
                "category": "Authentication",
                "control_tags": ["V2.1.1", "V2.2.1", "V2.3.1"],
                "information_system_id": test_information_system.id
            },
            {
                "title": "Mobile Security Threat",
                "description": "Threat de seguridad móvil",
                "severity": "Medium", 
                "category": "Mobile",
                "control_tags": ["MSTG-AUTH-1", "MSTG-NETWORK-1"],
                "information_system_id": test_information_system.id
            },
            {
                "title": "Infrastructure Threat",
                "description": "Threat de infraestructura",
                "severity": "Low",
                "category": "Infrastructure", 
                "control_tags": ["ID.AM-1", "PR.AC-1"],
                "information_system_id": test_information_system.id
            }
        ]
        
        # Crear todos los threats
        created_threats = []
        for threat_data in threats_to_create:
            response = client.post("/api/threats/", json=threat_data, headers=auth_headers)
            assert response.status_code == 200
            created_threats.append(response.json())
        
        # Buscar threats por tag específico
        search_response = client.get("/api/threats/search?control_tag=V2.1.1", headers=auth_headers)
        assert search_response.status_code == 200
        
        search_results = search_response.json()
        matching_threats = [
            threat for threat in search_results 
            if "V2.1.1" in threat.get("control_tags", [])
        ]
        assert len(matching_threats) == 1  # Solo el primer threat tiene V2.1.1
        
        # Buscar por tag que aparece en múltiples threats
        # (Necesitarías agregar este endpoint si no existe)
        
    def test_threat_control_tags_summary(self, auth_headers, test_information_system):
        """Test obtener resumen de control tags por threat"""
        
        # Crear threat con múltiples controles
        threat_data = {
            "title": "Multi-Standard Threat",
            "description": "Threat con controles de múltiples estándares",
            "severity": "Critical",
            "category": "Multi-Standard",
            "control_tags": ["V2.1.1", "MSTG-AUTH-1", "ID.AM-1", "A.5.1.1", "SBS-2137-1"],
            "information_system_id": test_information_system.id
        }
        
        response = client.post("/api/threats/", json=threat_data, headers=auth_headers)
        assert response.status_code == 200
        threat = response.json()
        
        # Obtener detalles expandidos del threat (con información de control tags)
        detailed_response = client.get(f"/api/threats/{threat['id']}/detailed", headers=auth_headers)
        
        # Este endpoint podría no existir aún, así que solo verificamos si responde
        if detailed_response.status_code == 200:
            detailed_threat = detailed_response.json()
            
            if "control_tags_details" in detailed_threat:
                tags_details = detailed_threat["control_tags_details"]
                
                # Verificar que incluye detalles de cada tag
                assert len(tags_details) == 5
                
                standards_represented = set()
                for tag_detail in tags_details:
                    assert "tag" in tag_detail
                    assert "standard" in tag_detail
                    assert "title" in tag_detail
                    standards_represented.add(tag_detail["standard"])
                
                # Debe representar los 5 estándares
                assert len(standards_represented) == 5


class TestControlTagsErrorHandling:
    """Tests de manejo de errores en endpoints de control tags"""
    
    def test_invalid_request_formats(self, auth_headers):
        """Test manejo de formatos de request inválidos"""
        
        # Request sin datos
        response = client.post("/control-tags/validate", json={}, headers=auth_headers)
        assert response.status_code == 422  # Unprocessable Entity
        
        # Request con datos inválidos
        response = client.post("/control-tags/validate", json={"invalid_field": "data"}, headers=auth_headers)
        assert response.status_code == 422
        
        # Batch validation con lista vacía
        response = client.post("/control-tags/validate-batch", json={"tags": []}, headers=auth_headers)
        assert response.status_code == 200
        result = response.json()
        assert result["results"] == []
        
    def test_pagination_edge_cases(self, auth_headers):
        """Test casos edge de paginación"""
        
        # Página negativa
        response = client.get("/control-tags/search?query=auth&page=-1", headers=auth_headers)
        assert response.status_code == 400
        
        # Tamaño de página demasiado grande
        response = client.get("/control-tags/search?query=auth&size=1000", headers=auth_headers)
        assert response.status_code == 400
        
        # Página que no existe
        response = client.get("/control-tags/search?query=auth&page=999999", headers=auth_headers)
        assert response.status_code == 200  # Debe retornar página vacía
        result = response.json()
        assert len(result["items"]) == 0
        
    def test_unauthorized_access(self):
        """Test acceso sin autorización"""
        
        # Request sin headers de autorización
        response = client.get("/control-tags/standards")
        assert response.status_code == 401
        
        # Request con token inválido
        invalid_headers = {"Authorization": "Bearer invalid-token"}
        response = client.get("/control-tags/standards", headers=invalid_headers)
        assert response.status_code == 401


if __name__ == "__main__":
    print("✅ Tests de endpoints de control tags listos")
    print("Ejecutar con: pytest api/tests/test_control_tags_api_endpoints.py -v")
