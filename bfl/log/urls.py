from django.urls import path
from . import views
from .views import (
    WorkoutCreateView,
    WorkoutUpdateView,
    WorkoutDeleteView,
)

urlpatterns = [
    path('', views.my_workouts, name='my-workouts'),
    path('all/', views.all_workouts_admin, name='all-workouts-admin'),
    path('new/', WorkoutCreateView.as_view(), name='add-workout'),
    path('<int:pk>/', views.workout_detail, name='workout-detail'),
    path('<int:pk>/edit/', WorkoutUpdateView.as_view(), name='workout-update'),
    path('<int:pk>/delete/', WorkoutDeleteView.as_view(), name='workout-delete'),
]
