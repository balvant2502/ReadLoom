from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from books.models import ReadingStreak

@receiver(post_save, sender=CustomUser)
def create_user_streak(sender, instance, created, **kwargs):
    if created:
        ReadingStreak.objects.create(user=instance)