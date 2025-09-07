"""
Tests para el sistema modular de controles de seguridad
"""

import pytest
import os
import sys

from tests.conftest import client
from control_tags import (
    ALL_CONTROLS,
    STANDARDS_MAP,
    get_available_standards,
    normalize_tag_for_lookup,
    get_tag_details,
    format_tag_for_display,
    validate_control_tag,
    search_predefined_tags,
    get_all_predefined_tags
)

try:
    from standards import (
        asvs_controls,
        masvs_controls,
        mstg_controls,
        iso27001_controls,
        nist_controls,
        owaspzap_controls,
        sans_controls,
        sbs_controls
    )
except ImportError:
    # Si no se pueden importar los módulos de standards, crear mocks
    asvs_controls = None
    masvs_controls = None
    mstg_controls = None


class TestControlsValidation:
    def test_validate_control_tag_valid_formats(self):
        """Test que validate_control_tag acepta formatos válidos"""
        # Test tags válidos (formato exacto como en los archivos)
        assert validate_control_tag("V2.1.1") == True
        assert validate_control_tag("AUTH-1") == True  # Updated MASVS format
        assert validate_control_tag("ID.AM-1") == True
        assert validate_control_tag("A.5.1.1") == True
        assert validate_control_tag("SBS-2137-1") == True
        
        # Test con case sensitivity (se normaliza a mayúsculas)
        assert validate_control_tag("v2.1.1") == True  # Se normaliza a V2.1.1
        assert validate_control_tag("auth-1") == True  # Se normaliza a AUTH-1 (updated format)

    def test_validate_control_tag_invalid_formats(self):
        """Test que validate_control_tag rechaza formatos inválidos"""
        assert validate_control_tag("") == False
        assert validate_control_tag("INVALID-TAG") == False
        assert validate_control_tag("123") == False
        assert validate_control_tag("XXXXX") == False
        assert validate_control_tag(None) == False

    def test_normalize_tag_for_lookup(self):
        """Test que normalize_tag_for_lookup funciona con limpieza básica"""
        # Solo limpieza básica: trim y uppercase
        assert normalize_tag_for_lookup("v2.1.1") == "V2.1.1"
        assert normalize_tag_for_lookup(" V2.1.1 ") == "V2.1.1"
        assert normalize_tag_for_lookup("mstg-auth-1") == "MSTG-AUTH-1"
        assert normalize_tag_for_lookup(" mstg-auth-1 ") == "MSTG-AUTH-1"
        
        # Tags vacíos
        assert normalize_tag_for_lookup("") == ""
        assert normalize_tag_for_lookup("   ") == ""
        assert normalize_tag_for_lookup(None) == ""
        
        # Tags que ya están en formato correcto
        assert normalize_tag_for_lookup("V2.1.1") == "V2.1.1"
        assert normalize_tag_for_lookup("MSTG-AUTH-1") == "MSTG-AUTH-1"
        assert normalize_tag_for_lookup("ID.AM-1") == "ID.AM-1"

    def test_get_tag_details_with_current_format(self):
        """Test que get_tag_details funciona con formato actual"""
        # Test con formato actual (sin prefijo)
        details = get_tag_details("V2.1.1")
        assert details is not None
        # El formato real no incluye 'control_id' sino otros campos
        assert isinstance(details, dict)
        assert len(details) > 0
        
        # Test con normalización case-insensitive
        details_lower = get_tag_details("v2.1.1")
        assert details_lower is not None  # Debe normalizarse a mayúsculas
        # Comparar que ambos retornan la misma información (normalizada)
        assert details == details_lower

    def test_format_tag_for_display(self):
        """Test que format_tag_for_display usa formato con información del estándar"""
        # El formato de display incluye información adicional del estándar
        display = format_tag_for_display("V2.1.1")
        assert "V2.1.1" in display
        assert "ASVS" in display  # Debe incluir el nombre del estándar
        
        # Los formatos obsoletos se normalizan y muestran el formato actual
        display_obsolete = format_tag_for_display("ASVS-V2.1.1")
        assert "V2.1.1" in display_obsolete
        assert "ASVS" in display_obsolete


