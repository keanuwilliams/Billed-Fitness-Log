"""
Billed Fitness Log URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/

"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', user_views.landing, name='landing'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('home/', user_views.user_home, name='user-home'),
    path('usr/<str:username>/', user_views.profile, name='profile'),
    path('usr/<str:username>/edit/', user_views.edit_profile, name='edit-profile'),
    path('settings/', user_views.settings, name='settings'),
    path('deactivate/', user_views.deactivate, name='deactivate'),
    path('change-password/', user_views.change_password, name='change-password'),
    path('login/', user_views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('sessions/', include('log.urls')),
]

if settings.DEBUG: # For development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
