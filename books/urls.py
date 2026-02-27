from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_book, name='upload_book'),
    path('my-books/', views.author_books, name='author_books'),
    path('list/', views.book_list, name='book_list'),

    #  STREAM & READER MUST COME BEFORE <slug>
    path('reader/<slug:slug>/', views.book_reader, name='book_reader'),
    path('stream/<slug:slug>/', views.stream_pdf, name='stream_pdf'),

    
    path('<slug:slug>/', views.book_detail, name='book_detail'),
    path('edit/<slug:slug>/',views.edit_book,name='edit_book'),
    path('delete/<slug:slug>/',views.delete_book,name='delete_book'),
    path('save-progress/<slug:slug>/', views.save_progress, name='save_progress'),
]