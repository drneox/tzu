"""
Standards module - Automatic security standards module
======================================================
This module dynamically loads all security standards from individual files.
To add a new standard, simply create a .py file with the {NAME}_CONTROLS variable.

Convention:
- File: standard_name.py  
- Variable: STANDARD_NAME_CONTROLS (uppercase)
- Example: asvs.py -> ASVS_CONTROLS, iso27001.py -> ISO27001_CONTROLS
"""

import os
import re
import importlib
from pathlib import Path

# Get current directory path
current_dir = Path(__file__).parent

# Dictionaries that will be filled automatically
ALL_CONTROLS = {}
STANDARDS_MAP = {}
TAGS_MAP = {}

def _load_standards_automatically():
    """
    Automatically loads all standards from .py files in the standards/ folder
    """
    global ALL_CONTROLS, STANDARDS_MAP, TAGS_MAP
    
    # Find all .py files except __init__.py
    standard_files = [f for f in os.listdir(current_dir) 
                     if f.endswith('.py') and not f.startswith('__')]
    
    loaded_standards = []
    
    for file_name in standard_files:
        try:
            # Extract module name (without .py)
            module_name = file_name[:-3]
            
            # Convert file name to variable name
            # e.g.: iso27001.py -> ISO27001, asvs.py -> ASVS
            standard_name = module_name.upper()
            controls_var_name = f"{standard_name}_CONTROLS"
            
            # Import module dynamically
            module = importlib.import_module(f'.{module_name}', package=__name__)
            
            # Check if the {NAME}_CONTROLS variable exists
            if hasattr(module, controls_var_name):
                controls = getattr(module, controls_var_name)
                
                # Add to standards mapping
                STANDARDS_MAP[standard_name] = controls
                
                # Create tags list
                TAGS_MAP[f"{standard_name}_TAGS"] = list(controls.keys())
                
                # Add to ALL_CONTROLS
                ALL_CONTROLS.update(controls)
                
                loaded_standards.append(f"{standard_name} ({len(controls)} controls)")
                
                print(f"✅ Loaded: {standard_name} with {len(controls)} controls")
            else:
                print(f"⚠️  Warning: {file_name} doesn't have {controls_var_name} variable")
                
        except Exception as e:
            print(f"❌ Error loading {file_name}: {e}")
    
    print(f"\n🎯 Automatic system loaded: {len(ALL_CONTROLS)} controls from {len(loaded_standards)} standards")
    return loaded_standards

# Load all standards automatically
_loaded_standards = _load_standards_automatically()

# Create dynamic variables for backward compatibility
for standard_name in STANDARDS_MAP.keys():
    # Create variables like ASVS_CONTROLS, MASVS_CONTROLS, etc.
    globals()[f"{standard_name}_CONTROLS"] = STANDARDS_MAP[standard_name]
    globals()[f"{standard_name}_TAGS"] = list(STANDARDS_MAP[standard_name].keys())

# STRIDE Control Examples (kept static for now)
STRIDE_CONTROL_EXAMPLES = {
    "SPOOFING": ["V2.1.1", "V2.2.1", "AUTH-1", "A.9.1.1", "PR.AC-1"],
    "TAMPERING": ["V4.1.1", "V4.2.1", "CODE-1", "A.8.2.1", "PR.DS-6"],
    "REPUDIATION": ["V3.1.1", "V3.2.1", "A.9.4.2", "PR.PT-1"],
    "INFORMATION_DISCLOSURE": ["V2.1.2", "V2.1.3", "STORAGE-1", "A.9.4.1", "PR.DS-1"],
    "DENIAL_OF_SERVICE": ["V1.1.1", "V1.2.1", "A.11.2.4", "PR.DS-4"],
    "ELEVATION_OF_PRIVILEGE": ["V4.1.1", "V4.2.1", "A.9.2.3", "PR.AC-4"]
}

# =====================================================
# UTILITY FUNCTIONS FOR TAG PROCESSING
# =====================================================

def get_standard_from_tag_id(tag_id: str) -> str:
    """
    Automatically extracts the standard from a tag_id using STANDARDS_MAP.
    
    Args:
        tag_id: Tag ID (e.g.: 'V2.1.1', 'AUTH-1')
    
    Returns:
        str: Standard name (e.g.: 'ASVS', 'MASVS')
    """
    for standard_name, controls in STANDARDS_MAP.items():
        if tag_id in controls:
            return standard_name
    return ""  # If not found

def normalize_tag_for_lookup(tag: str) -> str:
    """
    Simplified function for tag normalization.
    Standard files already have exact IDs as keys.
    
    Args:
        tag: Tag to normalize
    
    Returns:
        str: Clean tag (only trim and uppercase)
    """
    if not tag or tag is None:
        return ""
    
    # Only basic cleanup - files already have exact IDs
    return tag.strip().upper()

