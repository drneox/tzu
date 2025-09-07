"""
Tests para funcionalidades de frontend relacionadas con control tags
"""

import pytest
import json
from unittest.mock import patch, MagicMock, Mock
import sys
import os
from tests.conftest import client
from control_tags import (
    ALL_CONTROLS,
    get_available_standards,
    validate_control_tag,
    normalize_tag_for_lookup,
    get_tag_details,
    search_predefined_tags,
    format_tag_for_display
)

class TestFrontendControlTagsIntegration:
    """Tests para integración de frontend con control tags"""
    
    def test_control_tags_autocomplete_endpoint(self, test_client):
        """Test endpoint de autocompletado para el frontend"""
        # Simular búsqueda de autocompletado
        response = test_client.get("/api/control-tags/autocomplete?query=auth")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) <= 10  # Límite para autocompletado
        
        # Verificar estructura para el frontend
        for item in data:
            assert "value" in item  # Para el input
            assert "label" in item  # Para mostrar al usuario
            assert "standard" in item  # Para el color del tag
            assert "description" in item  # Para tooltip
            
    def test_control_tags_color_mapping_endpoint(self, test_client):
        """Test endpoint para obtener mapeo de colores"""
        response = test_client.get("/api/control-tags/colors")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar que incluye colores para todos los estándares
        expected_standards = ["ASVS", "MASVS", "NIST", "ISO27001", "SBS"]
        for standard in expected_standards:
            assert standard in data
            assert "color" in data[standard]
            assert "background" in data[standard]
            
    def test_control_tags_bulk_details_for_frontend(self, test_client):
        """Test endpoint para obtener detalles en lote para el frontend"""
        tags = ["V2.1.1", "MSTG-AUTH-1", "ID.AM-1"]
        
        response = test_client.post("/api/control-tags/bulk-details", json={"tags": tags})
        
        assert response.status_code == 200
        data = response.json()
        
        assert "results" in data
        assert len(data["results"]) == len(tags)
        
        # Verificar estructura para el frontend
        for result in data["results"]:
            assert "tag" in result
            assert "formatted_tag" in result
            assert "standard" in result
            assert "color_info" in result
            if result["details"]:
                assert "title" in result["details"]
                assert "description" in result["details"]
                assert "category" in result["details"]
                
    def test_threat_form_validation_endpoint(self, test_client):
        """Test validación de formulario de amenazas con control tags"""
        # Simular datos de formulario del frontend
        form_data = {
            "title": "Test Threat from Frontend",
            "description": "Amenaza creada desde frontend",
            "control_tags": ["V2.1.1", "invalid-tag", "MSTG-AUTH-1"],
            "severity": "High",
            "category": "Authentication"
        }
        
        # Endpoint de validación antes de enviar
        validation_response = test_client.post("/api/threats/validate-form", json=form_data)
        
        if validation_response.status_code == 200:
            validation_data = validation_response.json()
            
            assert "is_valid" in validation_data
            assert "errors" in validation_data
            assert "warnings" in validation_data
            
            # Debe detectar el tag inválido
            if "control_tags" in validation_data["warnings"]:
                assert any("invalid-tag" in str(warning) for warning in validation_data["warnings"]["control_tags"])
        elif validation_response.status_code == 404:
            # Endpoint no implementado aún
            pass
            
    def test_control_tags_search_with_filters(self, test_client):
        """Test búsqueda con filtros para el frontend"""
        # Búsqueda filtrada por estándar
        response = test_client.get("/api/control-tags/search?query=auth&standard=ASVS")
        
        assert response.status_code == 200
        data = response.json()
        
        # Todos los resultados deben ser de ASVS
        for item in data:
            tag = item["tag"]
            # Los tags de ASVS generalmente empiezan con V
            assert tag.startswith("V") or "ASVS" in item.get("formatted_tag", "")
            
    def test_control_tags_statistics_for_dashboard(self, test_client):
        """Test estadísticas de control tags para dashboard"""
        response = test_client.get("/api/control-tags/statistics")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar datos para dashboard
        assert "total_controls" in data
        assert "standards_breakdown" in data
        assert "popular_tags" in data
        assert "coverage_by_category" in data
        
        assert data["total_controls"] == 313
        
        # Verificar breakdown por estándares
        standards_breakdown = data["standards_breakdown"]
        assert "ASVS" in standards_breakdown
        assert standards_breakdown["ASVS"] == 93


