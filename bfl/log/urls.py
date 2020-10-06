from django.urls import path
from . import views
from .views import (
    CWorkoutCreateView,
    RWorkoutCreateView,
    WLWorkoutCreateView,
    CWorkoutUpdateView,
    RWorkoutUpdateView,
    WLWorkoutUpdateView,
    CWorkoutDeleteView,
    RWorkoutDeleteView,
    WLWorkoutDeleteView,
)

urlpatterns = [
    path('', views.my_workouts, name='my-workouts'),
    path('all/', views.all_workouts_admin, name='all-workouts-admin'),
    path('select/', views.select_workouts, name='workout-select'),
    path('cardio/new/', CWorkoutCreateView.as_view(), name='add-c-workout'),
    path('resistance/new/', RWorkoutCreateView.as_view(), name='add-r-workout'),
    path('weightlifting/new/', WLWorkoutCreateView.as_view(), name='add-wl-workout'),
    path('cardio/<int:pk>/', views.c_workout_detail, name='c-workout-detail'),
    path('resistance/<int:pk>/', views.r_workout_detail, name='r-workout-detail'),
    path('weightlifting/<int:pk>/', views.wl_workout_detail, name='wl-workout-detail'),
    path('cardio/<int:pk>/edit/', CWorkoutUpdateView.as_view(), name='edit-c-workout'),
    path('resistance/<int:pk>/edit/', RWorkoutUpdateView.as_view(), name='edit-r-workout'),
    path('weightlifting/<int:pk>/edit/', WLWorkoutUpdateView.as_view(), name='edit-wl-workout'),
    path('cardio/<int:pk>/delete/', CWorkoutDeleteView.as_view(), name='delete-c-workout'),
    path('resistance/<int:pk>/delete/', RWorkoutDeleteView.as_view(), name='delete-r-workout'),
    path('weightlifting/<int:pk>/delete/', WLWorkoutDeleteView.as_view(), name='delete-wl-workout'),
]
