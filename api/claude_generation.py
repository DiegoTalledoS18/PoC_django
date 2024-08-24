import anthropic
from .config import CLAUDE_API_KEY

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)


def generate_questions_from_claude(text):
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

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content