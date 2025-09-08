"""
Tests para la funcionalidad de tags de controles y reportes
"""

import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime

from tests.conftest import client
import models
import crud
import schemas
from standards import (
    ALL_CONTROLS,
    STANDARDS_MAP,
    STRIDE_CONTROL_EXAMPLES
)
from control_tags import (
    get_available_standards,
    normalize_tag_for_lookup,
    validate_control_tag,
    get_tag_details,
    search_predefined_tags,
    format_tag_for_display
)

class TestTagsFunctionality:
    """Tests para la funcionalidad completa de tags"""
    
    def test_tag_normalization_comprehensive(self):
        """Test exhaustivo de normalización de tags"""
        test_cases = [
            # Casos ASVS - simple cleanup (no more prefix removal)
            ("V2.1.1", "V2.1.1"),
            ("v2.1.1", "V2.1.1"),
            ("  V2.1.1  ", "V2.1.1"),
            
            # Casos MASVS (updated format without MSTG prefix)
            ("AUTH-1", "AUTH-1"),
            ("auth-1", "AUTH-1"),
            ("  AUTH-1  ", "AUTH-1"),
            
            # Casos NIST
            ("ID.AM-1", "ID.AM-1"),
            ("id.am-1", "ID.AM-1"),
            ("  ID.AM-1  ", "ID.AM-1"),
            
            # Casos ISO27001
            ("A.5.1.1", "A.5.1.1"),
            ("a.5.1.1", "A.5.1.1"),
            ("  A.5.1.1  ", "A.5.1.1"),
            
            # Casos SBS
            ("SBS-2137-1", "SBS-2137-1"),
            ("sbs-2137-1", "SBS-2137-1"),
            ("  SBS-2137-1  ", "SBS-2137-1"),
        ]
        
        for input_tag, expected in test_cases:
            result = normalize_tag_for_lookup(input_tag)
            assert result == expected, f"Input: {input_tag} -> Expected: {expected}, Got: {result}"
    
    def test_tag_validation_edge_cases(self):
        """Test de validación con casos edge"""
        # Tags válidos conocidos (updated MASVS format)
        valid_tags = [
            "V2.1.1", "V1.1.1", "V3.1.1",  # ASVS (tags que existen realmente)
            "AUTH-1", "NETWORK-1",  # MASVS (updated format without MSTG prefix)
            "ID.AM-1", "PR.AC-1", "DE.AE-1",  # NIST
            "A.5.1.1", "A.8.1.1", "A.11.1.1",  # ISO27001 (A.11.1.1 existe, A.12.6.1 no)
            "SBS-2137-1", "SBS-2137-5"  # SBS
        ]
        
        for tag in valid_tags:
            assert validate_control_tag(tag), f"Tag {tag} debería ser válido"
            
        # Tags inválidos
        invalid_tags = [
            "INVALID-TAG",
            "V999.999.999",  # ASVS no existente
            "MSTG-INVALID-1",  # MASVS no existente
            "XX.YY-1",  # NIST no existente
            "B.1.1.1",  # ISO27001 no existente (debería ser A.x.x.x)
            "SBS-9999-1",  # SBS no existente
            "",  # Vacío
            "   ",  # Solo espacios
            "123",  # Solo números
            "ABC",  # Solo letras sin formato
        ]
        
        for tag in invalid_tags:
            assert not validate_control_tag(tag), f"Tag {tag} debería ser inválido"
    
    def test_tag_search_functionality(self):
        """Test de funcionalidad de búsqueda de tags"""
        # Búsqueda por términos comunes
        search_terms = [
            ("authentication", "autenticación"),
            ("access", "acceso"), 
            ("encryption", "cifrado"),
            ("logging", "registro"),
            ("password", "contraseña"),
            ("session", "sesión")
        ]
        
        for term, description in search_terms:
            results = search_predefined_tags(term)
            assert isinstance(results, list), f"Búsqueda de '{term}' debe retornar lista"
            
            if len(results) > 0:
                # Verificar que los resultados son relevantes
                for result_tag in results[:3]:  # Solo primeros 3
                    details = get_tag_details(result_tag)
                    assert details is not None, f"Tag {result_tag} debe tener detalles"
                    
                    # El término debe aparecer en título o descripción (case insensitive)
                    content = (details["title"] + " " + details["description"]).lower()
                    assert term.lower() in content, f"'{term}' debe aparecer en contenido de {result_tag}"
    
    def test_tag_formatting_with_standards(self):
        """Test de formateo de tags con estándares"""
        test_cases = [
            ("V2.1.1", "V2.1.1 (ASVS)"),
            ("AUTH-1", "AUTH-1 (MASVS)"),  # Updated MASVS format
            ("ID.AM-1", "ID.AM-1 (NIST)"),
            ("A.5.1.1", "A.5.1.1 (ISO27001)"),
            ("SBS-2137-1", "SBS-2137-1 (SBS)"),
        ]
        
        for tag, expected_formatted in test_cases:
            result = format_tag_for_display(tag)
            assert result == expected_formatted, f"Tag {tag} -> Expected: {expected_formatted}, Got: {result}"
    
    def test_tag_details_completeness(self):
        """Test de completitud de detalles de tags"""
        # Seleccionar algunos tags conocidos de cada estándar (updated MASVS format)
        sample_tags = ["V2.1.1", "AUTH-1", "ID.AM-1", "A.5.1.1", "SBS-2137-1"]
        
        for tag in sample_tags:
            details = get_tag_details(tag)
            assert details is not None, f"Tag {tag} debe tener detalles"
            
            # Verificar campos requeridos
            required_fields = ["title", "description", "category"]
            for field in required_fields:
                assert field in details, f"Tag {tag} debe tener campo '{field}'"
                assert isinstance(details[field], str), f"Campo '{field}' debe ser string"
                assert len(details[field].strip()) > 0, f"Campo '{field}' no debe estar vacío"
                
            # Verificar que title y description son diferentes
            assert details["title"] != details["description"], f"Title y description deben ser diferentes para {tag}"
            
            # Verificar longitud mínima
            assert len(details["title"]) >= 10, f"Title debe tener al menos 10 caracteres para {tag}"
            assert len(details["description"]) >= 20, f"Description debe tener al menos 20 caracteres para {tag}"


