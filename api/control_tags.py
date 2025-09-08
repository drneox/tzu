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
        """Get all predefined tags from ALL_CONTROLS formatted with standards"""
        all_tag_ids = list(ALL_CONTROLS.keys())
        return [format_tag_for_display(tag_id) for tag_id in all_tag_ids]

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
        list: List of formatted control tag strings (e.g., "V2.1.1 (ASVS)")
    """
    if not query or query.strip() == "":
        # Return all tags for empty query
        all_tag_ids = list(ALL_CONTROLS.keys())[:limit]
        return [format_tag_for_display(tag_id) for tag_id in all_tag_ids]
    
    # Use the standards search function and format the results
    matching_tag_ids = search_predefined_tags(query)
    
    # Format the tag IDs for display
    results = []
    for tag_id in matching_tag_ids[:limit]:
        formatted_tag = format_tag_for_display(tag_id)
        if formatted_tag:
            results.append(formatted_tag)
    
    return results

