from django.db import models
from django.utils.text import slugify
from authentication.models import CustomUser


class Book(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    CATEGORY_CHOICES = (
        ('science', 'Science & Technology'),
        ('philosophy', 'Philosophy'),
        ('psychology', 'Psychology'),
        ('motivational', 'Motivational'),
        ('fiction', 'Fiction'),
        ('biography', 'Biography'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField()

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='books'
    )

    book_file = models.FileField(upload_to='books/')
    cover_image = models.ImageField(upload_to='covers/')

    total_pages = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    is_featured = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)

    reads = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class BookRead(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')