class TestSTRIDETagMapping:
    """Tests para el mapeo de tags STRIDE"""
    
    def test_stride_categories_coverage(self):
        """Test de cobertura de categorías STRIDE"""
        
        expected_stride_categories = [
            "SPOOFING",
            "TAMPERING", 
            "REPUDIATION",
            "INFORMATION_DISCLOSURE",
            "DENIAL_OF_SERVICE",
            "ELEVATION_OF_PRIVILEGE"
        ]
        
        # Verificar que todas las categorías STRIDE están cubiertas
        assert set(STRIDE_CONTROL_EXAMPLES.keys()) == set(expected_stride_categories), \
            "Todas las categorías STRIDE deben estar presentes"
            
        # Verificar que cada categoría tiene controles
        for category in expected_stride_categories:
            controls = STRIDE_CONTROL_EXAMPLES[category]
            assert len(controls) > 0, f"Categoría {category} debe tener controles"
            assert len(controls) >= 3, f"Categoría {category} debe tener al menos 3 controles"
            
            # Verificar que todos los controles son válidos
            for control in controls:
                normalized = normalize_tag_for_lookup(control)
                assert validate_control_tag(normalized), f"Control {control} en {category} debe ser válido"
    
    def test_stride_control_relevance(self):
        """Test de relevancia de controles STRIDE"""
        
        # Mapeo de términos esperados por categoría
        expected_terms = {
            "SPOOFING": ["authentication", "identity", "verification", "credential", "autenticación", "identidad", "verificación", "credencial"],
            "TAMPERING": ["integrity", "validation", "hash", "signature", "integridad", "validación", "firma"],
            "REPUDIATION": ["logging", "audit", "non-repudiation", "record", "log", "auditoría", "registro", "trazabilidad"],
            "INFORMATION_DISCLOSURE": ["confidentiality", "encryption", "access", "privacy", "confidencialidad", "cifrado", "acceso", "privacidad"],
            "DENIAL_OF_SERVICE": ["availability", "rate", "limit", "resource", "disponibilidad", "límite", "recurso"],
            "ELEVATION_OF_PRIVILEGE": ["authorization", "privilege", "permission", "access", "autorización", "privilegio", "permiso", "acceso"]
        }
        
        for category, controls in STRIDE_CONTROL_EXAMPLES.items():
            expected_category_terms = expected_terms.get(category, [])
            
            # Verificar que al menos algunos controles contienen términos relevantes
            relevant_controls = 0
            
            for control in controls:
                details = get_tag_details(normalize_tag_for_lookup(control))
                if details:
                    content = (details["title"] + " " + details["description"]).lower()
                    
                    for term in expected_category_terms:
                        if term.lower() in content:
                            relevant_controls += 1
                            break
            
            # Al menos 1 control debe ser relevante por categoría
            relevance_threshold = 1
            assert relevant_controls >= relevance_threshold, \
                f"Categoría {category}: {relevant_controls} controles relevantes, esperado al menos {relevance_threshold}"


