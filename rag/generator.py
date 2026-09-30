import os
from google import genai
from google.genai import types

# 1. Configurar la clave directamente en las variables de entorno del sistema
# Esto resuelve el error 401 UNAUTHENTICATED al obligar al cliente a autenticar correctamente
API_KEY_VAL = "API AQUI"
os.environ["GEMINI_API_KEY"] = API_KEY_VAL

# 2. Inicializar el cliente sin argumentos (tomará GEMINI_API_KEY del entorno)
client = genai.Client()

SYSTEM_PROMPT = """
Eres un asistente virtual experto y especializado EXCLUSIVAMENTE en Inteligencia Artificial, Sistemas, Programación, Desarrollo de Software y Tecnología en general.

REGLAS OBLIGATORIAS:
1. Analiza la PREGUNTA del usuario y determina si pertenece al ámbito de la Inteligencia Artificial, Sistemas, Informática o Tecnología.
2. Si la PREGUNTA es sobre IA, Sistemas o Tecnología:
   - Responde de forma detallada, clara y precisa.
   - Utiliza el CONTEXTO RECUPERADO si contiene información útil. Si el contexto no es suficiente, utiliza tus conocimientos generales sobre Inteligencia Artificial y Tecnología para responder la duda del usuario.
3. Si la PREGUNTA trata sobre un tema AJENO a la tecnología (por ejemplo: animales, cocina, deportes, entretenimiento, chismes, historia no tecnológica, etc.):
   - RECHAZA responder la pregunta directamente.
   - Responde exactamente con el siguiente mensaje:
     "Lo siento, únicamente estoy especializado en temas de Inteligencia Artificial, Sistemas, Programación y Tecnología. Por favor, hazme una consulta relacionada con estos temas."
"""

def generate_answer(query: str, context: list) -> str:
    """
    Genera la respuesta aplicando el filtro de tecnología usando la SDK oficial google-genai.
    """
    if context:
        context_text = "\n\n".join(f"- {doc}" for doc in context)
    else:
        context_text = "No se encontraron fragmentos relevantes en la base de conocimiento local."

    prompt_usuario = f"""
CONTEXTO RECUPERADO DE LA BASE DE CONOCIMIENTO LOCAL:
{context_text}

PREGUNTA DEL USUARIO:
{query}
"""

    modelos_disponibles = [
        "gemini-3.5-flash-lite",
        "gemini-3.6-flash"
    ]

    for model_name in modelos_disponibles:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt_usuario,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2
                )
            )
            return response.text
        except Exception as e:
            # Si el modelo específico da error 404, pasa al siguiente de la lista
            if "404" in str(e) or "NOT_FOUND" in str(e):
                continue
            return f"Error al consultar la API de Google Gemini: {str(e)}"

    return "Error: Ninguno de los modelos probados está disponible para este proyecto."