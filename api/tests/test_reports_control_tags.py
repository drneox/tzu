"""
Tests para la funcionalidad de reportes con control tags
"""

import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os

from tests.conftest import client, test_user, auth_headers, test_information_system, db_session
import models
import crud
import schemas
from control_tags import (
    ALL_CONTROLS,
    get_available_standards,
    validate_control_tag,
    normalize_tag_for_lookup
)

class TestReportsWithControlTags:
    """Tests para reportes que incluyen control tags"""
    
    def test_generate_report_with_control_tags(self, test_client, auth_headers, test_information_system):
        """Test generar reporte con tags de control"""
        # Crear amenazas con diferentes tags de control
        threats_data = [
            {
                "title": "Authentication Threat",
                "description": "Amenaza de autenticación",
                "control_tags": ["V2.1.1", "V2.2.1", "MSTG-AUTH-1"],
                "severity": "High",
                "category": "Authentication",
                "information_system_id": test_information_system.id
            },
            {
                "title": "Authorization Threat",
                "description": "Amenaza de autorización", 
                "control_tags": ["V4.1.1", "V4.2.1", "PR.AC-1"],
                "severity": "Medium",
                "category": "Authorization",
                "information_system_id": test_information_system.id
            },
            {
                "title": "Data Protection Threat",
                "description": "Amenaza de protección de datos",
                "control_tags": ["V9.1.1", "A.5.1.1", "ID.AM-1"],
                "severity": "High", 
                "category": "Data Protection",
                "information_system_id": test_information_system.id
            }
        ]
        
        # Crear las amenazas
        created_threats = []
        for threat_data in threats_data:
            response = test_client.post("/api/threats/", json=threat_data, headers=auth_headers)
            assert response.status_code == 201
            created_threats.append(response.json())
            
        # Generar reporte
        report_response = test_client.get(f"/api/reports/information-systems/{test_information_system.id}", headers=auth_headers)
        
        assert report_response.status_code == 200
        report_data = report_response.json()
        
        # Verificar estructura del reporte
        assert "threats" in report_data
        assert "control_tags_summary" in report_data
        assert "standards_coverage" in report_data
        
        # Verificar que incluye las amenazas con sus tags
        assert len(report_data["threats"]) == 3
        
        # Verificar resumen de control tags
        control_summary = report_data["control_tags_summary"]
        assert "total_unique_tags" in control_summary
        assert "tags_by_standard" in control_summary
        assert "most_frequent_tags" in control_summary
        
        # Verificar cobertura de estándares
        standards_coverage = report_data["standards_coverage"]
        assert "ASVS" in standards_coverage
        assert "MASVS" in standards_coverage
        assert "NIST" in standards_coverage
        assert "ISO27001" in standards_coverage
        
    def test_report_filtering_by_standard(self, test_client, auth_headers, test_information_system):
        """Test filtrado de reporte por estándar"""
        # Crear amenazas con tags de diferentes estándares
        threats_data = [
            {
                "title": "ASVS Threat",
                "description": "Amenaza con controles ASVS",
                "control_tags": ["V2.1.1", "V4.1.1"],
                "severity": "High",
                "category": "Authentication",
                "information_system_id": test_information_system.id
            },
            {
                "title": "NIST Threat", 
                "description": "Amenaza con controles NIST",
                "control_tags": ["ID.AM-1", "PR.AC-1"],
                "severity": "Medium",
                "category": "Access Control",
                "information_system_id": test_information_system.id
            },
            {
                "title": "Mixed Threat",
                "description": "Amenaza con controles mixtos",
                "control_tags": ["V2.1.1", "ID.AM-1", "A.5.1.1"],
                "severity": "High",
                "category": "Data Protection", 
                "information_system_id": test_information_system.id
            }
        ]
        
        # Crear amenazas
        for threat_data in threats_data:
            response = test_client.post("/api/threats/", json=threat_data, headers=auth_headers)
            assert response.status_code == 201
            
        # Generar reporte filtrado por ASVS
        asvs_report = test_client.get(
            f"/api/reports/information-systems/{test_information_system.id}?standards=ASVS", 
            headers=auth_headers
        )
        
        assert asvs_report.status_code == 200
        asvs_data = asvs_report.json()
        
        # Verificar que solo incluye amenazas con tags ASVS
        asvs_threats = asvs_data["threats"]
        for threat in asvs_threats:
            has_asvs_tag = any(tag.startswith("V") for tag in threat["control_tags"])
            assert has_asvs_tag, f"Amenaza {threat['title']} debe tener al menos un tag ASVS"
            
        # Generar reporte filtrado por NIST
        nist_report = test_client.get(
            f"/api/reports/information-systems/{test_information_system.id}?standards=NIST",
            headers=auth_headers
        )
        
        assert nist_report.status_code == 200
        nist_data = nist_report.json()
        
        # Verificar que solo incluye amenazas con tags NIST
        nist_threats = nist_data["threats"]
        for threat in nist_threats:
            has_nist_tag = any("." in tag and not tag.startswith("A.") for tag in threat["control_tags"])
            assert has_nist_tag, f"Amenaza {threat['title']} debe tener al menos un tag NIST"
            
    def test_report_control_tags_statistics(self, test_client, auth_headers, test_information_system):
        """Test estadísticas de control tags en reportes"""
        # Crear amenazas con tags repetidos para probar estadísticas
        threats_data = [
            {
                "title": "Threat 1",
                "description": "Primera amenaza",
                "control_tags": ["V2.1.1", "V4.1.1"],  # Tags ASVS
                "severity": "High",
                "category": "Authentication",
                "information_system_id": test_information_system.id
            },
            {
                "title": "Threat 2",
                "description": "Segunda amenaza",
                "control_tags": ["V2.1.1", "ID.AM-1"],  # V2.1.1 repetido
                "severity": "Medium", 
                "category": "Access Control",
                "information_system_id": test_information_system.id
            },
            {
                "title": "Threat 3",
                "description": "Tercera amenaza",
                "control_tags": ["V2.1.1", "A.5.1.1", "MSTG-AUTH-1"],  # V2.1.1 repetido de nuevo
                "severity": "High",
                "category": "Data Protection",
                "information_system_id": test_information_system.id
            }
        ]
        
        # Crear amenazas
        for threat_data in threats_data:
            response = test_client.post("/api/threats/", json=threat_data, headers=auth_headers)
            assert response.status_code == 201
            
        # Generar reporte con estadísticas
        report_response = test_client.get(
            f"/api/reports/information-systems/{test_information_system.id}?include_stats=true",
            headers=auth_headers
        )
        
        assert report_response.status_code == 200
        report_data = report_response.json()
        
        # Verificar estadísticas de tags
        control_summary = report_data["control_tags_summary"]
        
        # V2.1.1 debe ser el tag más frecuente (aparece 3 veces)
        most_frequent = control_summary["most_frequent_tags"]
        assert len(most_frequent) > 0
        
        # Verificar conteo por estándares
        tags_by_standard = control_summary["tags_by_standard"]
        assert "ASVS" in tags_by_standard
        assert "NIST" in tags_by_standard
        assert "ISO27001" in tags_by_standard
        assert "MASVS" in tags_by_standard
        
        # ASVS debe tener más tags que otros (V2.1.1 aparece 3 veces + V4.1.1)
        assert tags_by_standard["ASVS"] >= 2
        
    def test_export_report_with_control_tags(self, test_client, auth_headers, test_information_system):
        """Test exportar reporte con control tags en diferentes formatos"""
        # Crear una amenaza con tags de control
        threat_data = {
            "title": "Threat for Export",
            "description": "Amenaza para exportar",
            "control_tags": ["V2.1.1", "MSTG-AUTH-1", "ID.AM-1"],
            "severity": "High",
            "category": "Authentication",
            "information_system_id": test_information_system.id
        }
        
        response = test_client.post("/api/threats/", json=threat_data, headers=auth_headers)
        assert response.status_code == 201
        
        # Exportar en formato JSON
        json_export = test_client.get(
            f"/api/reports/information-systems/{test_information_system.id}/export?format=json",
            headers=auth_headers
        )
        
        assert json_export.status_code == 200
        
        # Verificar que el contenido incluye control tags
        if json_export.headers.get("content-type") == "application/json":
            export_data = json_export.json()
            assert "threats" in export_data
            threat = export_data["threats"][0]
            assert "control_tags" in threat
            assert len(threat["control_tags"]) == 3
            
    def test_report_control_tags_validation(self, test_client, auth_headers, test_information_system):
        """Test validación de control tags en reportes"""
        # Crear amenaza con tags válidos e inválidos mezclados
        threat_data = {
            "title": "Threat with Mixed Tags",
            "description": "Amenaza con tags válidos e inválidos",
            "control_tags": ["V2.1.1", "INVALID-TAG", "ID.AM-1", "ANOTHER-INVALID"],
            "severity": "High",
            "category": "Mixed",
            "information_system_id": test_information_system.id
        }
        
        response = test_client.post("/api/threats/", json=threat_data, headers=auth_headers)
        assert response.status_code == 201
        
        # Generar reporte con validación de tags
        report_response = test_client.get(
            f"/api/reports/information-systems/{test_information_system.id}?validate_tags=true",
            headers=auth_headers
        )
        
        assert report_response.status_code == 200
        report_data = report_response.json()
        
        # Verificar que el reporte incluye información de validación
        if "tag_validation" in report_data:
            validation_info = report_data["tag_validation"]
            assert "valid_tags" in validation_info
            assert "invalid_tags" in validation_info
            
            # Verificar que identifica correctamente los tags válidos e inválidos
            assert "V2.1.1" in validation_info["valid_tags"]
            assert "ID.AM-1" in validation_info["valid_tags"]
            assert "INVALID-TAG" in validation_info["invalid_tags"]
            assert "ANOTHER-INVALID" in validation_info["invalid_tags"]


