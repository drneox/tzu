import json
from types import SimpleNamespace
import os
from any_llm import completion
import control_tags
import standards
from stride_validator import get_valid_stride_categories

# Docker Compose pasa las variables de entorno automáticamente
# No necesitamos load_dotenv() ya que las variables están disponibles via env

def generate_control_tags_examples():
    """
    Genera ejemplos dinámicos de control tags basados en las definiciones del sistema
    """
    examples = {}
    stride_categories = list(get_valid_stride_categories())
    
    for category in stride_categories:
        try:
            # Get suggested tags for each STRIDE category
            suggested_tags = control_tags.get_suggested_tags_for_stride(category)
            # Format tags with parentheses for AI display
            formatted_tags = [tag["tag"] for tag in suggested_tags[:3]]  # Only first 3
            examples[category] = formatted_tags
        except:
            # Fallback in case of error
            examples[category] = ["V2.1.1 (ASVS)", "AUTH-1 (MASVS)", "SBS-2158-1 (SBS)"]
    
    return examples

def clientAI(base64_image):
  try:
    # Generar ejemplos dinámicos de control tags
    control_tag_examples = generate_control_tags_examples()
    
    # Generar información dinámica sobre estándares disponibles
    available_standards = standards.get_available_standards()
    standards_list = ", ".join(available_standards)
    standards_info = f"The system includes {len(standards.ALL_CONTROLS)} security controls from  {len(available_standards)} international standards: {standards_list}."
    
    # Construir ejemplos para el prompt
    examples_text = ""
    for category, tags in control_tag_examples.items():
        examples_text += f"**{category} threats**: {', '.join(tags)}\n"
    
    # Create dynamic prompt with updated examples
    dynamic_prompt = f"""
You are a senior cybersecurity expert. Perform a detailed threat modeling analysis using the STRIDE methodology, explicitly referencing OWASP MASVS and ASVS categories where applicable, and categorize risks using the OWASP Risk Rating Methodology.

The input will be a conceptual diagram (it may be a sequence diagram, data flow diagram, use case diagram, or architectural diagram). It does not represent a real production system, only wireframes or conceptual models. Focus ONLY on the security perspective — no functional or architectural explanation is required.

Important requirements:
- Each threat must explicitly mention the **asset or flow** affected in the diagram (e.g., login form, API Gateway, session token, OTP mechanism, transaction service).
- Each threat must be classified into exactly ONE **STRIDE category**: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, or Elevation of Privilege.
- Each threat must include **concrete remediation controls** with clear, actionable mitigation steps (e.g., implement multi-factor authentication, validate all inputs, use secure session management, maintain audit logs).
- Each remediation MUST have a **direct mapping** to the control_tags provided.
- For compliance-related threats, explicitly reference the **SBS Perú Cybersecurity Regulation** in the remediation description and in the control_tags.
- Each threat must include a **control_tags array** with specific identifiers from at least two different standards (e.g., one ASVS + one MASVS, or ASVS + ISO27001). Control tags must always be aligned with the remediation step.
- Use ONLY the allowed numeric values for OWASP Risk Rating factors (no decimals, no values outside the list).
- Output MUST be in **Spanish** and ONLY in JSON format.

Control Tags Guidelines:
{standards_info}

- Select controls that are SPECIFIC and MATCH the remediation described.
- Use a diversity of standards depending on the threat type.
- Examples:
{examples_text}

Remediation Format:
- Write clear, actionable mitigation steps without control references in the text.
- Control references must only go inside the control_tags array.
- Example: "Implementar autenticación multifactor obligatoria para todas las transacciones financieras y validar la identidad del usuario mediante al menos dos factores diferentes."

Allowed values:
Threat Agent Factors:
- skill_level: [0, 1, 3, 5, 6, 9]
- motive: [0, 1, 4, 9]
- opportunity: [0, 4, 7, 9]
- size: [0, 2, 4, 5, 6, 9]

Vulnerability Factors:
- ease_of_discovery: [0, 1, 3, 7, 9]
- ease_of_exploit: [0, 1, 3, 5, 9]
- awareness: [0, 1, 4, 6, 9]
- intrusion_detection: [0, 1, 3, 8, 9]

Technical Impact Factors:
- loss_of_confidentiality: [0, 2, 6, 7, 9]
- loss_of_integrity: [0, 1, 3, 5, 7, 9]
- loss_of_availability: [0, 1, 5, 7, 9]
- loss_of_accountability: [0, 1, 7, 9]

Business Impact Factors:
- financial_damage: [0, 1, 3, 7, 9]
- reputation_damage: [0, 1, 4, 5, 9]
- non_compliance: [0, 2, 5, 7]
- privacy_violation: [0, 3, 5, 7, 9]

Use the following JSON output structure:

{{
  "threats": [
    {{
      "title": "Threat Title",
      "description": "Detailed threat description.",
      "type": "One STRIDE category: Spoofing | Tampering | Repudiation | Information Disclosure | Denial of Service | Elevation of Privilege",
      "remediation": {{
        "description": "Clear, actionable mitigation steps without control references. Focus on implementation details and best practices.",
        "control_tags": ["V2.1.1 (ASVS)", "AUTH-1 (MASVS)", "SBS-2158-1 (SBS)"]
      }},
      "risk": {{
        "skill_level": "value from list",
        "motive": "value from list",
        "opportunity": "value from list",
        "size": "value from list",
        "ease_of_discovery": "value from list",
        "ease_of_exploit": "value from list",
        "awareness": "value from list",
        "intrusion_detection": "value from list",
        "loss_of_confidentiality": "value from list",
        "loss_of_integrity": "value from list",
        "loss_of_availability": "value from list",
        "loss_of_accountability": "value from list",
        "financial_damage": "value from list",
        "reputation_damage": "value from list",
        "non_compliance": "value from list",
        "privacy_violation": "value from list"
      }}
    }}
  ]
}}
"""
    
    # Get AI response
    response = completion(
      model="openai/gpt-4o", # <provider_id>/<model_id>
      messages=[
        {"role": "system", "content": "%s" % dynamic_prompt},
        {"role": "user", "content": [
        {"type": "image_url",
          "image_url":{
          "url": f"data:image/jpeg;base64,{base64_image}"
        }}
      ],
      "max_tokens": None}
    ])
    
    # Extraer el texto de la respuesta
    response_text = response.choices[0].message.content.strip()
    json_start = response_text.find("{")
    json_end = response_text.rfind("}")
    
    # Extraer y procesar el JSON de la respuesta
    if json_start != -1 and json_end != -1:
      json_content = response_text[json_start:json_end+1]
      try:
        # Intentar parsear el JSON
        threat_analysis_object = json.loads(json_content, object_hook=lambda d: SimpleNamespace(**d))
        
        # Verify that object has expected structure
        if not hasattr(threat_analysis_object, 'threats'):
          # Create object with correct structure but no threats
          empty_obj = SimpleNamespace()
          empty_obj.threats = []
          return empty_obj
        
        return threat_analysis_object
      except json.JSONDecodeError as e:
        # Retornar objeto vacío con estructura correcta
        empty_obj = SimpleNamespace()
        empty_obj.threats = []
        return empty_obj
    else:
      # Retornar objeto vacío con estructura correcta
      empty_obj = SimpleNamespace()
      empty_obj.threats = []
      return empty_obj
  except Exception as e:
    # Retornar objeto vacío con estructura correcta
    empty_obj = SimpleNamespace()
    empty_obj.threats = []
    return empty_obj



