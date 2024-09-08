from django.contrib import admin

from .models import Streak, Badge, UserBadge, StreakSaverUse
admin.site.register(Streak)
admin.site.register(Badge)
admin.site.register(UserBadge)
admin.site.register(StreakSaverUse)