def get_tag_details(tag: str) -> dict:
    """
    Gets details for a specific tag.
    
    Args:
        tag: The tag identifier
    
    Returns:
        dict: Dictionary with title, description, category and standard, or None if not found
    """
    normalized_tag = normalize_tag_for_lookup(tag)
    control_details = ALL_CONTROLS.get(normalized_tag)
    
    if control_details is None:
        return None
    
    # Find which standard this tag belongs to
    standard = None
    for standard_name, controls in STANDARDS_MAP.items():
        if normalized_tag in controls:
            standard = standard_name
            break
    
    # Create a copy of the dictionary and add the standard field
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
    Validates if a tag corresponds to an existing control.
    
    Args:
        tag: Tag to validate
    
    Returns:
        bool: True if the tag exists, False otherwise
    """
    normalized_tag = normalize_tag_for_lookup(tag)
    return normalized_tag in ALL_CONTROLS

def get_suggested_tags_for_stride(stride_category: str) -> list:
    """
    Gets suggested tags for a specific STRIDE category with complete information.
    
    Args:
        stride_category: STRIDE category (e.g.: 'SPOOFING', 'TAMPERING')
    
    Returns:
        list: List of objects with complete information for suggested tags
    """
    # Normalize the category name - replace spaces with underscores and convert to uppercase
    normalized_category = stride_category.upper().replace(' ', '_')
    raw_tags = STRIDE_CONTROL_EXAMPLES.get(normalized_category, [])
    # Create complete objects for each tag
    results = []
    for tag_id in raw_tags:
        tag_info = ALL_CONTROLS.get(tag_id, {})
        formatted_tag = format_tag_for_display(tag_id)
        if formatted_tag:
            results.append({
                "tag": formatted_tag,
                "tag_id": tag_id,
                "title": tag_info.get('title', ''),
                "description": tag_info.get('description', ''),
                "category": tag_info.get('category', ''),
                "standard": get_standard_from_tag_id(tag_id)  # Extract automatically
            })
    return results

def categorize_tags(tags: list) -> dict:
    """
    Categorizes a list of tags by standard.
    
    Args:
        tags: List of tags
    
    Returns:
        dict: Dictionary with tags grouped by standard
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
    
    # Remove empty categories
    return {k: v for k, v in categorized.items() if v}

def search_predefined_tags(query: str) -> list:
    """
    Search predefined tags that match the query.
    Searches in: tag ID, title, description and also by standard.
    
    Args:
        query: Search term
    
    Returns:
        list: List of tags that match the search
    """
    if not query or len(query) < 2:
        return []
    
    # If the query is already formatted (contains parentheses), extract the base tag
    import re
    formatted_pattern = r'^(.+?)\s*\([^)]+\)$'
    match = re.match(formatted_pattern, query.strip())
    if match:
        # It's a formatted tag like "V2.1.1 (ASVS)", extract the base part
        base_query = match.group(1).strip()
        query_lower = base_query.lower()
    else:
        query_lower = query.lower()
    
    all_tags = list(ALL_CONTROLS.keys())
    
    # Search for exact matches first, then partial matches
    exact_matches = [tag for tag in all_tags if query_lower == tag.lower()]
    partial_matches = [tag for tag in all_tags if query_lower in tag.lower() and tag not in exact_matches]
    
    # Search by standard (e.g.: searching "ASVS" returns all ASVS tags)
    standard_matches = []
    query_upper = query.upper()
    if query_upper in STANDARDS_MAP:
        # If the query is exactly a standard, return all its tags
        standard_matches = list(STANDARDS_MAP[query_upper])
    else:
        # If the query contains part of a standard, search tags from that standard
        for standard_name, tags in STANDARDS_MAP.items():
            if query_upper in standard_name:
                standard_matches.extend(tags)
    
    # Also search in titles and descriptions
    content_matches = []
    for tag, info in ALL_CONTROLS.items():
        if tag not in exact_matches and tag not in partial_matches and tag not in standard_matches:
            if (query_lower in info.get("title", "").lower() or 
                query_lower in info.get("description", "").lower()):
                content_matches.append(tag)
    
    # Combine results with priority: exact, partial, by standard, by content
    results = exact_matches + partial_matches + standard_matches + content_matches
    
    # Remove duplicates maintaining order
    seen = set()
    unique_results = []
    for tag in results:
        if tag not in seen:
            seen.add(tag)
            unique_results.append(tag)
    
    return unique_results[:50]  # Increase limit for standard searches

def get_all_predefined_tags() -> list:
    """
    Get all predefined tags with complete information for tooltips.
    
    Returns:
        list: List of objects with complete tag information
    """
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
                "standard": get_standard_from_tag_id(tag_id)  # Extract automatically
            })
    return results

def get_tags_by_standard(standard: str) -> list:
    """
    Get tags from a specific standard.
    
    Args:
        standard: Standard name (e.g.: 'ASVS', 'NIST')
    
    Returns:
        list: List of tags from the specified standard
    """
    standard_upper = standard.upper()
    if standard_upper in STANDARDS_MAP:
        return list(STANDARDS_MAP[standard_upper].keys())
    return []

def get_available_standards() -> list:
    """
    Gets list of available standards loaded automatically.
    
    Returns:
        list: List of available standard names
    """
    return list(STANDARDS_MAP.keys())

def get_standard_info(standard_name: str = None) -> dict:
    """
    Gets detailed information for a specific standard or all standards.
    
    Args:
        standard_name: Standard name (optional)
    
    Returns:
        dict: Detailed information for the standard or all standards
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
        # Return information for all standards
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
    # Main dictionaries
    'ALL_CONTROLS', 'STANDARDS_MAP', 'STRIDE_CONTROL_EXAMPLES',
    
    # Dynamic variables per standard (created automatically)
    *[f"{std}_CONTROLS" for std in STANDARDS_MAP.keys()],
    *[f"{std}_TAGS" for std in STANDARDS_MAP.keys()],
    
    # Utility functions
    'normalize_tag_for_lookup', 'get_tag_details', 'format_tag_for_display',
    'validate_control_tag', 'get_suggested_tags_for_stride', 'categorize_tags',
    'search_predefined_tags', 'get_all_predefined_tags', 'get_tags_by_standard',
    'get_available_standards', 'get_standard_info'
]
