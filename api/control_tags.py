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
        """Get all predefined tags from ALL_CONTROLS"""
        return list(ALL_CONTROLS.keys())

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
