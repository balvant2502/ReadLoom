from django.urls import path
from . import views

urlpatterns = [
    path('shelves/', views.shelves_view, name='shelves'),
]
