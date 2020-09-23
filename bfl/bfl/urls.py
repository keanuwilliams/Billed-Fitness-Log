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
    path('user-home/', user_views.user_home, name='user_home'),
    path('profile/', user_views.profile, name='profile'),
    path('edit-profile/', user_views.edit_profile, name='edit_profile'),
    path('settings/', user_views.settings, name='settings'),
    path('change-password/', user_views.change_password, name='change_password'),
    path('login/', user_views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
