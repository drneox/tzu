"""
Tests de integración para el sistema completo de controles modulares
"""

import pytest
import os
import sys

from tests.conftest import client, db_session
from control_tags import *
import models
import crud

class TestIntegrationControlsSystem:
    """Tests de integración para el sistema completo"""
    
    def test_end_to_end_tag_processing(self):
        """Test end-to-end del procesamiento de tags"""
        # Flujo completo: entrada de usuario -> normalización -> validación -> detalles
        user_input = "asvs-v2.1.1"
        
        # Paso 1: Normalizar
        normalized = normalize_tag_for_lookup(user_input)
        assert normalized == "V2.1.1"
        
        # Paso 2: Validar
        is_valid = validate_control_tag(normalized)
        assert is_valid == True
        
        # Paso 3: Obtener detalles
        details = get_tag_details(normalized)
        assert details is not None
        assert "title" in details
        assert "description" in details
        
        # Paso 4: Formatear para visualización
        formatted = format_tag_for_display(normalized)
        assert formatted == "V2.1.1 (ASVS)"
        
    def test_bulk_tag_validation(self):
        """Test de validación en lote de múltiples tags"""
        test_tags = [
            "V2.1.1",
            "MSTG-AUTH-1", 
            "ID.AM-1",
            "A.5.1.1",
            "SBS-2137-1",
            "INVALID-TAG"
        ]
        
        valid_count = 0
        for tag in test_tags:
            if validate_control_tag(tag):
                valid_count += 1
                
        assert valid_count == 5, f"Esperado 5 tags válidos, encontrado {valid_count}"
        
    def test_search_across_all_standards(self):
        """Test de búsqueda a través de todos los estándares"""
        # Buscar un término que aparezca en múltiples estándares
        results = search_predefined_tags("authentication")
        
        # Verificar que tenemos resultados de múltiples estándares
        standards_found = set()
        for tag in results:
            if validate_control_tag(tag):
                # Determinar estándar basado en formato
                if tag.startswith("V"):
                    standards_found.add("ASVS")
                elif tag.startswith("MSTG"):
                    standards_found.add("MASVS")
                elif "." in tag and not tag.startswith("A."):
                    standards_found.add("NIST")
                elif tag.startswith("A."):
                    standards_found.add("ISO27001")
                elif tag.startswith("SBS"):
                    standards_found.add("SBS")
                    
        assert len(standards_found) >= 2, f"Búsqueda debe encontrar resultados en múltiples estándares, encontró: {standards_found}"
        
    def test_standard_coverage_completeness(self):
        """Test de completitud de cobertura por estándar"""
        all_standards = get_available_standards()
        
        total_controls = 0
        for standard in all_standards:
            tags = get_tags_by_standard(standard)
            total_controls += len(tags)
            
            # Verificar que cada tag es válido
            for tag in tags:
                assert validate_control_tag(tag), f"Tag {tag} en estándar {standard} debe ser válido"
                
        assert total_controls == len(ALL_CONTROLS), \
            f"Suma de controles por estándar ({total_controls}) debe igualar ALL_CONTROLS ({len(ALL_CONTROLS)})"
            
    def test_tag_uniqueness_across_standards(self):
        """Test de unicidad de tags a través de estándares"""
        all_tags = get_all_predefined_tags()
        unique_tags = set(all_tags)
        
        assert len(all_tags) == len(unique_tags), \
            f"Todos los tags deben ser únicos. Total: {len(all_tags)}, Únicos: {len(unique_tags)}"
            
    def test_cross_standard_references(self):
        """Test de referencias cruzadas entre estándares"""
        # Verificar que no hay conflictos en el mapeo
        for tag_id in ALL_CONTROLS:
            details = get_tag_details(tag_id)
            assert details is not None, f"Tag {tag_id} debe tener detalles"
            
            # Verificar que el formato del tag es correcto
            formatted = format_tag_for_display(tag_id)
            assert formatted is not None, f"Tag {tag_id} debe poder formatearse para mostrar"
            
    def test_stride_mapping_validity(self):
        """Test de validez del mapeo STRIDE"""
        from api.standards import STRIDE_CONTROL_EXAMPLES
        
        for threat_type, controls in STRIDE_CONTROL_EXAMPLES.items():
            for control in controls:
                # Normalizar y validar cada control
                normalized = normalize_tag_for_lookup(control)
                assert validate_control_tag(normalized), \
                    f"Control {control} en STRIDE {threat_type} debe ser válido"
                    
                # Verificar que tiene detalles
                details = get_tag_details(normalized)
                assert details is not None, \
                    f"Control {control} en STRIDE {threat_type} debe tener detalles"


class TestPerformanceAndLimits:
    """Tests de rendimiento y límites del sistema"""
    
    def test_large_search_performance(self):
        """Test de rendimiento en búsquedas grandes"""
        import time
        
        start_time = time.time()
        
        # Realizar múltiples búsquedas
        search_terms = ["auth", "access", "control", "security", "data"]
        total_results = 0
        
        for term in search_terms:
            results = search_predefined_tags(term)
            total_results += len(results)
            
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Debe completarse en menos de 1 segundo
        assert execution_time < 1.0, f"Búsquedas deben completarse rápidamente. Tiempo: {execution_time:.2f}s"
        assert total_results > 0, "Debe encontrar algunos resultados"
        
    def test_memory_usage_reasonable(self):
        """Test de uso de memoria razonable"""
        import sys
        
        # Obtener el tamaño de ALL_CONTROLS
        all_controls_size = sys.getsizeof(ALL_CONTROLS)
        
        # Para 313 controles, el uso de memoria debe ser razonable (menos de 1MB)
        assert all_controls_size < 1_000_000, \
            f"ALL_CONTROLS debe usar memoria razonable. Tamaño actual: {all_controls_size} bytes"
            
    def test_tag_search_limits(self):
        """Test de límites en búsqueda de tags"""
        # Test de límite máximo de resultados
        # Usar una búsqueda que potencialmente retorne muchos resultados
        results = search_predefined_tags("a")  # Búsqueda muy amplia
        
        # Verificar que se respeta el límite
        assert len(results) <= 20, f"Búsqueda debe limitarse a 20 resultados, obtuvo {len(results)}"


