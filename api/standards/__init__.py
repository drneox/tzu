"""
Standards module - Módulo de estándares de seguridad automático
================================================================
Este módulo carga dinámicamente todos los estándares de seguridad desde archivos individuales.
Para agregar un nuevo estándar, simplemente crea un archivo .py con la variable {NOMBRE}_CONTROLS.

Convención:
- Archivo: nombre_estandar.py  
- Variable: NOMBRE_ESTANDAR_CONTROLS (en mayúsculas)
- Ejemplo: asvs.py -> ASVS_CONTROLS, iso27001.py -> ISO27001_CONTROLS
"""

import os
import re
import importlib
from pathlib import Path

# Obtener la ruta del directorio actual
current_dir = Path(__file__).parent

# Diccionarios que se llenarán automáticamente
ALL_CONTROLS = {}
STANDARDS_MAP = {}
TAGS_MAP = {}

def _load_standards_automatically():
    """
    Carga automáticamente todos los estándares desde archivos .py en la carpeta standards/
    """
    global ALL_CONTROLS, STANDARDS_MAP, TAGS_MAP
    
    # Buscar todos los archivos .py excepto __init__.py
    standard_files = [f for f in os.listdir(current_dir) 
                     if f.endswith('.py') and not f.startswith('__')]
    
    loaded_standards = []
    
    for file_name in standard_files:
        try:
            # Extraer el nombre del módulo (sin .py)
            module_name = file_name[:-3]
            
            # Convertir nombre de archivo a nombre de variable
            # ej: iso27001.py -> ISO27001, asvs.py -> ASVS
            standard_name = module_name.upper()
            controls_var_name = f"{standard_name}_CONTROLS"
            
            # Importar el módulo dinámicamente
            module = importlib.import_module(f'.{module_name}', package=__name__)
            
            # Verificar si existe la variable {NOMBRE}_CONTROLS
            if hasattr(module, controls_var_name):
                controls = getattr(module, controls_var_name)
                
                # Agregar al mapeo de estándares
                STANDARDS_MAP[standard_name] = controls
                
                # Crear lista de tags
                TAGS_MAP[f"{standard_name}_TAGS"] = list(controls.keys())
                
                # Agregar a ALL_CONTROLS
                ALL_CONTROLS.update(controls)
                
                loaded_standards.append(f"{standard_name} ({len(controls)} controles)")
                
                print(f"✅ Cargado: {standard_name} con {len(controls)} controles")
            else:
                print(f"⚠️  Advertencia: {file_name} no tiene variable {controls_var_name}")
                
        except Exception as e:
            print(f"❌ Error cargando {file_name}: {e}")
    
    print(f"\n🎯 Sistema automático cargado: {len(ALL_CONTROLS)} controles de {len(loaded_standards)} estándares")
    return loaded_standards

# Cargar todos los estándares automáticamente
_loaded_standards = _load_standards_automatically()

# Crear variables dinámicas para compatibilidad hacia atrás
for standard_name in STANDARDS_MAP.keys():
    # Crear variables como ASVS_CONTROLS, MASVS_CONTROLS, etc.
    globals()[f"{standard_name}_CONTROLS"] = STANDARDS_MAP[standard_name]
    globals()[f"{standard_name}_TAGS"] = list(STANDARDS_MAP[standard_name].keys())

# STRIDE Control Examples (se mantiene estático por ahora)
STRIDE_CONTROL_EXAMPLES = {
    "SPOOFING": ["V2.1.1", "V2.2.1", "AUTH-1", "A.9.1.1", "PR.AC-1"],
    "TAMPERING": ["V5.1.1", "V6.2.1", "CODE-1", "A.8.2.1", "PR.DS-6"],
    "REPUDIATION": ["V7.1.1", "V7.2.1", "A.9.4.2", "PR.PT-1"],
    "INFORMATION_DISCLOSURE": ["V8.1.1", "V9.1.1", "STORAGE-1", "A.9.4.1", "PR.DS-1"],
    "DENIAL_OF_SERVICE": ["V11.1.4", "V12.1.1", "A.11.2.4", "PR.DS-4"],
    "ELEVATION_OF_PRIVILEGE": ["V4.1.1", "V4.2.1", "A.9.2.3", "PR.AC-4"]
}

