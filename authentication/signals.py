from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from books.models import ReadingStreak
from .events import book_completed,streak_updated
from .services import BadgeService

@receiver(post_save, sender=CustomUser)
def create_user_streak(sender, instance, created, **kwargs):
    if created:
        ReadingStreak.objects.create(user=instance)


@receiver(book_completed)
def book_completed_listener(sender, user, **kwargs):

    BadgeService.handle_book_completed(user)


@receiver(streak_updated)
def streak_updated_listener(sender, user, **kwargs):

    BadgeService.handle_streak_updated(user)