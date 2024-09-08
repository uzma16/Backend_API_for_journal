from django.dispatch import receiver
from django.db.models.signals import post_save
from journal.service import calculate_coins
from journal.models import Journal
from streaks.models import StreakSaverUse


@receiver(post_save, sender=Journal)
def update_coins(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        coins = calculate_coins(instance.entry_type, instance.entry_length)
        if coins > 0:
            user.coins_balance += coins
            user.save()

@receiver(post_save, sender=StreakSaverUse)
def deduct_coins(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        coins_to_deduct = 50
        user.coins_balance -= coins_to_deduct
        user.save()