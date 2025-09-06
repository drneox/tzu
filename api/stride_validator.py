# STRIDE Category Validation and Normalization
"""
Módulo para validar y normalizar categorías STRIDE.
Asegura consistencia en la nomenclatura de las categorías.
"""

# STRIDE Categories constants for validation
VALID_STRIDE_CATEGORIES = {
    'Spoofing',
    'Tampering', 
    'Repudiation',
    'Information Disclosure',
    'Denial of Service',
    'Elevation of Privilege'
}

def normalize_stride_category(category_input):
    """
    Normaliza y valida categorías STRIDE para asegurar consistencia.
    
    Args:
        category_input (str): Categoría STRIDE a normalizar
        
    Returns:
        str: Categoría normalizada si es válida, None si no es válida
        
    Examples:
        normalize_stride_category("spoofing") -> "Spoofing"
        normalize_stride_category("INFORMATION DISCLOSURE") -> "Information Disclosure"
        normalize_stride_category("invalid") -> None
    """
    if not category_input or not isinstance(category_input, str):
        return None
    
    # Limpiar espacios y normalizar
    cleaned = category_input.strip()
    
    # Buscar coincidencia exacta (case-insensitive)
    for valid_category in VALID_STRIDE_CATEGORIES:
        if cleaned.lower() == valid_category.lower():
            return valid_category
    
    # Buscar coincidencia parcial (por si la IA devuelve texto extra)
    for valid_category in VALID_STRIDE_CATEGORIES:
        if valid_category.lower() in cleaned.lower():
            return valid_category
    
    # Si no encuentra coincidencia, retornar None
    return None

def is_valid_stride_category(category):
    """
    Verifica si una categoría es válida.
    
    Args:
        category (str): Categoría a verificar
        
    Returns:
        bool: True si es válida, False en caso contrario
    """
    return normalize_stride_category(category) is not None

def get_valid_stride_categories():
    """
    Retorna la lista de categorías STRIDE válidas.
    
    Returns:
        set: Conjunto de categorías válidas
    """
    return VALID_STRIDE_CATEGORIES.copy()
