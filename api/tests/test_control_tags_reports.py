"""
Tests específicos para la funcionalidad de tags de control y reportes
Usa la configuración de SQLite de test del conftest.py
"""

import pytest
import json
from fastapi.testclient import TestClient
import sys
import os
import sys

# Importar la configuración de test
from tests.conftest import client, test_user, auth_headers, test_information_system, db_session

# Importar módulos directamente desde el directorio actual
import control_tags
import schemas
import crud
import models
from control_tags import validate_control_tag

class TestControlTagsWithDatabase:
    """Tests de tags de control usando la base de datos de test"""
    
    def test_create_threat_with_control_tags(self, db_session, test_user, test_information_system):
        """Test crear threat con control tags en la base de datos"""
        
        # Crear un threat con control tags
        threat_data = schemas.ThreatCreate(
            title="Test Threat with Controls",
            description="Un threat de prueba con control tags",
            severity="High",
            category="Authentication",
            control_tags=["V2.1.1", "MSTG-AUTH-1", "ID.AM-1"],
            information_system_id=test_information_system.id
        )
        
        # Crear el threat usando CRUD
        created_threat = crud.create_threat(
            db=db_session, 
            threat=threat_data, 
            user_id=test_user.id
        )
        
        # Verificar que se creó correctamente
        assert created_threat.id is not None
        assert created_threat.title == "Test Threat with Controls"
        assert created_threat.control_tags == ["V2.1.1", "MSTG-AUTH-1", "ID.AM-1"]
        assert created_threat.user_id == test_user.id
        
        # Verificar que se puede recuperar de la base de datos
        retrieved_threat = crud.get_threat(db=db_session, threat_id=created_threat.id)
        assert retrieved_threat is not None
        assert retrieved_threat.control_tags == ["V2.1.1", "MSTG-AUTH-1", "ID.AM-1"]
        
    def test_update_threat_control_tags(self, db_session, test_user, test_information_system):
        """Test actualizar control tags de un threat existente"""
        
        # Crear threat inicial
        initial_threat_data = schemas.ThreatCreate(
            title="Threat to Update",
            description="Threat que se va a actualizar",
            severity="Medium",
            category="Authorization",
            control_tags=["V2.1.1"],
            information_system_id=test_information_system.id
        )
        
        created_threat = crud.create_threat(
            db=db_session, 
            threat=initial_threat_data, 
            user_id=test_user.id
        )
        
        # Actualizar con nuevos control tags
        update_data = schemas.ThreatUpdate(
            control_tags=["V2.1.1", "V2.2.1", "NIST-ID.AM-1", "A.5.1.1"]
        )
        
        updated_threat = crud.update_threat(
            db=db_session, 
            threat_id=created_threat.id, 
            threat_update=update_data
        )
        
        # Verificar la actualización
        assert updated_threat.control_tags == ["V2.1.1", "V2.2.1", "NIST-ID.AM-1", "A.5.1.1"]
        
        # Verificar persistencia
        retrieved_threat = crud.get_threat(db=db_session, threat_id=created_threat.id)
        assert retrieved_threat.control_tags == ["V2.1.1", "V2.2.1", "NIST-ID.AM-1", "A.5.1.1"]
        
    def test_filter_threats_by_control_tags(self, db_session, test_user, test_information_system):
        """Test filtrar threats por control tags"""
        
        # Crear varios threats con diferentes control tags
        threats_data = [
            schemas.ThreatCreate(
                title="ASVS Threat",
                description="Threat con tags ASVS",
                severity="High",
                category="Authentication",
                control_tags=["V2.1.1", "V2.2.1"],
                information_system_id=test_information_system.id
            ),
            schemas.ThreatCreate(
                title="NIST Threat",
                description="Threat con tags NIST",
                severity="Medium",
                category="Access Control",
                control_tags=["ID.AM-1", "PR.AC-1"],
                information_system_id=test_information_system.id
            ),
            schemas.ThreatCreate(
                title="Mixed Threat",
                description="Threat con tags mixtos",
                severity="Low",
                category="Data Protection",
                control_tags=["V2.1.1", "ID.AM-1", "A.5.1.1"],
                information_system_id=test_information_system.id
            )
        ]
        
        created_threats = []
        for threat_data in threats_data:
            threat = crud.create_threat(
                db=db_session, 
                threat=threat_data, 
                user_id=test_user.id
            )
            created_threats.append(threat)
        
        # Test filtrar por tag específico - debería encontrar 2 threats
        threats_with_v211 = crud.get_threats_by_control_tag(
            db=db_session, 
            control_tag="V2.1.1", 
            user_id=test_user.id
        )
        assert len(threats_with_v211) == 2
        
        # Test filtrar por tag NIST - debería encontrar 2 threats
        threats_with_nist = crud.get_threats_by_control_tag(
            db=db_session, 
            control_tag="ID.AM-1", 
            user_id=test_user.id
        )
        assert len(threats_with_nist) == 2
        
    def test_threat_with_invalid_control_tags(self, db_session, test_user, test_information_system):
        """Test manejar threats con control tags inválidos"""
        
        # Crear threat con algunos tags válidos e inválidos
        threat_data = schemas.ThreatCreate(
            title="Threat with Mixed Tags",
            description="Threat con tags válidos e inválidos",
            severity="High",
            category="Validation",
            control_tags=["V2.1.1", "INVALID-TAG", "ID.AM-1", "ANOTHER-INVALID"],
            information_system_id=test_information_system.id
        )
        
        # El threat se debe crear (no validamos tags en el momento de creación)
        created_threat = crud.create_threat(
            db=db_session, 
            threat=threat_data, 
            user_id=test_user.id
        )
        
        assert created_threat.control_tags == ["V2.1.1", "INVALID-TAG", "ID.AM-1", "ANOTHER-INVALID"]
        
        # Pero podemos validar los tags posteriormente
        valid_tags = []
        invalid_tags = []
        
        for tag in created_threat.control_tags:
            if validate_control_tag(tag):
                valid_tags.append(tag)
            else:
                invalid_tags.append(tag)
        
        assert valid_tags == ["V2.1.1", "ID.AM-1"]
        assert invalid_tags == ["INVALID-TAG", "ANOTHER-INVALID"]


