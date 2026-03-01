from django.db import models
from authentication.models import CustomUser 
from books.models import Book

class Shelf(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="shelves"
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')  # no duplicate shelf names per user

    def __str__(self):
        return f"{self.name} ({self.user})"


class ShelfBook(models.Model):
    shelf = models.ForeignKey(
        Shelf,
        on_delete=models.CASCADE,
        related_name="shelf_books"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('shelf', 'book')