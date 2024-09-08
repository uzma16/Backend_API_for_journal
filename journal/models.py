import uuid
from django.db import models
from django.utils import timezone
from accounts.models import User
from .utils import calculate_audio_length, get_sentiments


def name_file(instance, filename):
    return '/'.join(['media', str(instance.id), filename])

class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    transcript = models.TextField(null=True, blank=True)
    audio = models.FileField(upload_to=name_file, null=True, blank=True)
    image = models.ImageField(upload_to=name_file, null=True, blank=True)
    emotions = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    text_to_speech = models.BooleanField(default=True)
    entry_length = models.FloatField(null=True)

    @property
    def entry_type(self):
        "Returns entry type: 'audio' or 'text'"
        return "audio" if self.audio else "text"

    def save(self, *args, **kwargs):
        if self.description:
            self.entry_length = len(self.description.split())
            self.emotions = get_sentiments(self.description)
        elif self.audio:
            self.entry_length = calculate_audio_length(self.audio)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'Journal'

    def __str__(self):
        return str(self.user)