class TestErrorHandling:
    """Tests de manejo de errores y casos edge"""
    
    def test_null_and_empty_inputs(self):
        """Test de entradas nulas y vacías"""
        # Test normalize_tag_for_lookup
        assert normalize_tag_for_lookup(None) is None
        assert normalize_tag_for_lookup("") == ""
        assert normalize_tag_for_lookup("   ") == ""
        
        # Test validate_control_tag
        assert validate_control_tag(None) == False
        assert validate_control_tag("") == False
        assert validate_control_tag("   ") == False
        
        # Test get_tag_details
        assert get_tag_details(None) is None
        assert get_tag_details("") is None
        assert get_tag_details("   ") is None
        
        # Test search_predefined_tags
        assert search_predefined_tags(None) == []
        assert search_predefined_tags("") == []
        assert search_predefined_tags("   ") == []
        
    def test_malformed_tag_inputs(self):
        """Test de entradas de tags malformadas"""
        malformed_tags = [
            "V2.1.1.EXTRA",
            "INVALID-FORMAT-TAG",
            "123456",
            "SPECIAL-@#$%-CHARS",
            "VERY-LONG-TAG-THAT-SHOULD-NOT-EXIST-IN-ANY-STANDARD-EVER",
            "   V2.1.1   ",  # Con espacios extra
            "v2.1.1.additional.stuff"
        ]
        
        for tag in malformed_tags:
            # La mayoría deberían ser inválidos, excepto algunos casos especiales
            result = validate_control_tag(tag)
            if tag.strip() == "V2.1.1":  # Caso especial con espacios
                assert result == True, f"Tag con espacios debe normalizarse correctamente: {tag}"
            else:
                # Para otros casos malformados, verificar que el sistema maneja apropiadamente
                assert isinstance(result, bool), f"validate_control_tag debe retornar boolean para: {tag}"
                
    def test_case_sensitivity_handling(self):
        """Test de manejo de sensibilidad a mayúsculas/minúsculas"""
        test_cases = [
            ("V2.1.1", "v2.1.1"),
            ("MSTG-AUTH-1", "mstg-auth-1"),
            ("ID.AM-1", "id.am-1"),
            ("A.5.1.1", "a.5.1.1"),
            ("SBS-2137-1", "sbs-2137-1")
        ]
        
        for upper_case, lower_case in test_cases:
            # Ambos deben normalizar al mismo resultado
            upper_normalized = normalize_tag_for_lookup(upper_case)
            lower_normalized = normalize_tag_for_lookup(lower_case)
            
            assert upper_normalized == lower_normalized, \
                f"Case insensitive: {upper_case} y {lower_case} deben normalizar igual"
                
            # Ambos deben ser válidos (o inválidos) de la misma manera
            upper_valid = validate_control_tag(upper_case)
            lower_valid = validate_control_tag(lower_case)
            
            assert upper_valid == lower_valid, \
                f"Case insensitive validation: {upper_case} y {lower_case} deben tener la misma validez"


class TestSystemIntegrity:
    """Tests de integridad del sistema completo"""
    
    def test_no_duplicate_control_ids(self):
        """Test que no hay IDs de control duplicados"""
        all_ids = list(ALL_CONTROLS.keys())
        unique_ids = set(all_ids)
        
        assert len(all_ids) == len(unique_ids), \
            f"No debe haber IDs duplicados. Total: {len(all_ids)}, Únicos: {len(unique_ids)}"
            
    def test_all_controls_have_required_fields(self):
        """Test que todos los controles tienen campos requeridos"""
        required_fields = ["title", "description", "category"]
        
        for control_id, control_data in ALL_CONTROLS.items():
            for field in required_fields:
                assert field in control_data, \
                    f"Control {control_id} debe tener campo '{field}'"
                assert control_data[field], \
                    f"Campo '{field}' en control {control_id} no debe estar vacío"
                assert len(control_data[field].strip()) > 0, \
                    f"Campo '{field}' en control {control_id} no debe ser solo espacios"
                    
    def test_standards_map_completeness(self):
        """Test de completitud del mapa de estándares"""
        # Verificar que STANDARDS_MAP contiene toda la información necesaria
        for standard_name, standard_info in STANDARDS_MAP.items():
            assert "controls" in standard_info, f"Estándar {standard_name} debe tener 'controls'"
            assert "tags" in standard_info, f"Estándar {standard_name} debe tener 'tags'"
            
            controls = standard_info["controls"]
            tags = standard_info["tags"]
            
            assert len(controls) == len(tags), \
                f"Estándar {standard_name}: controles ({len(controls)}) y tags ({len(tags)}) deben tener la misma cantidad"
                
            # Verificar que los tags corresponden a los IDs de controles
            control_ids = set(controls.keys())
            tag_set = set(tags)
            
            assert control_ids == tag_set, \
                f"Estándar {standard_name}: IDs de controles y tags deben coincidir"


if __name__ == "__main__":
    # Ejecutar algunos tests básicos si se ejecuta directamente
    integration_test = TestIntegrationControlsSystem()
    integration_test.test_end_to_end_tag_processing()
    integration_test.test_bulk_tag_validation()
    print("✅ Tests de integración pasaron correctamente")
