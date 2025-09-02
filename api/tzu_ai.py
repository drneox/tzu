import json
from types import SimpleNamespace
import os
from any_llm import completion

# Docker Compose pasa las variables de entorno automáticamente
# No necesitamos load_dotenv() ya que las variables están disponibles via env

prompt_system = f"""
You are a senior cybersecurity expert. Perform a detailed threat modeling analysis using the STRIDE methodology, explicitly referencing OWASP MASVS and ASVS categories where applicable, and categorize risks using the OWASP Risk Rating Methodology.

The input will be a conceptual diagram (it may be a sequence diagram, data flow diagram, use case diagram, or architectural diagram). It does not represent a real production system, only wireframes or conceptual models. Focus ONLY on the security perspective — no functional or architectural explanation is required.

Important requirements:
- Each threat must explicitly mention the **asset or flow** affected in the diagram (e.g., login form, API Gateway, session token, OTP mechanism, transaction service).
- Each threat must be classified into at least one **STRIDE category** and mapped to **MASVS/ASVS controls** if relevant.
- Each threat must include **concrete remediation controls**, aligned with ASVS/MASVS requirements and the Reglamento de Ciberseguridad de la SBS Perú (e.g., MFA required for financial transactions, SMS OTP not valid, secure session management, signed audit logs).
- For compliance-related threats, explicitly reference the **SBS Perú Cybersecurity Regulation**.
- Use ONLY the allowed numeric values for OWASP Risk Rating factors (no decimals, no values outside the list).
- Output MUST be in **Spanish** and ONLY in JSON format.

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
      "categories": "STRIDE Category and MASVS/ASVS Category if applicable",
      "remediation": "Recommended mitigation aligned with ASVS/MASVS and SBS regulation",
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

def clientAI(base64_image):
  print("\n=== INICIANDO ANÁLISIS CON CLIENTAI ===")
  try:
    # Obtener respuesta de la IA
    print("Enviando imagen a la API...")
    response = completion(
      model="openai/gpt-4o", # <provider_id>/<model_id>
      messages=[
        {"role": "system", "content": "%s" % prompt_system},
        {"role": "user", "content": [
        {"type": "image_url",
          "image_url":{
          "url": f"data:image/jpeg;base64,{base64_image}"
        }}
      ],
      "max_tokens": 3000000}
    ])
    print("Respuesta recibida de la API")
    
    # Extraer el texto de la respuesta
    response_text = response.choices[0].message.content.strip()
    json_start = response_text.find("{")
    json_end = response_text.rfind("}")
    print(response_text)
    
    # Extraer y procesar el JSON de la respuesta
    if json_start != -1 and json_end != -1:
      json_content = response_text[json_start:json_end+1]
      try:
        # Intentar parsear el JSON
        threat_analysis_object = json.loads(json_content, object_hook=lambda d: SimpleNamespace(**d))
        
        # Verificar que el objeto tiene la estructura esperada
        if not hasattr(threat_analysis_object, 'threats'):
          print("La respuesta no contiene la propiedad 'threats'")
          print(f"Propiedades disponibles: {dir(threat_analysis_object)}")
          # Crear objeto con estructura correcta pero sin amenazas
          empty_obj = SimpleNamespace()
          empty_obj.threats = []
          return empty_obj
        
        print(f"Objeto de análisis de amenazas encontrado con {len(threat_analysis_object.threats)} amenazas")
        print(f"Primera amenaza (si existe): {threat_analysis_object.threats[0] if threat_analysis_object.threats else 'Ninguna'}")
        return threat_analysis_object
      except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {str(e)}")
        # Retornar objeto vacío con estructura correcta
        empty_obj = SimpleNamespace()
        empty_obj.threats = []
        return empty_obj
    else:
      print("No se encontró contenido JSON en la respuesta")
      # Retornar objeto vacío con estructura correcta
      empty_obj = SimpleNamespace()
      empty_obj.threats = []
      return empty_obj
  except Exception as e:
    print(f"Error en el procesamiento de la IA: {str(e)}")
    # Retornar objeto vacío con estructura correcta
    empty_obj = SimpleNamespace()
    empty_obj.threats = []
    return empty_obj



