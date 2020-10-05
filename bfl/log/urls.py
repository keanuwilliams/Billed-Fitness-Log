from django.urls import path
from .views import (
    WorkoutListView,
    WorkoutAdminListView,
    WorkoutDetailView,
    WorkoutCreateView,
    WorkoutUpdateView,
    WorkoutDeleteView,
)

urlpatterns = [
    path('', WorkoutListView.as_view(), name='workout-list'),
    path('all/', WorkoutAdminListView.as_view(), name='workout-admin-list'),
    path('new/', WorkoutCreateView.as_view(), name='workout-create'),
    path('<int:pk>/', WorkoutDetailView.as_view(), name='workout-detail'),
    path('<int:pk>/edit/', WorkoutUpdateView.as_view(), name='workout-update'),
    path('<int:pk>/delete/', WorkoutDeleteView.as_view(), name='workout-delete'),
]
