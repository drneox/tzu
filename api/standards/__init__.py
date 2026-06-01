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
STANDARDS_VERSIONS = {}  # standard_name -> version string

def _load_standards_automatically():
    """
    Automatically loads all standards from .py files in the standards/ folder
    """
    global ALL_CONTROLS, STANDARDS_MAP, TAGS_MAP, STANDARDS_VERSIONS
    
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
                
                # Load version if defined in the module
                if hasattr(module, 'VERSION'):
                    STANDARDS_VERSIONS[standard_name] = module.VERSION
                
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

# STRIDE Control Examples — one real tag per relevant standard per category
STRIDE_CONTROL_EXAMPLES = {
    "SPOOFING": ["V2.1.1", "V2.2.1", "AUTH-1", "A.9.1.1", "PR.AC-1", "SBS-2158-5"],
    "TAMPERING": ["V4.1.1", "V4.2.1", "CODE-1", "A.8.2.1", "PR.DS-6", "SBS-2158-7"],
    "REPUDIATION": ["V3.1.1", "V3.2.1", "A.9.4.2", "PR.PT-1", "SBS-2158-8"],
    "INFORMATION_DISCLOSURE": ["V2.1.2", "V2.1.3", "STORAGE-1", "A.9.4.1", "PR.DS-1", "SBS-2158-4"],
    "DENIAL_OF_SERVICE": ["V1.1.1", "V1.2.1", "A.11.2.4", "PR.DS-4", "SBS-2167-8"],
    "ELEVATION_OF_PRIVILEGE": ["V4.1.1", "V4.2.1", "A.9.2.3", "PR.AC-4", "SBS-2158-6"],
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
    Strips the '(STANDARD)' suffix if present, e.g. 'A.9.2.4 (ISO27001)' → 'A.9.2.4'.
    
    Args:
        tag: Tag to normalize
    
    Returns:
        str: Clean tag ID ready for dict lookup
    """
    if not tag or tag is None:
        return ""
    
    tag = tag.strip()
    # Strip standard suffix like " (ASVS)" or "(ISO27001)"
    import re as _re_local
    m = _re_local.match(r'^(.+?)\s*\([^)]+\)\s*$', tag)
    if m:
        tag = m.group(1).strip()
    # Normalize MASVS v2.0 prefix: "MASVS-AUTH-2" → "AUTH-2"
    # Normalize MASVS v1.x prefix: "MSTG-AUTH-2" → "AUTH-2"
    tag_upper = tag.upper()
    if tag_upper.startswith("MASVS-"):
        tag = tag[6:]
    elif tag_upper.startswith("MSTG-"):
        tag = tag[5:]
    return tag.upper()

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

def get_standards_catalog_for_prompt() -> str:
    """
    Returns a compact text block with version and format hints per standard for
    inclusion in the AI system prompt (~100 extra tokens).  The goal is to
    constrain the model to IDs that exist in the local catalog without listing
    all controls explicitly.
    """
    # Format hints keyed by standard name
    _FORMAT_HINTS = {
        "ASVS":     "formato V{chapter}.{section}.{control} (ej. V2.1.1, V4.1.1, V7.5.3)",
        "MASVS":    "formato CATEGORY-N o MASVS-CATEGORY-N (ej. AUTH-1, MASVS-AUTH-2, STORAGE-2, CODE-3)",
        "NIST":     "SOLO formato CSF XX.YY-N (ej. PR.AC-1, DE.CM-1). "
                    "NO usar controles SP 800-53 (SC-8, AC-2, IA-5, etc.)",
        "ISO27001": "formato A.{seccion}.{subseccion}.{control} (ej. A.9.1.1, A.10.1.1)",
        "SBS":      "SOLO controles de la Circular SBS G-504-2021 (Ciberseguridad). "
                    "Formato SBS-504-{N} (ej. SBS-504-1, SBS-504-8, SBS-504-16)",
    }

    lines = []
    for std_name in sorted(STANDARDS_MAP.keys()):
        version = STANDARDS_VERSIONS.get(std_name, "")
        count = len(STANDARDS_MAP[std_name])
        version_label = f" v{version}" if version else ""
        hint = _FORMAT_HINTS.get(std_name, "")
        lines.append(f"- **{std_name}{version_label}** ({count} controles): {hint}")
    return "\n".join(lines)

def rag_lite_suggest(context_text: str, top_n_per_standard: int = 4) -> dict:
    """
    Keyword-based pre-filter (RAG lite): scores every control in ALL_CONTROLS
    against the query text and returns the top N per standard.

    No external dependencies — pure Python token-overlap scoring.

    Args:
        context_text: Combined threat context (system description, STRIDE hints, etc.)
        top_n_per_standard: Number of controls to return per standard

    Returns:
        dict: {standard_name: [{"tag": formatted, "title": str}, ...]}
    """
    from collections import Counter

    # Minimal stopwords (ES + EN)
    _STOP = {
        'de','la','el','en','y','a','los','del','se','las','por','un','para',
        'con','una','su','al','lo','como','más','o','pero','sus','le','ha',
        'me','si','sin','sobre','ser','e','no','que','es','son','muy','te',
        'ya','ni','este','esta','son','fue','the','of','and','in','is','to',
        'it','for','on','are','an','or','not','this','that','with','all',
    }

    def _tok(text):
        return [t for t in re.findall(r'[a-záéíóúüña-z]{3,}', text.lower()) if t not in _STOP]

    query_counter = Counter(_tok(context_text))
    if not query_counter:
        return {}

    per_standard: dict = {}

    for tag_id, entry in ALL_CONTROLS.items():
        ctrl_text = f"{entry.get('title','')} {entry.get('description','')} {entry.get('category','')}"
        ctrl_counter = Counter(_tok(ctrl_text))
        score = sum(min(query_counter[t], ctrl_counter[t]) for t in query_counter if t in ctrl_counter)
        if score == 0:
            continue
        # Normalize by sqrt of control length to avoid bias toward long descriptions
        ctrl_len = sum(ctrl_counter.values()) or 1
        norm_score = score / (ctrl_len ** 0.5)

        std = get_standard_from_tag_id(tag_id)
        if not std:
            continue
        per_standard.setdefault(std, []).append((norm_score, tag_id, entry))

    result = {}
    for std, items in per_standard.items():
        items.sort(key=lambda x: x[0], reverse=True)
        result[std] = [
            {"tag": format_tag_for_display(tag_id) or tag_id, "title": entry.get("title", "")}
            for _, tag_id, entry in items[:top_n_per_standard]
        ]
    return result


def format_rag_lite_for_prompt(rag_results: dict) -> str:
    """
    Formats rag_lite_suggest() output as a compact block for prompt injection.
    Each line: - **STD**: TAG (Title), TAG (Title), ...
    """
    if not rag_results:
        return ""
    lines = []
    for std in sorted(rag_results.keys()):
        controls = rag_results[std]
        if not controls:
            continue
        tags_str = ", ".join(f"{c['tag']} ({c['title']})" for c in controls)
        lines.append(f"- **{std}**: {tags_str}")
    return "\n".join(lines)


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
# =====================================================
# EXPORTS FOR COMPATIBILITY
# =====================================================

# =====================================================
# CONTROL TAG VALIDATION & CORRECTION (Option B)
# =====================================================

import re as _re

# Regex patterns that identify each standard's tag format
_STANDARD_PATTERNS = {
    "ASVS":     _re.compile(r'^V\d+\.\d+\.\d+$'),
    "MASVS":    _re.compile(r'^[A-Z]+-\d+$'),
    "NIST":     _re.compile(r'^([A-Z]{2,3}\.[A-Z]{2,3}-\d+|[A-Z]{2,3}-\d+(\(\d+\))?)$'),  # CSF and SP 800-53
    "ISO27001": _re.compile(r'^(ISO27001-)?A\.\d+\.\d+\.\d+$'),
    "SBS":      _re.compile(r'^SBS-\d{3,4}-\d+(\.\d+)?$'),  # 3 o 4 dígitos: SBS-504-1, SBS-2158-1
}


def _parse_formatted_tag(formatted_tag: str):
    """
    Parses 'V2.1.1 (ASVS)' → (tag_id='V2.1.1', standard_hint='ASVS').
    Also handles bare IDs like 'V2.1.1'.
    """
    m = _re.match(r'^(.+?)\s*\(([^)]+)\)\s*$', formatted_tag.strip())
    if m:
        return m.group(1).strip(), m.group(2).strip().upper()
    return formatted_tag.strip(), None


def _detect_standard_from_pattern(tag_id: str) -> str:
    """Returns the standard name if tag_id matches its format pattern, else ''."""
    for std, pattern in _STANDARD_PATTERNS.items():
        if pattern.match(tag_id):
            return std
    return ""


def _closest_sbs_tag(tag_id: str) -> str | None:
    """
    Given an invalid SBS tag, tries to find the closest valid SBS tag.
    Returns None if the resolution doesn't exist in our dict (caller will keep as-is).

    Strategy:
    1. Strip dotted subpoints: SBS-2158-3.2 → SBS-2158-3 (direct hit if it exists).
    2. Same resolution → pick the one with the nearest control number.
    3. If the resolution is not in our dict at all → return None (keep original tag).
    """
    sbs_tags = list(STANDARDS_MAP.get("SBS", {}).keys())
    if not sbs_tags:
        return None

    # Strip dotted subpoints: SBS-2158-3.2 → SBS-2158-3
    stripped = _re.sub(r'^(SBS-\d+-\d+)\.\d+$', r'\1', tag_id)
    if stripped in STANDARDS_MAP.get("SBS", {}):
        return stripped  # Direct hit after stripping subpoint

    # Use stripped form for further matching (or original if unchanged)
    candidate = stripped if stripped != tag_id else tag_id

    # Extract resolution and control number
    m = _re.match(r'^SBS-(\d+)-(\d+)$', candidate)
    if m:
        resolution = m.group(1)
        requested_num = int(m.group(2))
        # Collect tags with the same resolution
        same_res = []
        for t in sbs_tags:
            tm = _re.match(r'^SBS-(\d+)-(\d+)$', t)
            if tm and tm.group(1) == resolution:
                same_res.append((int(tm.group(2)), t))
        if same_res:
            # Resolution exists in our dict → correct to nearest control number
            same_res.sort(key=lambda x: abs(x[0] - requested_num))
            return same_res[0][1]
        # Resolution not in our dict → return None to keep the tag as-is
        return None

    return None


def validate_and_correct_control_tags(tags: list) -> list:
    """
    Validates and corrects control tags returned by the LLM.

    Rules:
    - Tags found in ALL_CONTROLS: kept as-is (returned in 'ID (STANDARD)' format).
    - Tags NOT in ALL_CONTROLS but whose ID matches a known format for
      ASVS / NIST / ISO27001 / MASVS: accepted as-is (LLM knows the full standard;
      our mapping is a curated subset).
    - SBS tags NOT in ALL_CONTROLS: corrected to the closest valid SBS tag.
    - Tags with unrecognised format: removed.

    Args:
        tags: List of tag strings in any format, e.g. ['V2.1.1 (ASVS)', 'SBS-2158-99']

    Returns:
        Deduplicated list of validated/corrected tags in 'ID (STANDARD)' format.
    """
    result = []
    seen = set()

    for raw in tags:
        if not isinstance(raw, str) or not raw.strip():
            continue

        tag_id, standard_hint = _parse_formatted_tag(raw)

        # 1. Exact match in our dictionary
        if tag_id in ALL_CONTROLS:
            formatted = format_tag_for_display(tag_id)
            if formatted and formatted not in seen:
                seen.add(formatted)
                result.append(formatted)
            continue

        # 2. Determine effective standard, trusting the hint when provided.
        # Without this, MAVSV's broad pattern ^[A-Z]+-\d+$ would match NIST SP 800-53
        # tags like SC-8, AC-2, etc. before the NIST pattern is checked.
        if standard_hint and standard_hint in _STANDARD_PATTERNS:
            if _STANDARD_PATTERNS[standard_hint].match(tag_id):
                detected_std = standard_hint  # hint is plausible — trust it
            else:
                detected_std = _detect_standard_from_pattern(tag_id)
        else:
            detected_std = _detect_standard_from_pattern(tag_id)
        effective_std = detected_std or standard_hint or ""

        if effective_std == "SBS":
            # SBS is custom: try to correct to a real tag
            corrected_id = _closest_sbs_tag(tag_id)
            if corrected_id:
                # Known resolution: use the corrected tag from our dict
                formatted = format_tag_for_display(corrected_id)
            else:
                # Unknown resolution: keep as-is (like NIST SP 800-53 tags not in our dict)
                formatted = f"{tag_id} (SBS)"
            if formatted and formatted not in seen:
                seen.add(formatted)
                result.append(formatted)
        elif effective_std in ("ASVS", "NIST", "ISO27001", "MASVS"):
            # Well-known standard: accept the tag even if not in our mapping
            formatted = f"{tag_id} ({effective_std})"
            if formatted not in seen:
                seen.add(formatted)
                result.append(formatted)
        # else: unknown format → discard silently

    return result



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
    'get_available_standards', 'get_standards_catalog_for_prompt',
    'get_standard_info', 'validate_and_correct_control_tags'
]