# =====================================================
# UTILITY FUNCTIONS FOR TAG PROCESSING
# =====================================================

def normalize_tag_for_lookup(tag: str) -> str:
    """
    Función simplificada para normalización de tags.
    Los archivos de estándares ya tienen los IDs exactos como llaves.
    
    Args:
        tag: Tag a normalizar
    
    Returns:
        str: Tag limpio (solo trim y uppercase)
    """
    if not tag or tag is None:
        return ""
    
    # Solo limpieza básica - los archivos ya tienen los IDs exactos
    return tag.strip().upper()

def get_tag_details(tag: str) -> dict:
    """
    Obtiene los detalles de un tag específico.
    
    Args:
        tag: El identificador del tag
    
    Returns:
        dict: Diccionario con title, description, category y standard, o None si no se encuentra
    """
    normalized_tag = normalize_tag_for_lookup(tag)
    control_details = ALL_CONTROLS.get(normalized_tag)
    
    if control_details is None:
        return None
    
    # Buscar en qué estándar está este tag
    standard = None
    for standard_name, controls in STANDARDS_MAP.items():
        if normalized_tag in controls:
            standard = standard_name
            break
    
    # Crear una copia del diccionario y agregar el campo standard
    result = control_details.copy()
    result["standard"] = standard
    return result

def format_tag_for_display(tag: str) -> str:
    """
    Formats tag for display with standard name in parentheses.
    
    Args:
        tag: The tag identifier
    
    Returns:
        str: Tag formatted with standard name in parentheses (e.g., "V2.1.1 (ASVS)")
    """
    normalized_tag = normalize_tag_for_lookup(tag)
    
    # Find which standard this tag belongs to
    for standard_name, controls in STANDARDS_MAP.items():
        if normalized_tag in controls:
            return f"{tag} ({standard_name})"
    
    # If not found in any standard, return tag as-is
    return tag

def validate_control_tag(tag: str) -> bool:
    """
    Valida si un tag corresponde a un control existente.
    
    Args:
        tag: Tag a validar
    
    Returns:
        bool: True si el tag existe, False en caso contrario
    """
    normalized_tag = normalize_tag_for_lookup(tag)
    return normalized_tag in ALL_CONTROLS

def get_suggested_tags_for_stride(stride_category: str) -> list:
    """
    Obtiene tags sugeridos para una categoría STRIDE específica.
    
    Args:
        stride_category: Categoría STRIDE (ej: 'SPOOFING', 'TAMPERING')
    
    Returns:
        list: Lista de tags sugeridos
    """
    return STRIDE_CONTROL_EXAMPLES.get(stride_category.upper(), [])

def categorize_tags(tags: list) -> dict:
    """
    Categoriza una lista de tags por estándar.
    
    Args:
        tags: Lista de tags
    
    Returns:
        dict: Diccionario con tags agrupados por estándar
    """
    categorized = {standard: [] for standard in STANDARDS_MAP.keys()}
    categorized['UNKNOWN'] = []
    
    for tag in tags:
        found = False
        
        for standard_name, controls in STANDARDS_MAP.items():
            if tag in controls:
                categorized[standard_name].append(tag)
                found = True
                break
        
        if not found:
            categorized['UNKNOWN'].append(tag)
    
    # Remover categorías vacías
    return {k: v for k, v in categorized.items() if v}