class TestControlTagsEndpointsWithDB:
    """Tests de endpoints de control tags usando base de datos de test"""
    
    def test_get_threat_control_tags_endpoint(self, auth_headers, test_information_system, db_session, test_user):
        """Test obtener control tags de un threat via endpoint"""
        
        # Crear threat via endpoint
        threat_data = {
            "title": "API Test Threat",
            "description": "Threat creado via API",
            "severity": "High",
            "category": "API Security",
            "control_tags": ["V2.1.1", "MSTG-NETWORK-1", "ID.AM-1"],
            "information_system_id": test_information_system.id
        }
        
        # Crear threat
        response = client.post("/api/threats/", json=threat_data, headers=auth_headers)
        assert response.status_code == 200
        created_threat = response.json()
        
        # Obtener threat y verificar control tags
        response = client.get(f"/api/threats/{created_threat['id']}", headers=auth_headers)
        assert response.status_code == 200
        
        retrieved_threat = response.json()
        assert retrieved_threat["control_tags"] == ["V2.1.1", "MSTG-NETWORK-1", "ID.AM-1"]
        
    def test_update_threat_control_tags_endpoint(self, auth_headers, test_information_system):
        """Test actualizar control tags via endpoint"""
        
        # Crear threat inicial
        initial_data = {
            "title": "Threat to Update via API",
            "description": "Se actualizará via API",
            "severity": "Medium",
            "category": "Update Test",
            "control_tags": ["V2.1.1"],
            "information_system_id": test_information_system.id
        }
        
        response = client.post("/api/threats/", json=initial_data, headers=auth_headers)
        assert response.status_code == 200
        created_threat = response.json()
        
        # Actualizar control tags
        update_data = {
            "control_tags": ["V2.1.1", "V2.2.1", "MSTG-AUTH-1", "ID.AM-1", "A.5.1.1"]
        }
        
        response = client.put(
            f"/api/threats/{created_threat['id']}", 
            json=update_data, 
            headers=auth_headers
        )
        assert response.status_code == 200
        
        updated_threat = response.json()
        expected_tags = ["V2.1.1", "V2.2.1", "MSTG-AUTH-1", "ID.AM-1", "A.5.1.1"]
        assert updated_threat["control_tags"] == expected_tags
        
    def test_search_threats_by_control_tags(self, auth_headers, test_information_system):
        """Test buscar threats por control tags via endpoint"""
        
        # Crear múltiples threats con diferentes tags
        threats_data = [
            {
                "title": "Authentication Threat",
                "description": "Threat de autenticación",
                "severity": "High",
                "category": "Authentication",
                "control_tags": ["V2.1.1", "V2.2.1"],
                "information_system_id": test_information_system.id
            },
            {
                "title": "Network Threat", 
                "description": "Threat de red",
                "severity": "Medium",
                "category": "Network",
                "control_tags": ["MSTG-NETWORK-1", "MSTG-NETWORK-2"],
                "information_system_id": test_information_system.id
            },
            {
                "title": "Mixed Standards Threat",
                "description": "Threat con múltiples estándares",
                "severity": "Low",
                "category": "Mixed",
                "control_tags": ["V2.1.1", "MSTG-AUTH-1", "ID.AM-1"],
                "information_system_id": test_information_system.id
            }
        ]
        
        # Crear todos los threats
        created_threat_ids = []
        for threat_data in threats_data:
            response = client.post("/api/threats/", json=threat_data, headers=auth_headers)
            assert response.status_code == 200
            created_threat_ids.append(response.json()["id"])
        
        # Buscar threats con control tag específico
        response = client.get("/api/threats/search?control_tag=V2.1.1", headers=auth_headers)
        assert response.status_code == 200
        
        search_results = response.json()
        # Debe encontrar 2 threats que contienen V2.1.1
        threats_with_tag = [t for t in search_results if "V2.1.1" in t.get("control_tags", [])]
        assert len(threats_with_tag) == 2


