# api/generate_questions_gpt.py

from openai import OpenAI
from .config import OPENAI_API_KEY

# Configurar el cliente OpenAI con la clave API importada
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_questions_from_text(text):
    prompt = f"Utiliza el siguiente texto para generar 5 preguntas de opción múltiple:\n\n{text}"

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "Eres un experto en generar preguntas de opción múltiple basadas en un texto proporcionado."},
            {"role": "user", "content": prompt}
        ]
    )

    response = completion.choices[0].message.content
    # Procesa la respuesta y formatea las preguntas en un formato JSON
    # Supongamos que el formato ya es JSON, si no, deberás procesar la respuesta adecuadamente
    import json
    try:
        questions = json.loads(response)
    except json.JSONDecodeError:
        questions = []

    return questions
