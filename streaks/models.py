from django.db import models
from django.utils import timezone
import uuid
from accounts.models import User


def name_file(instance, filename):
    return "/".join(["badge", str(instance.label), filename])


class Streak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    current_streak = models.IntegerField(default=0, null=True)  # Current streak length
    highest_streak = models.IntegerField(default=0, null=True, blank=True)
    start_date = models.DateField(default=timezone.now)  # Start date of current streak
    updated_at = models.DateTimeField(auto_now=True)
    last_entry_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "streak_new"

    def __str__(self):
        return self.user.username


class StreakSaverUse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "streak_saver_use"

    def __str__(self):
        return self.user.username


class Badge(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to=name_file, null=True, blank=True)
    streak_length = models.IntegerField(unique=True)  # In days
    users = models.ManyToManyField(User, through="UserBadge", related_name="badges")

    class Meta:
        db_table = "streak_badge"
        ordering = ["streak_length"]

    def __str__(self):
        return self.label


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "streak_user_badge"

    def __str__(self):
        return f"{self.user.username} - {self.badge}"