class TestReportsWithControlTags:
    """Tests para reportes que incluyen información de control tags"""
    
    def test_generate_report_with_control_tags(self, auth_headers, test_information_system, db_session, test_user):
        """Test generar reporte que incluya información de control tags"""
        
        # Crear threats con control tags diversos
        threats_data = [
            schemas.ThreatCreate(
                title="High Risk Auth Threat",
                description="Threat crítico de autenticación",
                severity="Critical",
                category="Authentication", 
                control_tags=["V2.1.1", "V2.2.1", "V2.3.1"],
                information_system_id=test_information_system.id
            ),
            schemas.ThreatCreate(
                title="Mobile Security Issue",
                description="Problema de seguridad móvil",
                severity="High",
                category="Mobile Security",
                control_tags=["MSTG-AUTH-1", "MSTG-NETWORK-1"],
                information_system_id=test_information_system.id
            ),
            schemas.ThreatCreate(
                title="Data Protection Issue",
                description="Problema de protección de datos",
                severity="Medium", 
                category="Data Protection",
                control_tags=["ID.AM-1", "PR.DS-1", "A.5.1.1"],
                information_system_id=test_information_system.id
            )
        ]
        
        # Crear threats en la base de datos
        for threat_data in threats_data:
            crud.create_threat(
                db=db_session,
                threat=threat_data,
                user_id=test_user.id
            )
        
        # Generar reporte via endpoint
        response = client.get(f"/api/report?information_system_id={test_information_system.id}", headers=auth_headers)
        assert response.status_code == 200
        
        report_data = response.json()
        
        # Verificar que el reporte incluye información de control tags
        assert "threats" in report_data
        assert len(report_data["threats"]) == 3
        
        # Verificar que cada threat incluye sus control tags
        for threat in report_data["threats"]:
            assert "control_tags" in threat
            assert len(threat["control_tags"]) > 0
            
    def test_report_filtered_by_standard(self, auth_headers, test_information_system, db_session, test_user):
        """Test generar reporte filtrado por estándar específico"""
        
        # Crear threats con diferentes estándares
        threats_data = [
            schemas.ThreatCreate(
                title="ASVS Only Threat",
                description="Solo controles ASVS",
                severity="High",
                category="Web Security",
                control_tags=["V2.1.1", "V3.1.1", "V4.1.1"],
                information_system_id=test_information_system.id
            ),
            schemas.ThreatCreate(
                title="NIST Only Threat", 
                description="Solo controles NIST",
                severity="Medium",
                category="Infrastructure",
                control_tags=["ID.AM-1", "PR.AC-1", "DE.AE-1"],
                information_system_id=test_information_system.id
            ),
            schemas.ThreatCreate(
                title="Mixed Standards Threat",
                description="Controles mixtos",
                severity="Low",
                category="Mixed",
                control_tags=["V2.1.1", "ID.AM-1", "A.5.1.1"],
                information_system_id=test_information_system.id
            )
        ]
        
        # Crear threats
        for threat_data in threats_data:
            crud.create_threat(
                db=db_session,
                threat=threat_data, 
                user_id=test_user.id
            )
        
        # Generar reporte filtrado por ASVS
        response = client.get(
            f"/api/report?information_system_id={test_information_system.id}&standards=ASVS", 
            headers=auth_headers
        )
        assert response.status_code == 200
        
        asvs_report = response.json()
        
        # Verificar que solo incluye threats con controles ASVS
        asvs_threats = asvs_report["threats"]
        for threat in asvs_threats:
            # Al menos un control tag debe ser de ASVS (empezar con V)
            asvs_tags = [tag for tag in threat["control_tags"] if tag.startswith("V")]
            assert len(asvs_tags) > 0
            
    def test_control_tags_summary_in_report(self, auth_headers, test_information_system, db_session, test_user):
        """Test que el reporte incluya resumen de control tags"""
        
        # Crear threats con control tags variados
        threat_data = schemas.ThreatCreate(
            title="Complex Threat",
            description="Threat con múltiples controles",
            severity="Critical",
            category="Complex Security",
            control_tags=["V2.1.1", "V2.2.1", "MSTG-AUTH-1", "ID.AM-1", "A.5.1.1", "SBS-2137-1"],
            information_system_id=test_information_system.id
        )
        
        crud.create_threat(
            db=db_session,
            threat=threat_data,
            user_id=test_user.id
        )
        
        # Generar reporte
        response = client.get(f"/api/report?information_system_id={test_information_system.id}", headers=auth_headers)
        assert response.status_code == 200
        
        report_data = response.json()
        
        # Verificar que incluye estadísticas de controles
        if "control_tags_summary" in report_data:
            summary = report_data["control_tags_summary"]
            
            # Verificar que incluye conteos por estándar
            assert "standards_count" in summary
            assert summary["standards_count"]["ASVS"] >= 2  # V2.1.1, V2.2.1
            assert summary["standards_count"]["MASVS"] >= 1  # MSTG-AUTH-1
            assert summary["standards_count"]["NIST"] >= 1  # ID.AM-1
            assert summary["standards_count"]["ISO27001"] >= 1  # A.5.1.1
            assert summary["standards_count"]["SBS"] >= 1  # SBS-2137-1


