from django.contrib import admin
from .models import Reminder

# Register your models here.
@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('user', 'time')
    list_filter = ('time',)
