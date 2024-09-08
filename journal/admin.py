from django.contrib import admin
from .models import *


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)
