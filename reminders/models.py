from django.db import models
from accounts.models import User
from .constant import RepeatChoices
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.TextField(null=True, blank=True)
    time = models.DateTimeField()
    repeat = models.CharField(max_length=50, choices=RepeatChoices, default='Everyday')
    days_of_week = ArrayField(models.BooleanField(), size=7)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Reminder'