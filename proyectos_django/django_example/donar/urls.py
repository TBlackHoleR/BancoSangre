from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (
    DonacionCreateView,
    DonacionDeleteView,
    DonacionListView,
    DonacionUpdateView,
)

app_name = 'donar'

urlpatterns = [
    path('list/', login_required(DonacionListView.as_view()), name='list'),
    path('create/', login_required(DonacionCreateView.as_view()), name='create'),
    path(
        'update/<int:pk>/',
        login_required(DonacionUpdateView.as_view()),
        name='update'
    ),
    path(
        'delete/<int:pk>/',
        login_required(DonacionDeleteView.as_view()),
        name='delete'
    ),
]
