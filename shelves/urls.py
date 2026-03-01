from django.urls import path
from .views import shelves_page, create_shelf, shelf_books, add_to_shelf_page, delete_shelf

urlpatterns = [
    path('shelfhome/', shelves_page, name='shelves'),
    path('create/', create_shelf, name='create_shelf'),
    path('<int:shelf_id>/books/', shelf_books, name='shelf_books'),
    path('add-to-shelf/<slug:slug>/', add_to_shelf_page, name='add_to_shelf'),
    path('<int:shelf_id>/delete/', delete_shelf, name='delete_shelf'),
]
