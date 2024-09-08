from rest_framework import serializers
from .models import Reminder
import pytz

class ReminderSerializer(serializers.ModelSerializer):
    local_time = serializers.SerializerMethodField()

    def create(self, validated_data):
        reminder = Reminder.objects.create(user=self.context.get('request').user, **validated_data)
        return reminder

    class Meta:
        model = Reminder
        fields = ['id', 'time', 'label', 'repeat', 'days_of_week', 'is_active', 'local_time']

    def get_local_time(self, instance):
        local_time = instance.time
        zone = pytz.timezone(instance.user.user_timezone_name)
        user_timezone = local_time.astimezone(zone)
        return user_timezone
