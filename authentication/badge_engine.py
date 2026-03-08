from .models import Badge, UserBadge
from books.models import ReadingProgress,ReadingStreak


def process_book_badges(user):

    books_read = ReadingProgress.objects.filter(
        user=user,
        is_finished=True
        ).count()

    badges = Badge.objects.filter(condition_type="books_read")

    for badge in badges:
        if books_read >= badge.condition_value:
            UserBadge.objects.get_or_create(user=user, badge=badge)


def process_streak_badges(user):

    streak = ReadingStreak.objects.get(user=user).highest_streak

    badges = Badge.objects.filter(condition_type="streak")

    for badge in badges:
        if streak >= badge.condition_value:
            UserBadge.objects.get_or_create(user=user, badge=badge)