import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import datetime
from django.utils import timezone
from django.dispatch import receiver
from .constant import GENDER_CHOICES
from django.db.models.signals import pre_delete
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password
from django.contrib.postgres.fields import ArrayField


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, phone, password, **kwargs):
        user = self.model(phone=phone, is_staff=True, is_superuser=True, is_admin=True, **kwargs)
        user.password = make_password(password)
        user.save()
        return user


def nameFile(instance, filename):
    return '/'.join(['images/profile', str(instance.username), filename])


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=50, unique=True, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    picture = models.ImageField(upload_to=nameFile, null=True, blank=True)
    zodiac_sign = models.CharField(max_length=50, blank=True, null=True)
    fcm_token = ArrayField(models.CharField(max_length=1000), null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    user_timezone = models.CharField(max_length=50, null=True, blank=True)
    user_timezone_name = models.CharField(max_length=150, null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    coins_balance = models.IntegerField(default=0)

    objects = AccountManager()

    class Meta:
        db_table = 'User'
        indexes = [
            models.Index(fields=[
                'username'
            ])
        ]

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.username


# prevent superuser to delete itself
@receiver(pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    if instance.is_superuser:
        raise PermissionDenied
