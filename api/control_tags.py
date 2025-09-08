"""
Security control tags utilities
Examples of tags that can be used in remediations

This module now uses a modular architecture where controls are organized
by standards in the 'standards' module. Maintains backward compatibility with all
existing functions.
"""

# Compatibility layer for control tags functionality
# This module re-exports functions from the standards module to maintain backward compatibility

from standards import (
    ALL_CONTROLS,
    STANDARDS_MAP,
    TAGS_MAP,
    STRIDE_CONTROL_EXAMPLES,
    get_tag_details,
    validate_control_tag,
    format_tag_for_display,
    normalize_tag_for_lookup,
    get_suggested_tags_for_stride,
    categorize_tags,
    search_predefined_tags,
    get_available_standards
)

try:
    from standards import get_all_predefined_tags
except ImportError:
    # If the function doesn't exist in standards module, provide a fallback
    def get_all_predefined_tags():
        """Get all predefined tags from ALL_CONTROLS formatted with standards as objects"""
        from standards import get_standard_from_tag_id
        results = []
        for tag_id, tag_info in ALL_CONTROLS.items():
            formatted_tag = format_tag_for_display(tag_id)
            if formatted_tag:
                results.append({
                    "tag": formatted_tag,
                    "tag_id": tag_id,
                    "title": tag_info.get('title', ''),
                    "description": tag_info.get('description', ''),
                    "category": tag_info.get('category', ''),
                    "standard": get_standard_from_tag_id(tag_id)  # Extraer automáticamente
                })
        return results

# Make everything available at module level
__all__ = [
    'ALL_CONTROLS',
    'STANDARDS_MAP', 
    'TAGS_MAP',
    'STRIDE_CONTROL_EXAMPLES',
    'get_tag_details',
    'validate_control_tag',
    'format_tag_for_display',
    'normalize_tag_for_lookup',
    'get_suggested_tags_for_stride',
    'categorize_tags',
    'search_predefined_tags',
    'get_all_predefined_tags',
    'get_available_standards'
]

# Alias functions for API compatibility
def search_control_tags(query: str, limit: int = 50):
    """
    Search for control tags by keyword or description with limit support.
    
    Args:
        query: Search query string
        limit: Maximum number of results to return
        
    Returns:
        list: List of control tag objects with full information for tooltips
    """
    from standards import get_standard_from_tag_id
    
    if not query or query.strip() == "":
        # Return all tags for empty query
        all_tag_ids = list(ALL_CONTROLS.keys())[:limit]
        results = []
        for tag_id in all_tag_ids:
            tag_info = ALL_CONTROLS.get(tag_id, {})
            results.append({
                "tag": format_tag_for_display(tag_id),
                "tag_id": tag_id,
                "title": tag_info.get('title', ''),
                "description": tag_info.get('description', ''),
                "category": tag_info.get('category', ''),
                "standard": get_standard_from_tag_id(tag_id)  # Extraer automáticamente
            })
        return results
    
    # Use the standards search function and format the results
    matching_tag_ids = search_predefined_tags(query)
    
    # Create detailed objects for each tag
    results = []
    for tag_id in matching_tag_ids[:limit]:
        tag_info = ALL_CONTROLS.get(tag_id, {})
        formatted_tag = format_tag_for_display(tag_id)
        if formatted_tag:
            results.append({
                "tag": formatted_tag,
                "tag_id": tag_id,
                "title": tag_info.get('title', ''),
                "description": tag_info.get('description', ''),
                "category": tag_info.get('category', ''),
                "standard": get_standard_from_tag_id(tag_id)  # Extraer automáticamente
            })
    
    return results

get_stride_suggestions = get_suggested_tags_for_stride
