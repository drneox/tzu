"""
Tests para endpoints específicos de control tags que hemos implementado
"""

import pytest
import json
from fastapi.testclient import TestClient

# Importar configuración de test
from tests.conftest import client, auth_headers, test_user, test_information_system

class TestControlTagsAPIEndpoints:
    """Tests para los endpoints específicos de control tags"""
    
    def test_get_all_standards_endpoint(self, auth_headers):
        """Test obtener todos los estándares disponibles"""
        response = client.get("/control-tags/standards", headers=auth_headers)
        
        assert response.status_code == 200
        response_data = response.json()
        
        assert "standards" in response_data
        assert "total_standards" in response_data
        
        standards = response_data["standards"]
        expected_standards = ["ASVS", "MASVS", "NIST", "ISO27001", "SBS"]
        assert set(standards) == set(expected_standards)
        assert len(standards) == 5
        assert response_data["total_standards"] == 5
        
    def test_get_standard_info_endpoint(self, auth_headers):
        """Test obtener información detallada de un estándar"""
        response = client.get("/control-tags/standards/ASVS", headers=auth_headers)
        
        assert response.status_code == 200
        asvs_info = response.json()
        
        assert asvs_info["name"] == "ASVS"
        assert asvs_info["controls_count"] == 90  # Actual count from the system
        assert "categories" in asvs_info
        assert "sample_controls" in asvs_info
        
    def test_search_control_tags_endpoint(self, auth_headers):
        """Test buscar control tags"""
        # Buscar tags de autenticación
        response = client.get("/control-tags/search?query=auth", headers=auth_headers)
        
        assert response.status_code == 200
        search_results = response.json()
        
        assert "results" in search_results
        assert "total" in search_results
        assert len(search_results["results"]) > 0
        
        # Los resultados son strings formateados, no objetos
        for result in search_results["results"][:3]:
            assert isinstance(result, str)
            assert "(" in result  # Should contain standard name in parentheses
        
    def test_batch_validate_tags_endpoint(self, auth_headers):
        """Test validar múltiples tags en batch"""
        tags_to_validate = [
            "V2.1.1",  # Valid ASVS tag
            "AUTH-1",  # Valid MASVS tag
            "PR.AC-1", # Valid NIST tag
            "A.9.1.1", # Valid ISO tag
            "SBS-2137-1", # Valid SBS tag
            "INVALID-TAG-1", # Invalid tag
            "ANOTHER-INVALID" # Invalid tag
        ]
        
        response = client.post("/control-tags/validate/batch", 
                             json=tags_to_validate,  # Send list directly
                             headers=auth_headers)
        
        assert response.status_code == 200
        results = response.json()
        
        assert "results" in results
        assert len(results["results"]) == len(tags_to_validate)
        
        # Contar válidos e inválidos
        valid_count = sum(1 for result in results["results"] if result["is_valid"])
        invalid_count = sum(1 for result in results["results"] if not result["is_valid"])
        
        assert valid_count == 5  # 5 tags válidos
        assert invalid_count == 2  # 2 tags inválidos
        
    def test_get_all_predefined_tags_endpoint(self, auth_headers):
        """Test get all predefined tags"""
        response = client.get("/control-tags/predefined", headers=auth_headers)
        
        assert response.status_code == 200
        all_tags = response.json()
        
        assert "total" in all_tags
        assert "tags" in all_tags
        assert all_tags["total"] == 335  # Total actual de controles según la salida del sistema
        assert len(all_tags["tags"]) == 335
        
        # Verificar que incluye tags de todos los estándares  
        tags_list = all_tags["tags"]
        
        # Now tags are objects with 'tag', 'tag_id', 'title', 'description', 'category', 'standard' fields
        # Extract tag_id for comparison (the raw tag without formatting)
        tag_ids = [tag["tag_id"] for tag in tags_list]
        
        # Just verify we have tags from each standard (relaxed counts)
        asvs_tags = [tag_id for tag_id in tag_ids if tag_id.startswith("V")]
        iso_tags = [tag_id for tag_id in tag_ids if tag_id.startswith("A.")]
        sbs_tags = [tag_id for tag_id in tag_ids if tag_id.startswith("SBS")]
        
        # Basic checks - verify we have tags from each standard
        assert len(asvs_tags) > 20   # ASVS has many tags
        assert len(iso_tags) > 50    # ISO27001 has many tags  
        assert len(sbs_tags) > 40    # SBS has many tags
        
        # Verify we have some MASVS and NIST tags
        assert any(tag_id.startswith("AUTH-") for tag_id in tag_ids)  # Some MASVS tags
        assert any("PR." in tag_id for tag_id in tag_ids)  # Some NIST tags
        
        # Verify the new object structure
        first_tag = tags_list[0]
        assert "tag" in first_tag  # Formatted tag with (STANDARD)
        assert "tag_id" in first_tag  # Raw tag ID
        assert "title" in first_tag
        assert "description" in first_tag
        assert "category" in first_tag
        assert "standard" in first_tag
        
        # Verify formatted tag contains standard in parentheses
        assert "(" in first_tag["tag"] and ")" in first_tag["tag"]
        
    def test_get_tag_details_endpoint(self, auth_headers):
        """Test obtener detalles específicos de un tag"""
        response = client.get("/control-tags/V2.1.1/details", headers=auth_headers)
        
        assert response.status_code == 200
        details = response.json()
        
        assert "standard" in details
        assert "title" in details
        assert "description" in details
        assert "category" in details
        
        assert details["standard"] == "ASVS"
        
    def test_validate_single_tag_endpoint(self, auth_headers):
        """Test validar un tag individual"""
        # Test tag válido
        response = client.get("/control-tags/validate/V2.1.1", headers=auth_headers)
        
        assert response.status_code == 200
        validation_result = response.json()
        
        assert "tag" in validation_result
        assert "is_valid" in validation_result
        assert validation_result["is_valid"] == True
        assert validation_result["tag"] == "V2.1.1"
        
        # Test tag inválido
        response = client.get("/control-tags/validate/INVALID-TAG", headers=auth_headers)
        
        assert response.status_code == 200
        validation_result = response.json()
        
        assert validation_result["is_valid"] == False
        assert validation_result["tag"] == "INVALID-TAG"