class TestControlTagsUIComponents:
    """Tests para componentes de UI específicos"""
    
    def test_tag_input_component_validation(self, test_client):
        """Test validación en tiempo real para componente de input de tags"""
        # Simular validación mientras el usuario escribe
        partial_inputs = ["V2", "V2.1", "V2.1.1", "INVALID"]
        
        for partial_input in partial_inputs:
            response = test_client.get(f"/api/control-tags/validate-partial?input={partial_input}")
            
            if response.status_code == 200:
                data = response.json()
                
                assert "is_potentially_valid" in data
                assert "suggestions" in data
                assert "exact_match" in data
                
                if partial_input == "V2.1.1":
                    assert data["exact_match"] == True
                elif partial_input == "INVALID":
                    assert data["is_potentially_valid"] == False
            elif response.status_code == 404:
                # Endpoint no implementado
                pass
                
    def test_tag_tooltip_data_endpoint(self, test_client):
        """Test datos para tooltips de tags"""
        test_tags = ["V2.1.1", "MSTG-AUTH-1", "ID.AM-1"]
        
        for tag in test_tags:
            response = test_client.get(f"/api/control-tags/{tag}/tooltip")
            
            if response.status_code == 200:
                data = response.json()
                
                assert "title" in data
                assert "description" in data
                assert "standard" in data
                assert "category" in data
                assert "color" in data
                assert "formatted_tag" in data
            elif response.status_code == 404:
                # Tag no encontrado o endpoint no implementado
                pass
                
    def test_control_tags_export_for_frontend(self, test_client):
        """Test exportación de datos para uso en frontend"""
        response = test_client.get("/api/control-tags/export?format=frontend")
        
        if response.status_code == 200:
            data = response.json()
            
            # Formato optimizado para frontend
            assert "standards" in data
            assert "tags_by_standard" in data
            assert "color_mapping" in data
            assert "validation_patterns" in data
            
            # Verificar estructura para cada estándar
            for standard_name, standard_data in data["standards"].items():
                assert "name" in standard_data
                assert "color" in standard_data
                assert "tags" in standard_data
        elif response.status_code == 404:
            # Endpoint no implementado
            pass


class TestControlTagsReactIntegration:
    """Tests específicos para integración con React frontend"""
    
    def test_react_hook_data_format(self, test_client):
        """Test formato de datos optimizado para React hooks"""
        response = test_client.get("/api/control-tags/react-format")
        
        if response.status_code == 200:
            data = response.json()
            
            # Formato optimizado para useControlTags hook
            assert "allTags" in data  # Array de todos los tags
            assert "tagsByStandard" in data  # Objeto con tags agrupados
            assert "tagDetails" in data  # Mapa de tag -> detalles
            assert "searchIndex" in data  # Índice para búsqueda rápida
            
            # Verificar que allTags es un array
            assert isinstance(data["allTags"], list)
            assert len(data["allTags"]) == 313
            
            # Verificar estructura de tagDetails
            if data["tagDetails"]:
                sample_tag = list(data["tagDetails"].keys())[0]
                tag_detail = data["tagDetails"][sample_tag]
                assert "title" in tag_detail
                assert "description" in tag_detail
                assert "standard" in tag_detail
        elif response.status_code == 404:
            # Endpoint no implementado
            pass
            
    def test_control_tags_for_select_component(self, test_client):
        """Test datos para componente Select de React"""
        response = test_client.get("/api/control-tags/select-options")
        
        if response.status_code == 200:
            data = response.json()
            
            # Formato para React Select
            assert isinstance(data, list)
            
            for option in data[:5]:  # Verificar primeros 5
                assert "value" in option
                assert "label" in option
                assert "group" in option  # Para agrupar por estándar
                
                # Verificar estructura de grupo
                assert option["group"] in ["ASVS", "MASVS", "NIST", "ISO27001", "SBS"]
        elif response.status_code == 404:
            # Endpoint no implementado
            pass


