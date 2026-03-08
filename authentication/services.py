from .badge_engine import process_book_badges, process_streak_badges


class BadgeService:

    @staticmethod
    def handle_book_completed(user):
        process_book_badges(user)

    @staticmethod
    def handle_streak_updated(user):
        process_streak_badges(user)