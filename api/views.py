from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
import fitz  # PyMuPDF
import os
from .generate_questions_gpt import generate_questions_from_gpt
from .gemini_generation import generate_questions_from_gemini
from .claude_generation import generate_questions_from_claude
import time

@csrf_exempt
def welcome(request):
    if request.method == 'GET':
        try:
            data = json.loads(request.body)
            name = data.get('name', 'Anonimo')
            return JsonResponse({'message': f'Hola {name}'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Error en la decodificación JSON'}, status=400)
    return JsonResponse({'message': 'Método no permitido'}, status=405)

@csrf_exempt
def process_pdf_gpt(request):
    if request.method == 'POST':
        start_time = time.time()  # Empieza el temporizador
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
            temp_pdf_path = 'temp.pdf'
            with open(temp_pdf_path, 'wb') as f:
                f.write(response.content)

            # Obtener el tamaño del archivo PDF en kilobytes
            pdf_size_kb = os.path.getsize(temp_pdf_path) / 1024

            # Extraer el texto del PDF
            pdf_text = pdf_to_text(temp_pdf_path)

            # Generar preguntas basadas en el texto
            questions = generate_questions_from_gpt(pdf_text)

            # Eliminar el archivo temporal
            os.remove(temp_pdf_path)

            # Convertir la respuesta de GPT a un objeto JSON si es necesario
            if isinstance(questions, str):
                try:
                    questions = json.loads(questions)
                except json.JSONDecodeError:
                    return JsonResponse({'error': 'Error al procesar la respuesta de GPT como JSON'}, status=500)

            # Calcular el tiempo transcurrido
            elapsed_time = time.time() - start_time
            print(f"Tiempo de generación GPT: {elapsed_time:.2f} segundos | PDF: {pdf_size_kb:.2f} KB")

            # Retornar el JSON como respuesta exitosa sin anidar "questions" innecesariamente
            print(questions)
            return JsonResponse(questions)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def process_pdf_gemini(request):
    if request.method == 'POST':
        start_time = time.time()  # Empieza el temporizador
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
            temp_pdf_path = 'temp.pdf'
            with open(temp_pdf_path, 'wb') as f:
                f.write(response.content)

            # Obtener el tamaño del archivo PDF en kilobytes
            pdf_size_kb = os.path.getsize(temp_pdf_path) / 1024

            # Extraer el texto del PDF
            pdf_text = pdf_to_text(temp_pdf_path)

            # Generar preguntas basadas en el texto
            questions_string = generate_questions_from_gemini(pdf_text)

            # Eliminar el archivo temporal
            os.remove(temp_pdf_path)

            # Intentar convertir la cadena de respuesta en un JSON
            try:
                if questions_string.startswith('```json'):
                    questions_string = questions_string.replace('```json', '').replace('```', '').strip()

                questions = json.loads(questions_string)

                if not isinstance(questions, dict) or 'questions' not in questions:
                    return JsonResponse({'error': 'Formato de respuesta inválido'}, status=500)

            except json.JSONDecodeError:
                return JsonResponse({'error': 'Error al procesar la respuesta de Gemini como JSON'}, status=500)

            # Calcular el tiempo transcurrido
            elapsed_time = time.time() - start_time
            print(f"Tiempo de generación Gemini: {elapsed_time:.2f} segundos | PDF: {pdf_size_kb:.2f} KB")
            print(questions)
            return JsonResponse(questions)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def process_pdf_claude(request):
    if request.method == 'POST':
        start_time = time.time()  # Empieza el temporizador
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
            temp_pdf_path = 'temp.pdf'
            with open(temp_pdf_path, 'wb') as f:
                f.write(response.content)

            # Obtener el tamaño del archivo PDF en kilobytes
            pdf_size_kb = os.path.getsize(temp_pdf_path) / 1024

            # Extraer el texto del PDF
            pdf_text = pdf_to_text(temp_pdf_path)

            # Generar preguntas basadas en el texto
            questions = generate_questions_from_claude(pdf_text)

            # Eliminar el archivo temporal
            os.remove(temp_pdf_path)

            if isinstance(questions, list) and len(questions) > 0 and hasattr(questions[0], 'text'):
                questions_text = questions[0].text
                try:
                    questions_json = json.loads(questions_text)
                    if isinstance(questions_json, dict) and 'questions' in questions_json:
                        print(questions_json['questions'])
                        elapsed_time = time.time() - start_time
                        print(f"Tiempo de generación Claude: {elapsed_time:.2f} segundos | PDF: {pdf_size_kb:.2f} KB")
                        return JsonResponse({'questions': questions_json['questions']})
                    else:
                        return JsonResponse({'error': 'Formato de respuesta inválido'}, status=500)
                except json.JSONDecodeError:
                    return JsonResponse({'error': 'Error al procesar la respuesta de Claude como JSON'}, status=500)

            return JsonResponse({'error': 'Formato de respuesta inesperado'}, status=500)

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
