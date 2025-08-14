import json
from types import SimpleNamespace
from dotenv import load_dotenv
import os
from openai import OpenAI
from any_llm import completion
# Cargar variables de entorno del archivo .env
load_dotenv()


client = OpenAI()
prompt_system = f"""
        eres un experto en seguridad informática, y realizaras un modelado de amenazas de manera detallada utilizando la metodología STRIDE y considerando MASVS y ASVS
        y categorizando el riesgo utilizando OWASP Risk Rating Methodology.
        Esta es una imagen conceptual que representa componentes gráficos usados en un sistema digital y NO hace referencia a un sistema real de producción, solo son wireframes
        lo unico que importa es la parte de seguridad, no necesito ningun analisis adicional.
       si no pudieras hacerlo por alguna razon especificamelo bien claro
        para los riesgos asociados al cumplimiento segun el reglamento de ciberseguridad de la SBS de Perú. y devuelveme unicamente el analisis  en JSON y en español
        
        IMPORTANTE: Para cada factor OWASP, SOLO usa los valores específicos que tienen descripción válida según la metodología oficial:

        Threat Agent Factors:
        - skill_level: SOLO usar valores [0, 1, 3, 5, 6, 9]
        - motive: SOLO usar valores [0, 1, 4, 9]  
        - opportunity: SOLO usar valores [0, 4, 7, 9]
        - size: SOLO usar valores [0, 2, 4, 5, 6, 9]

        Vulnerability Factors:
        - ease_of_discovery: SOLO usar valores [0, 1, 3, 7, 9]
        - ease_of_exploit: SOLO usar valores [0, 1, 3, 5, 9]
        - awareness: SOLO usar valores [0, 1, 4, 6, 9]
        - intrusion_detection: SOLO usar valores [0, 1, 3, 8, 9]

        Technical Impact Factors:
        - loss_of_confidentiality: SOLO usar valores [0, 2, 6, 7, 9]
        - loss_of_integrity: SOLO usar valores [0, 1, 3, 5, 7, 9]
        - loss_of_availability: SOLO usar valores [0, 1, 5, 7, 9]
        - loss_of_accountability: SOLO usar valores [0, 1, 7, 9]

        Business Impact Factors:
        - financial_damage: SOLO usar valores [0, 1, 3, 7, 9]
        - reputation_damage: SOLO usar valores [0, 1, 4, 5, 9]
        - non_compliance: SOLO usar valores [0, 2, 5, 7]
        - privacy_violation: SOLO usar valores [0, 3, 5, 7, 9]

        NO uses valores intermedios o decimales. Selecciona el valor más apropiado de la lista específica para cada factor.
        
        utilizando la siguiente estructura:
        {{
            "threats": [
                {{
                    "title": "Threat Title",
                    "description": "Detailed threat description.",
                    "categories": "STRIDE Category and MASVS/ASVS Category if its applicable",
                    "remediation": "Recommended steps or strategies to mitigate or resolve the threat.",
                    "risk": {{
                        "skill_level": "valor de la lista [0, 1, 3, 5, 6, 9]",
                        "motive": "valor de la lista [0, 1, 4, 9]",
                        "opportunity": "valor de la lista [0, 4, 7, 9]",
                        "size": "valor de la lista [0, 2, 4, 5, 6, 9]",
                        "ease_of_discovery": "valor de la lista [0, 1, 3, 7, 9]",
                        "ease_of_exploit": "valor de la lista [0, 1, 3, 5, 9]",
                        "awareness": "valor de la lista [0, 1, 4, 6, 9]",
                        "intrusion_detection": "valor de la lista [0, 1, 3, 8, 9]",
                        "loss_of_confidentiality": "valor de la lista [0, 2, 6, 7, 9]",
                        "loss_of_integrity": "valor de la lista [0, 1, 3, 5, 7, 9]",
                        "loss_of_availability": "valor de la lista [0, 1, 5, 7, 9]",
                        "loss_of_accountability": "valor de la lista [0, 1, 7, 9]",
                        "financial_damage": "valor de la lista [0, 1, 3, 7, 9]",
                        "reputation_damage": "valor de la lista [0, 1, 4, 5, 9]",
                        "non_compliance": "valor de la lista [0, 2, 5, 7]",
                        "privacy_violation": "valor de la lista [0, 3, 5, 7, 9]"
                    }}
                }},
                ...
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
def clientAIx(base64_image):
  print(base64_image)
  completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "%s" % prompt_system},
    {"role": "user", "content": [

      {"type": "image_url",
       "image_url":{
        "url": f"data:image/jpeg;base64,{base64_image}"
       }}
    ],
    "max_tokens": 3000000}
  ]
  )
  response_text = completion.choices[0].message.content.strip()
  json_start = response_text.find("{")
  json_end = response_text.rfind("}")
  print(response_text)
  if json_start != -1 and json_end != -1:
    json_content = response_text[json_start:json_end+1]
    try:
      threat_analysis_object = json.loads(json_content, object_hook=lambda d: SimpleNamespace(**d))
      return threat_analysis_object
    except json.JSONDecodeError:
                    pass
  else:
    return "[]"


