from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('process_pdf/', views.process_pdf, name='process_pdf'),
]