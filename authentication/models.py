from django.db import models

# Create your models here.
class CustomUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=40, unique=True)
    user_type = models.CharField(
        max_length=30,
        choices=[
            ('reader', 'Reader'),
            ('author', 'Author'),
            ('administrator', 'Administrator'),
        ],
        default='reader'
    )
    gender = models.CharField(max_length=30)

    def __str__(self):
        return self.username