from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.caa, name='create-an-account'),
    path('login/', views.login, name='login')
]
