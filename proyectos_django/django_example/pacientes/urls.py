from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (
    PacientesCreateView,
    PacientesDeleteView,
    PacientesListView,
    PacientesUpdateView,
)

app_name = 'pacientes'

urlpatterns = [
    path('list/', login_required(PacientesListView.as_view()), name='list'),
    path('create/', login_required(PacientesCreateView.as_view()), name='create'),
    path(
        'update/<int:pk>/',
        login_required(PacientesUpdateView.as_view()),
        name='update'
    ),
    path(
        'delete/<int:pk>/',
        login_required(PacientesDeleteView.as_view()),
        name='delete'
    ),
]