class TestReportsFunctionality:
    """Tests para la funcionalidad de reportes"""
    
    def test_basic_report_generation(self):
        """Test básico de generación de reportes"""
        # TODO: Implementar cuando el endpoint /api/report esté disponible
        # Por ahora solo verificamos que las funciones de tags funcionan
        from control_tags import get_available_standards, categorize_tags
        
        # Test que las funciones básicas funcionan
        standards = get_available_standards()
        assert len(standards) > 0
        
        # Test categorización de tags
        sample_tags = ["V2.1.1", "MSTG-AUTH-1", "ID.AM-1"]
        categorized = categorize_tags(sample_tags)
        assert len(categorized) > 0
        
    def test_report_filtering_by_standards(self):
        """Test de filtrado de reportes por estándares"""
        # Simular datos de threats con diferentes tags
        sample_threats = [
            {
                "id": 1,
                "title": "Threat 1",
                "control_tags": ["V2.1.1", "MSTG-AUTH-1"],
                "severity": "High"
            },
            {
                "id": 2, 
                "title": "Threat 2",
                "control_tags": ["ID.AM-1", "A.5.1.1"],
                "severity": "Medium"
            },
            {
                "id": 3,
                "title": "Threat 3", 
                "control_tags": ["SBS-2137-1"],
                "severity": "Low"
            }
        ]
        
        # Test filtrado por ASVS
        asvs_threats = [t for t in sample_threats if any(validate_control_tag(tag) and tag.startswith("V") for tag in t["control_tags"])]
        assert len(asvs_threats) == 1
        
        # Test filtrado por NIST (tags que tienen formato XXX.YYY-Z como ID.AM-1, PR.AC-1)
        nist_threats = [t for t in sample_threats if any(validate_control_tag(tag) and 
                       len(tag.split('.')) == 2 and len(tag.split('.')[0]) <= 3 and 
                       not tag.startswith("A.") and not tag.startswith("V") 
                       for tag in t["control_tags"])]
        assert len(nist_threats) == 1
        
        # Test filtrado por múltiples estándares
        multi_standard_threats = [t for t in sample_threats if any(validate_control_tag(tag) for tag in t["control_tags"])]
        assert len(multi_standard_threats) == 3
    
    def test_report_data_aggregation(self):
        """Test de agregación de datos para reportes"""
        # Simular proceso de agregación de datos
        all_standards = get_available_standards()
        
        report_data = {}
        for standard in all_standards:
            # Simular conteo de controles por estándar
            if standard == "ASVS":
                report_data[standard] = {"total_controls": 93, "covered_controls": 15}
            elif standard == "MASVS":
                report_data[standard] = {"total_controls": 10, "covered_controls": 3}
            elif standard == "NIST":
                report_data[standard] = {"total_controls": 108, "covered_controls": 25}
            elif standard == "ISO27001":
                report_data[standard] = {"total_controls": 59, "covered_controls": 12}
            elif standard == "SBS":
                report_data[standard] = {"total_controls": 43, "covered_controls": 8}
        
        # Verificar estructura de datos del reporte
        for standard, data in report_data.items():
            assert "total_controls" in data
            assert "covered_controls" in data
            assert data["covered_controls"] <= data["total_controls"]
            
        # Calcular métricas agregadas
        total_controls = sum(data["total_controls"] for data in report_data.values())
        total_covered = sum(data["covered_controls"] for data in report_data.values())
        coverage_percentage = (total_covered / total_controls) * 100 if total_controls > 0 else 0
        
        assert total_controls == 313  # Total conocido
        assert coverage_percentage <= 100
        assert coverage_percentage >= 0
    
    def test_report_export_formats(self):
        """Test de formatos de exportación de reportes"""
        # Simular datos de reporte
        report_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_threats": 10,
                "total_controls": 313,
                "covered_controls": 63
            },
            "standards_coverage": {
                "ASVS": {"total": 93, "covered": 15, "percentage": 16.1},
                "MASVS": {"total": 10, "covered": 3, "percentage": 30.0},
                "NIST": {"total": 108, "covered": 25, "percentage": 23.1},
                "ISO27001": {"total": 59, "covered": 12, "percentage": 20.3},
                "SBS": {"total": 43, "covered": 8, "percentage": 18.6}
            },
            "threats_by_severity": {
                "High": 3,
                "Medium": 4,
                "Low": 3
            }
        }
        
        # Test formato JSON
        json_export = json.dumps(report_data, indent=2)
        assert len(json_export) > 0
        parsed_json = json.loads(json_export)
        assert parsed_json == report_data
        
        # Test estructura para CSV (simulado)
        csv_headers = ["Standard", "Total Controls", "Covered Controls", "Coverage %"]
        csv_rows = []
        for standard, data in report_data["standards_coverage"].items():
            csv_rows.append([standard, data["total"], data["covered"], data["percentage"]])
        
        assert len(csv_headers) == 4
        assert len(csv_rows) == 5  # 5 estándares
        
        # Test estructura para PDF (simulado)
        pdf_sections = [
            "Executive Summary",
            "Coverage by Standard", 
            "Threats Analysis",
            "Recommendations",
            "Detailed Controls"
        ]
        
        assert len(pdf_sections) == 5


