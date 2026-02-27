from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_book, name='upload_book'),
    path('my-books/', views.author_books, name='author_books'),
    path('list/', views.book_list, name='book_list'),
    path('<slug:slug>/', views.book_detail, name='book_detail'),
]