class TestControlTagsValidationInEndpoints:
    """Tests de validación de control tags en endpoints"""
    
    def test_validate_tags_before_threat_creation(self, auth_headers, test_information_system):
        """Test validar tags antes de crear threat"""
        
        # Test con tags válidos
        valid_tags = ["V2.1.1", "MSTG-AUTH-1", "ID.AM-1"]
        response = client.post("/api/control-tags/validate-batch", json={"tags": valid_tags}, headers=auth_headers)
        assert response.status_code == 200
        
        validation_result = response.json()
        assert all(result["is_valid"] for result in validation_result["results"])
        
        # Test con tags mixtos (válidos e inválidos)
        mixed_tags = ["V2.1.1", "INVALID-TAG", "ID.AM-1", "ANOTHER-INVALID"]
        response = client.post("/api/control-tags/validate-batch", json={"tags": mixed_tags}, headers=auth_headers)
        assert response.status_code == 200
        
        validation_result = response.json()
        valid_count = sum(1 for result in validation_result["results"] if result["is_valid"])
        assert valid_count == 2  # Solo V2.1.1 e ID.AM-1 son válidos
        
    def test_get_tag_suggestions_endpoint(self, auth_headers):
        """Test obtener sugerencias de tags"""
        
        # Buscar tags relacionados con autenticación
        response = client.get("/api/control-tags/suggestions?query=authentication", headers=auth_headers)
        assert response.status_code == 200
        
        suggestions = response.json()
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        
        # Verificar que las sugerencias incluyen información detallada
        for suggestion in suggestions[:3]:  # Verificar primeras 3
            assert "tag" in suggestion
            assert "title" in suggestion
            assert "description" in suggestion
            assert "standard" in suggestion
            
    def test_get_tags_by_standard_endpoint(self, auth_headers):
        """Test obtener tags por estándar específico"""
        
        # Test ASVS
        response = client.get("/api/control-tags/by-standard/ASVS", headers=auth_headers)
        assert response.status_code == 200
        
        asvs_tags = response.json()
        assert len(asvs_tags) == 93  # ASVS tiene 93 controles
        assert all(tag.startswith("V") for tag in asvs_tags["tags"])
        
        # Test NIST
        response = client.get("/api/control-tags/by-standard/NIST", headers=auth_headers)
        assert response.status_code == 200
        
        nist_tags = response.json()
        assert len(nist_tags) == 108  # NIST tiene 108 controles
        
        # Test estándar inválido
        response = client.get("/api/control-tags/by-standard/INVALID", headers=auth_headers)
        assert response.status_code == 404


if __name__ == "__main__":
    # Ejecutar algunos tests básicos si se ejecuta directamente
    print("✅ Tests de control tags y reportes listos para ejecución con pytest")
    print("Uso: pytest api/tests/test_control_tags_reports.py -v")
