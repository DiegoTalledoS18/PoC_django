from django.http import JsonResponse
import json
from django.shortcuts import render
from pymupdf import message
from django.views.decorators.csrf import csrf_exempt


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
