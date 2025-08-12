import json
from types import SimpleNamespace
from openai import OpenAI
client = OpenAI()
prompt_system = f"""
        eres un experto en seguridad informática, y realizaras un modelado de amenazas de manera detallada utilizando la metodología STRIDE
        y categorizando el riesgo utilizando DREAD.
        adicionalmente a los riesgos de DREAD consideraras un tipo de riesgo adicional llamado "compliance"
        para los riesgos asociados al cumplimiento segun el reglamento de ciberseguridad de la SBS de Perú. y devuelveme unicamente el analisis  en JSON y en español
        utilizando la siguiente estructura:
        {{
            "threats": [
                {{
                    "title": "Threat Title",
                    "description": "Detailed threat description.",
                    "categories": "STRIDE Category",
                    "remediation": "Recommended steps or strategies to mitigate or resolve the threat.",
                    "risk":[
                         "damage":"value 1 to 5",
                         "reproducibility":"value 1 to 5",
                         "exploitability":"value 1 to 5",
                         "affected_users":"value 1 to 5",
                         "discoverability":"value 1 to 5",
                         "compliance":"value 1 to 5"
                    ]"Here you will include a field for each dread category and each one will have a score from 1 to 5. all in lowcase"
                }},
                ...
            ]
        }}
        """
"""
        description: aqui indicaras la descripción del riesgo,
        type: aqui indicaras el tipo de riesgo segun STRIDE,
        risk: aqui incluiras un campo por cada categoría de dread  y cada uno tendrá un puntaje del 1 al 5.
        recommendation: aqui incluiras la recomendación del control para mitigar el riesgo en una lista.
        abuse_case: aqui describiras un caso de abuso para el riesgo
"""
"""
def clientAI(case):
  completion = client.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "%s" % prompt_system},
    {"role": "user", "content": case}
  ]
  )
"""
def clientAI(base64_image):
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
    "max_tokens": 300}
  ]
  )
  response_text = completion.choices[0].message.content.strip()
  json_start = response_text.find("{")
  json_end = response_text.rfind("}")
  if json_start != -1 and json_end != -1:
    json_content = response_text[json_start:json_end+1]
    try:
      threat_analysis_object = json.loads(json_content, object_hook=lambda d: SimpleNamespace(**d))
      return threat_analysis_object
    except json.JSONDecodeError:
                    pass
  else:
    return "[]"


