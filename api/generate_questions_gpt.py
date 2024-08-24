# api/generate_questions_gpt.py

from openai import OpenAI
from .config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_questions_from_gpt(text):
    prompt = f"""Utiliza el siguiente texto para generar 5 preguntas de opción múltiple en el siguiente formato JSON:
       {{
         "questions": [
           {{
             "question": "Pregunta aquí",
             "alternatives": ["Opción 1", "Opción 2", "Opción 3", "Opción 4"],
             "answer": 0
           }},
           // Agregar más preguntas
         ]
       }}\n\nTexto:\n{text}"""

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "Eres un experto en generar preguntas de opción múltiple basadas en un texto proporcionado."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    # Devuelve la respuesta en crudo sin procesar
    return completion.choices[0].message.content