def search_predefined_tags(query: str) -> list:
    """
    Buscar tags predefinidos que coincidan con la consulta.
    
    Args:
        query: Término de búsqueda
    
    Returns:
        list: Lista de tags que coinciden con la búsqueda
    """
    if not query or len(query) < 2:
        return []
    
    # Si el query ya está formateado (contiene paréntesis), extraer el tag base
    import re
    formatted_pattern = r'^(.+?)\s*\([^)]+\)$'
    match = re.match(formatted_pattern, query.strip())
    if match:
        # Es un tag ya formateado como "V2.1.1 (ASVS)", extraer la parte base
        base_query = match.group(1).strip()
        query_lower = base_query.lower()
    else:
        query_lower = query.lower()
    
    all_tags = list(ALL_CONTROLS.keys())
    
    # Buscar coincidencias exactas primero, luego parciales
    exact_matches = [tag for tag in all_tags if query_lower == tag.lower()]
    partial_matches = [tag for tag in all_tags if query_lower in tag.lower() and tag not in exact_matches]
    
    # También buscar en títulos y descripciones
    content_matches = []
    for tag, info in ALL_CONTROLS.items():
        if tag not in exact_matches and tag not in partial_matches:
            if (query_lower in info.get("title", "").lower() or 
                query_lower in info.get("description", "").lower()):
                content_matches.append(tag)
    
    # Combinar y limitar resultados
    results = exact_matches + partial_matches + content_matches
    return results[:20]

def get_all_predefined_tags() -> list:
    """
    Obtener todos los tags predefinidos.
    
    Returns:
        list: Lista de todos los tags disponibles
    """
    return list(ALL_CONTROLS.keys())

def get_tags_by_standard(standard: str) -> list:
    """
    Obtener tags de un estándar específico.
    
    Args:
        standard: Nombre del estándar (ej: 'ASVS', 'NIST')
    
    Returns:
        list: Lista de tags del estándar especificado
    """
    standard_upper = standard.upper()
    if standard_upper in STANDARDS_MAP:
        return list(STANDARDS_MAP[standard_upper].keys())
    return []

def get_available_standards() -> list:
    """
    Obtiene lista de estándares disponibles cargados automáticamente.
    
    Returns:
        list: Lista de nombres de estándares disponibles
    """
    return list(STANDARDS_MAP.keys())

def get_standard_info(standard_name: str = None) -> dict:
    """
    Obtiene información detallada de un estándar específico o todos los estándares.
    
    Args:
        standard_name: Nombre del estándar (opcional)
    
    Returns:
        dict: Información detallada del estándar o todos los estándares
    """
    if standard_name:
        standard_upper = standard_name.upper()
        if standard_upper not in STANDARDS_MAP:
            return None
        
        controls = STANDARDS_MAP[standard_upper]
        categories = list(set(control.get("category", "Unknown") for control in controls.values()))
        
        return {
            "name": standard_upper,
            "controls_count": len(controls),
            "categories": sorted(categories),
            "sample_controls": list(controls.keys())[:5]
        }
    else:
        # Retornar información de todos los estándares
        return {
            standard: {
                "name": standard,
                "controls_count": len(controls),
                "categories": sorted(list(set(control.get("category", "Unknown") for control in controls.values()))),
                "sample_controls": list(controls.keys())[:3]
            }
            for standard, controls in STANDARDS_MAP.items()
        }

# =====================================================
# EXPORTS FOR COMPATIBILITY
# =====================================================

__all__ = [
    # Diccionarios principales
    'ALL_CONTROLS', 'STANDARDS_MAP', 'STRIDE_CONTROL_EXAMPLES',
    
    # Variables dinámicas por estándar (se crean automáticamente)
    *[f"{std}_CONTROLS" for std in STANDARDS_MAP.keys()],
    *[f"{std}_TAGS" for std in STANDARDS_MAP.keys()],
    
    # Funciones utilitarias
    'normalize_tag_for_lookup', 'get_tag_details', 'format_tag_for_display',
    'validate_control_tag', 'get_suggested_tags_for_stride', 'categorize_tags',
    'search_predefined_tags', 'get_all_predefined_tags', 'get_tags_by_standard',
    'get_available_standards', 'get_standard_info'
]
