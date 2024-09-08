from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Streak, Badge, UserBadge
from journal.models import Journal
from django.utils import timezone
from .utils import update_streak_function


@receiver(post_save, sender=Journal)
def update_streak(sender, instance, created, **kwargs):
    user = instance.user
    if hasattr(user, "streak"):
        streak = update_streak_function(user.streak)
    else:
        streak = Streak.objects.create(
            user=instance.user,
            current_streak=1,
            highest_streak=1,
            start_date=timezone.now(),
            last_entry_date=timezone.now(),
        )

    return streak


@receiver(post_save, sender=Journal)
def create_badge(sender, instance, created, **kwargs):
    current_streak = (
        instance.user.streak.current_streak if hasattr(instance.user, "streak") else 1
    )
    if current_streak % 7 == 0:
        badge = Badge.objects.filter(streak_length=current_streak).first()
        if (
            badge
            and not UserBadge.objects.filter(
                user_id=instance.user_id, badge_id=badge.id
            ).exists()
        ):
            UserBadge.objects.create(user=instance.user, badge=badge)
