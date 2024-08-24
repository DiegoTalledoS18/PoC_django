from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('process_pdf_gpt/', views.process_pdf_gpt, name='process_pdf_gpt'),
    path('process_pdf_gemini/', views.process_pdf_gemini, name='process_pdf_gemini'),
    path('process_pdf_claude/', views.process_pdf_claude, name='process_pdf_claude'),
]