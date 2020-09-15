"""
Billed Fitness Log URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/

"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('', user_views.landing, name='landing'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login, name='login'),
]
