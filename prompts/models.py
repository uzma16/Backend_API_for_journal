import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from textblob import TextBlob
from .service import color

# Create your models here


def nameFile(instance, filename):
    return '/'.join(['prompt', str(instance.id), filename])


class Prompt(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    audio = models.FileField(upload_to=nameFile, null=True, blank=True)
    image = models.ImageField(upload_to=nameFile, null=True, blank=True)
    sentiments = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    color =models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'Prompt'


# prevent superuser to delete itself
@receiver(pre_save, sender=Prompt)
def dominant_color(sender, instance, **kwargs):
    if instance.image:
        hue = color(instance.image)
        instance.color = hue
        return instance.color


@receiver(pre_save, sender=Prompt)
def sentiments(sender, instance, **kwargs):
    text = instance.description
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    instance.sentiments = sentiment
    return instance.sentiments