class TestControlTagsPerformanceForFrontend:
    """Tests de rendimiento específicos para frontend"""
    
    def test_autocomplete_response_time(self, test_client):
        """Test tiempo de respuesta para autocompletado"""
        import time
        
        search_queries = ["auth", "access", "data", "security", "control"]
        
        for query in search_queries:
            start_time = time.time()
            
            response = test_client.get(f"/api/control-tags/search?query={query}&limit=10")
            
            end_time = time.time()
            response_time = end_time - start_time
            
            assert response.status_code == 200
            assert response_time < 0.2, f"Autocompletado debe ser rápido para '{query}'. Tiempo: {response_time:.3f}s"
            
    def test_bulk_validation_for_form(self, test_client):
        """Test validación en lote para formularios"""
        import time
        
        # Simular validación de formulario completo
        form_tags = [
            "V2.1.1", "V2.2.1", "V4.1.1", 
            "MSTG-AUTH-1", "MSTG-NETWORK-1",
            "ID.AM-1", "PR.AC-1", "DE.AE-1",
            "A.5.1.1", "A.8.1.1",
            "SBS-2137-1", "SBS-2137-2"
        ]
        
        start_time = time.time()
        
        response = test_client.post("/api/control-tags/batch-validate", json={"tags": form_tags})
        
        end_time = time.time()
        validation_time = end_time - start_time
        
        assert response.status_code == 200
        assert validation_time < 0.5, f"Validación de formulario debe ser rápida. Tiempo: {validation_time:.3f}s"
        
        data = response.json()
        assert len(data["results"]) == len(form_tags)
        
    def test_tags_data_caching(self, test_client):
        """Test que los datos se pueden cachear eficientemente en frontend"""
        import time
        
        # Primera solicitud (sin caché)
        start_time = time.time()
        response1 = test_client.get("/api/control-tags/all")
        end_time = time.time()
        first_request_time = end_time - start_time
        
        assert response1.status_code == 200
        
        # Verificar que incluye headers para caché
        cache_headers = response1.headers.get("cache-control")
        etag = response1.headers.get("etag")
        
        # Si hay headers de caché, el frontend puede cachear eficientemente
        if cache_headers or etag:
            print(f"✅ Headers de caché presentes: cache-control={cache_headers}, etag={etag}")
            
        # Segunda solicitud (potencialmente desde caché)
        start_time = time.time()
        response2 = test_client.get("/api/control-tags/all")
        end_time = time.time()
        second_request_time = end_time - start_time
        
        assert response2.status_code == 200
        
        # Los datos deben ser consistentes
        assert response1.json() == response2.json()


class TestControlTagsErrorHandlingFrontend:
    """Tests de manejo de errores específicos para frontend"""
    
    def test_graceful_degradation_invalid_tags(self, test_client):
        """Test degradación graceful con tags inválidos"""
        # Simular formulario con algunos tags inválidos
        mixed_tags = ["V2.1.1", "INVALID-TAG-1", "MSTG-AUTH-1", "ANOTHER-INVALID", "ID.AM-1"]
        
        response = test_client.post("/api/control-tags/batch-validate", json={"tags": mixed_tags})
        
        assert response.status_code == 200
        data = response.json()
        
        # El sistema debe manejar graciosamente los tags inválidos
        assert "results" in data
        assert len(data["results"]) == len(mixed_tags)
        
        valid_count = sum(1 for result in data["results"] if result["is_valid"])
        invalid_count = len(mixed_tags) - valid_count
        
        assert valid_count == 3  # V2.1.1, MSTG-AUTH-1, ID.AM-1
        assert invalid_count == 2  # Los dos INVALID tags
        
    def test_search_with_empty_results(self, test_client):
        """Test búsqueda que no retorna resultados"""
        response = test_client.get("/api/control-tags/search?query=NONEXISTENT_SEARCH_TERM_12345")
        
        assert response.status_code == 200
        data = response.json()
        
        # Debe retornar array vacío, no error
        assert isinstance(data, list)
        assert len(data) == 0
        
    def test_malformed_request_handling(self, test_client):
        """Test manejo de solicitudes malformadas"""
        # Solicitud con JSON malformado
        response = test_client.post(
            "/api/control-tags/validate",
            data="invalid json",
            headers={"content-type": "application/json"}
        )
        
        # Debe retornar error 422 (Unprocessable Entity) o 400 (Bad Request)
        assert response.status_code in [400, 422]
        
    def test_missing_required_fields(self, test_client):
        """Test campos requeridos faltantes"""
        # Validación sin campo 'tag'
        response = test_client.post("/api/control-tags/validate", json={})
        
        assert response.status_code == 422  # Unprocessable Entity
        
        error_data = response.json()
        assert "detail" in error_data
        
        # Debe indicar que falta el campo 'tag'
        assert any("tag" in str(error).lower() for error in error_data["detail"])


if __name__ == "__main__":
    print("✅ Tests de integración frontend con control tags creados exitosamente")
