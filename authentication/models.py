from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    user_type = models.CharField(
        max_length=30,
        choices=[
            ('reader', 'Reader'),
            ('author', 'Author'),
            ('administrator', 'Administrator'),
        ],
        default='reader'
    )
    gender = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username