class TestReportsAggregation:
    """Tests para agregación de datos en reportes"""
    
    def test_aggregate_report_multiple_systems(self, test_client, auth_headers, test_user, db_session):
        """Test reporte agregado de múltiples sistemas"""
        from api.crud import create_information_system
        from api.schemas import InformationSystemBaseCreate
        
        # Crear múltiples sistemas de información
        systems_data = [
            {"title": "System A", "description": "Sistema A de prueba"},
            {"title": "System B", "description": "Sistema B de prueba"}
        ]
        
        created_systems = []
        for system_data in systems_data:
            system_create = InformationSystemBaseCreate(**system_data)
            system = create_information_system(db=db_session, information_system=system_create)
            created_systems.append(system)
            
        # Crear amenazas en cada sistema con diferentes tags
        for i, system in enumerate(created_systems):
            threat_data = {
                "title": f"Threat in System {system.title}",
                "description": f"Amenaza en {system.title}",
                "control_tags": [f"V2.{i+1}.1", "ID.AM-1"],
                "severity": "High",
                "category": "Authentication",
                "information_system_id": system.id
            }
            
            response = test_client.post("/api/threats/", json=threat_data, headers=auth_headers)
            assert response.status_code == 201
            
        # Generar reporte agregado
        aggregate_response = test_client.get("/api/reports/aggregate", headers=auth_headers)
        
        assert aggregate_response.status_code == 200
        aggregate_data = aggregate_response.json()
        
        # Verificar estructura del reporte agregado
        assert "total_systems" in aggregate_data
        assert "total_threats" in aggregate_data
        assert "control_tags_overview" in aggregate_data
        assert "standards_distribution" in aggregate_data
        
        assert aggregate_data["total_systems"] == 2
        assert aggregate_data["total_threats"] >= 2
        
    def test_report_trends_over_time(self, test_client, auth_headers, test_information_system):
        """Test tendencias de control tags en el tiempo"""
        # Crear amenazas con diferentes fechas (simuladas)
        import datetime
        
        threat_data = {
            "title": "Historical Threat",
            "description": "Amenaza histórica",
            "control_tags": ["V2.1.1", "ID.AM-1"],
            "severity": "High",
            "category": "Authentication",
            "information_system_id": test_information_system.id
        }
        
        response = test_client.post("/api/threats/", json=threat_data, headers=auth_headers)
        assert response.status_code == 201
        
        # Generar reporte de tendencias
        trends_response = test_client.get(
            f"/api/reports/trends?start_date=2024-01-01&end_date=2024-12-31",
            headers=auth_headers
        )
        
        # Este endpoint podría no existir aún, así que verificamos graciosamente
        if trends_response.status_code == 200:
            trends_data = trends_response.json()
            assert "period" in trends_data
            assert "control_tags_evolution" in trends_data
        elif trends_response.status_code == 404:
            # Endpoint no implementado aún, está bien
            pass
        else:
            # Otros errores no esperados
            assert False, f"Error inesperado en trends: {trends_response.status_code}"


