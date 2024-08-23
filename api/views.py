from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import fitz  # PyMuPDF
import os
from .generate_questions_gpt import generate_questions_from_text


@csrf_exempt
def welcome(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', 'World')
            return JsonResponse({'message': f'Hola {name}'})
        except json.JSONDecodeError:
            return JsonResponse({'message': f'Hola Anonimo'})
    return JsonResponse({'message': f'Hola Anonimo'})


@csrf_exempt
def process_pdf(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pdf_url = data.get('pdf_url', None)

            if not pdf_url:
                return JsonResponse({'error': 'No se proporcionó la URL del PDF'}, status=400)

            # Descargar el archivo PDF desde Firebase
            response = requests.get(pdf_url)
            if response.status_code != 200:
                return JsonResponse({'error': 'No se pudo descargar el archivo PDF'}, status=500)

            # Guardar el PDF en un archivo temporal
            with open('temp.pdf', 'wb') as f:
                f.write(response.content)

            # Extraer el texto del PDF
            pdf_text = pdf_to_text('temp.pdf')

            # Generar preguntas basadas en el texto
            questions = generate_questions_from_text(pdf_text)

            # Eliminar el archivo temporal
            os.remove('temp.pdf')

            # Convertir la respuesta de GPT a un objeto JSON si es necesario
            if isinstance(questions, str):
                try:
                    questions = json.loads(questions)
                except json.JSONDecodeError:
                    return JsonResponse({'error': 'Error al procesar la respuesta de GPT como JSON'}, status=500)

            # Retornar el JSON como respuesta exitosa
            return JsonResponse({'questions': questions})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)



def pdf_to_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    pdf_document.close()
    return text
