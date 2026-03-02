from django.contrib import admin
from .models import Book, BookRating, ReadingProgress

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'author.first_name')

admin.site.register(BookRating)
admin.site.register(ReadingProgress)