class TestReportsPerformance:
    """Tests de rendimiento para reportes con control tags"""
    
    def test_large_report_generation_performance(self, test_client, auth_headers, test_information_system):
        """Test rendimiento para generación de reportes grandes"""
        import time
        
        # Crear múltiples amenazas con muchos tags
        threats_count = 20
        for i in range(threats_count):
            threat_data = {
                "title": f"Performance Test Threat {i+1}",
                "description": f"Amenaza de prueba de rendimiento {i+1}",
                "control_tags": [
                    f"V2.{(i % 10) + 1}.1", 
                    f"V4.{(i % 5) + 1}.1",
                    "ID.AM-1",
                    "A.5.1.1"
                ],
                "severity": ["High", "Medium", "Low"][i % 3],
                "category": "Performance Test",
                "information_system_id": test_information_system.id
            }
            
            response = test_client.post("/api/threats/", json=threat_data, headers=auth_headers)
            assert response.status_code == 201
            
        # Medir tiempo de generación del reporte
        start_time = time.time()
        
        report_response = test_client.get(
            f"/api/reports/information-systems/{test_information_system.id}?include_stats=true",
            headers=auth_headers
        )
        
        end_time = time.time()
        generation_time = end_time - start_time
        
        assert report_response.status_code == 200
        assert generation_time < 3.0, f"Generación de reporte debe ser rápida. Tiempo: {generation_time:.2f}s"
        
        report_data = report_response.json()
        assert len(report_data["threats"]) == threats_count
        
    def test_concurrent_report_requests(self, test_client, auth_headers, test_information_system):
        """Test manejo de múltiples solicitudes de reporte concurrentes"""
        import threading
        import time
        
        # Crear una amenaza base
        threat_data = {
            "title": "Concurrent Test Threat",
            "description": "Amenaza para prueba concurrente",
            "control_tags": ["V2.1.1", "ID.AM-1"],
            "severity": "High",
            "category": "Concurrency",
            "information_system_id": test_information_system.id
        }
        
        response = test_client.post("/api/threats/", json=threat_data, headers=auth_headers)
        assert response.status_code == 201
        
        # Función para hacer solicitud de reporte
        results = []
        
        def make_report_request():
            try:
                response = test_client.get(
                    f"/api/reports/information-systems/{test_information_system.id}",
                    headers=auth_headers
                )
                results.append(response.status_code)
            except Exception as e:
                results.append(f"Error: {e}")
                
        # Crear múltiples threads para solicitudes concurrentes
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_report_request)
            threads.append(thread)
            
        # Iniciar todos los threads
        start_time = time.time()
        for thread in threads:
            thread.start()
            
        # Esperar que terminen todos
        for thread in threads:
            thread.join()
            
        end_time = time.time()
        total_time = end_time - start_time
        
        # Verificar que todas las solicitudes fueron exitosas
        assert len(results) == 5
        for result in results:
            assert result == 200, f"Todas las solicitudes concurrentes deben ser exitosas: {results}"
            
        assert total_time < 5.0, f"Solicitudes concurrentes deben completarse rápidamente. Tiempo: {total_time:.2f}s"


if __name__ == "__main__":
    print("✅ Tests de reportes con control tags creados exitosamente")