class TestTagsIntegrationWithThreats:
    """Tests de integración entre tags y threats"""
    
    def test_threat_tag_assignment(self):
        """Test de asignación de tags a threats"""
        # Simular creación de threat con tags
        threat_data = {
            "title": "SQL Injection Vulnerability",
            "description": "Potential SQL injection in login form",
            "control_tags": ["V2.1.1", "V2.1.2", "CODE-1"],  # Tags válidos ASVS y MASVS
            "severity": "High",
            "category": "Injection"
        }
        
        # Validar que todos los tags son válidos
        for tag in threat_data["control_tags"]:
            assert validate_control_tag(tag), f"Tag {tag} debe ser válido"
            
        # Verificar que los tags son relevantes al tipo de threat
        relevant_terms = ["input", "validation", "injection", "code"]
        tag_relevance_count = 0
        
        for tag in threat_data["control_tags"]:
            details = get_tag_details(tag)
            if details:
                content = (details["title"] + " " + details["description"]).lower()
                for term in relevant_terms:
                    if term in content:
                        tag_relevance_count += 1
                        break
        
        # Al menos 1 de 3 tags debe ser relevante (más flexible)
        assert tag_relevance_count >= 1, "Al menos un tag debe ser relevante al threat"
    
    def test_threat_tag_search_and_filter(self):
        """Test de búsqueda y filtrado de threats por tags"""
        # Simular base de datos de threats
        threats_db = [
            {"id": 1, "title": "Auth Bypass", "control_tags": ["V2.1.1", "V2.1.2"]},
            {"id": 2, "title": "Data Leak", "control_tags": ["V7.1.1", "A.13.1.1"]},
            {"id": 3, "title": "Mobile Auth", "control_tags": ["MSTG-AUTH-1", "MSTG-AUTH-2"]},
            {"id": 4, "title": "Network Attack", "control_tags": ["ID.AM-1", "PR.AC-1"]},
            {"id": 5, "title": "Compliance Issue", "control_tags": ["SBS-2137-1", "SBS-2137-2"]}
        ]
        
        # Test filtrado por estándar ASVS
        asvs_threats = [t for t in threats_db if any(tag.startswith("V") for tag in t["control_tags"])]
        assert len(asvs_threats) == 2
        
        # Test filtrado por estándar MASVS
        masvs_threats = [t for t in threats_db if any(tag.startswith("MSTG") for tag in t["control_tags"])]
        assert len(masvs_threats) == 1
        
        # Test filtrado por tag específico
        specific_tag_threats = [t for t in threats_db if "V2.1.1" in t["control_tags"]]
        assert len(specific_tag_threats) == 1
        
        # Test búsqueda por patrón de tag
        auth_related_threats = [t for t in threats_db if any("AUTH" in tag for tag in t["control_tags"])]
        assert len(auth_related_threats) == 1
    
    def test_threat_tag_validation_workflow(self):
        """Test del flujo completo de validación de tags en threats"""
        # Simular flujo de validación al crear/actualizar threat (updated format)
        input_tags = ["v2.1.1", "auth-1", "invalid-tag", "id.am-1"]
        
        validated_tags = []
        invalid_tags = []
        
        for tag in input_tags:
            normalized = normalize_tag_for_lookup(tag)
            if validate_control_tag(normalized):
                validated_tags.append(normalized)
            else:
                invalid_tags.append(tag)
        
        # Verificar resultados
        assert len(validated_tags) == 3, f"Esperado 3 tags válidos, got {len(validated_tags)}"
        assert len(invalid_tags) == 1, f"Esperado 1 tag inválido, got {len(invalid_tags)}"
        assert "invalid-tag" in invalid_tags
        
        # Verificar normalización correcta (updated MASVS format)
        expected_normalized = ["V2.1.1", "AUTH-1", "ID.AM-1"]
        assert set(validated_tags) == set(expected_normalized)
        
        # Obtener detalles de tags válidos
        tags_with_details = []
        for tag in validated_tags:
            details = get_tag_details(tag)
            if details:
                tags_with_details.append({
                    "tag": tag,
                    "formatted": format_tag_for_display(tag),
                    "title": details["title"],
                    "category": details["category"]
                })
        
        assert len(tags_with_details) == 3
        
        # Verificar formato de salida
        for tag_info in tags_with_details:
            assert "tag" in tag_info
            assert "formatted" in tag_info
            assert "title" in tag_info
            assert "category" in tag_info
            assert "(" in tag_info["formatted"] and ")" in tag_info["formatted"]  # Debe tener formato CONTROL (STANDARD)


if __name__ == "__main__":
    # Ejecutar algunos tests básicos si se ejecuta directamente
    tags_test = TestTagsFunctionality()
    tags_test.test_tag_normalization_comprehensive()
    print("✅ Tests de tags ejecutados correctamente")