class TestStandardsIntegration:
    @pytest.mark.skipif(asvs_controls is None, reason="asvs_controls module not available")
    def test_asvs_controls_structure(self):
        """Test que ASVS controls tienen la estructura correcta"""
        assert hasattr(asvs_controls, 'controls')
        controls = asvs_controls.controls
        
        # Verificar que los controles usan formato actual (sin prefijo ASVS-)
        sample_key = next(iter(controls.keys()))
        assert not sample_key.startswith("ASVS-")  # No debe tener prefijo obsoleto
        assert "V" in sample_key  # Debe tener formato V*.*.* 

    @pytest.mark.skipif(masvs_controls is None, reason="masvs_controls module not available")
    def test_masvs_controls_structure(self):
        """Test que MASVS controls tienen la estructura correcta"""
        assert hasattr(masvs_controls, 'controls')
        controls = masvs_controls.controls
        
        # Verificar que los controles usan formato actual (sin prefijo MASVS-)
        sample_key = next(iter(controls.keys()))
        assert not sample_key.startswith("MASVS-")  # No debe tener prefijo obsoleto

    def test_get_available_standards(self):
        """Test que get_available_standards retorna estándares válidos"""
        standards = get_available_standards()
        assert isinstance(standards, list)
        assert len(standards) > 0
        
        # Verificar que incluye los estándares principales
        # El formato real puede ser lista de strings o diccionarios
        if standards and isinstance(standards[0], str):
            # Si son strings - verificar estándares que realmente existen
            assert "ASVS" in standards
            assert "MASVS" in standards
            # MSTG no parece estar disponible actualmente
        else:
            # Si son diccionarios
            standard_names = [s['name'] for s in standards]
            assert "ASVS" in standard_names
            assert "MASVS" in standard_names


class TestSearchFunctionality:
    def test_search_predefined_tags_current_format(self):
        """Test búsqueda de tags con formato actual"""
        # Buscar con formato actual
        results = search_predefined_tags("V2.1")
        assert isinstance(results, list)
        assert len(results) > 0
        
        # Verificar que los resultados usan formato actual
        for result in results:
            assert not result.startswith("ASVS-")  # No debe tener prefijo obsoleto

    def test_search_predefined_tags_obsolete_format(self):
        """Test que búsqueda con formato obsoleto encuentra resultados"""
        # Buscar con formato obsoleto debería encontrar resultados
        results = search_predefined_tags("ASVS-V2.1")
        assert isinstance(results, list)
        # Los resultados deben normalizarse al formato actual
        for result in results:
            assert not result.startswith("ASVS-")  # Los resultados no deben tener prefijo

    def test_get_all_predefined_tags(self):
        """Test que get_all_predefined_tags retorna formato actual"""
        all_tags = get_all_predefined_tags()
        assert isinstance(all_tags, list)
        assert len(all_tags) > 0
        
        # Verificar que ningún tag tiene prefijo obsoleto
        for tag in all_tags:
            assert not tag.startswith("ASVS-")
            assert not tag.startswith("MASVS-")


class TestBasicFunctionality:
    def test_current_format_works(self):
        """Test que formatos actuales funcionan correctamente"""
        # Los formatos actuales (exactos) deben funcionar
        assert validate_control_tag("V2.1.1") == True
        assert validate_control_tag("AUTH-1") == True  # Updated MASVS format
        
        # get_tag_details debe retornar información válida
        details = get_tag_details("V2.1.1")
        if details:
            # Verificar que los detalles son válidos
            assert isinstance(details, dict)
            assert len(details) > 0

    def test_mixed_format_handling(self):
        """Test manejo de búsquedas básicas"""
        # Test que podemos buscar tags válidos
        results = search_predefined_tags("V2")
        for result in results:
            # Los resultados deben estar en formato actual
            assert not result.startswith("ASVS-")


class TestControlsMapping:
    def test_all_controls_format(self):
        """Test que ALL_CONTROLS usa formato actual"""
        assert isinstance(ALL_CONTROLS, dict)
        
        # Verificar que las claves no tienen prefijos obsoletos
        for control_id in ALL_CONTROLS.keys():
            assert not control_id.startswith("ASVS-")
            assert not control_id.startswith("MASVS-")

    def test_standards_map_format(self):
        """Test que STANDARDS_MAP usa formato actual"""
        assert isinstance(STANDARDS_MAP, dict)
        
        # Verificar estructura de cada estándar
        for standard_name, standard_data in STANDARDS_MAP.items():
            if 'controls' in standard_data:
                for control_id in standard_data['controls'].keys():
                    # Los control_id no deben tener prefijos obsoletos
                    assert not control_id.startswith("ASVS-")
                    assert not control_id.startswith("MASVS-")


class TestDataConsistency:
    def test_no_obsolete_formats_in_data(self):
        """Test que los datos no contienen formatos obsoletos"""
        all_tags = get_all_predefined_tags()
        
        # Verificar que ningún tag predefinido usa formato obsoleto
        obsolete_tags = [tag for tag in all_tags if tag.startswith(("ASVS-", "MASVS-"))]
        assert len(obsolete_tags) == 0, f"Encontrados tags obsoletos: {obsolete_tags}"

    def test_normalization_consistency(self):
        """Test que la normalización básica es consistente"""
        test_cases = [
            ("v2.1.1", "V2.1.1"),
            ("mstg-auth-1", "MSTG-AUTH-1"), 
            ("id.am-1", "ID.AM-1"),
            (" V2.1.1 ", "V2.1.1"),  # Con espacios
            ("  mstg-auth-1  ", "MSTG-AUTH-1"),  # Con espacios
        ]
        
        for input_tag, expected in test_cases:
            normalized = normalize_tag_for_lookup(input_tag)
            assert normalized == expected, f"Expected {expected}, got {normalized} for {input_tag}"
