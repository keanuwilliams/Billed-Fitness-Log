from django.urls import path
from .views import (
    SessionListView,
    SessionAdminListView,
    SessionDetailView,
    SessionCreateView,
    SessionUpdateView,
    SessionDeleteView,
)
from . import views

urlpatterns = [
    path('', SessionListView.as_view(), name='session-list'),
    path('all/', SessionAdminListView.as_view(), name='session-admin-list'),
    path('new/', SessionCreateView.as_view(), name='session-create'),
    path('<int:pk>/', SessionDetailView.as_view(), name='session-detail'),
    path('<int:pk>/edit/', SessionUpdateView.as_view(), name='session-update'),
    path('<int:pk>/delete/', SessionDeleteView.as_view(), name='session-delete'),
]
