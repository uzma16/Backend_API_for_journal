from rest_framework import serializers
from .models import Badge, Streak, StreakSaverUse
from django.utils import timezone
from datetime import timedelta
from .utils import get_streak_saving_date


class BadgeSerializer(serializers.ModelSerializer):
    earned_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Badge
        fields = ["label", "logo", "streak_length", "earned_at"]

    def get_earned_at(self, instance):
        if not hasattr(instance, "userbadges"):
            # If Badge Serializer is accessed from Journal Serializer
            return timezone.now().date()
        return (
            instance.userbadges[0].created_at if len(instance.userbadges) > 0 else None
        )


class DaySerializer(serializers.Serializer):
    date = serializers.DateField(read_only=True)
    day = serializers.IntegerField(read_only=True)
    in_current_streak = serializers.BooleanField(read_only=True)
    is_frozen = serializers.BooleanField(read_only=True)
    entry_count = serializers.IntegerField(read_only=True)
    streak_saver_used = serializers.BooleanField(default=False, read_only=True)
    badge_earned = BadgeSerializer(read_only=True)


class CalendarSerializer(serializers.Serializer):
    current_date = serializers.DateField(read_only=True)
    use_saver_by = serializers.DateField(read_only=True)
    can_use_saver_after = serializers.DateField(read_only=True)
    days_data = DaySerializer(many=True, read_only=True)


class StreakQuerySerializer(serializers.Serializer):
    year = serializers.IntegerField(
        required=False,
        help_text="year in YYYY format",
    )
    month = serializers.IntegerField(
        required=False,
        help_text="month value between 1 to 12",
    )


class StreakSerializer(serializers.ModelSerializer):
    calendar = CalendarSerializer(read_only=True)
    coins_balance = serializers.IntegerField(read_only=True)
    sign_up_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Streak
        fields = [
            "coins_balance",
            "sign_up_date",
            "current_streak",
            "highest_streak",
            "start_date",
            "calendar",
        ]


class StreakSaverSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreakSaverUse
        fields = "__all__"
        extra_kwargs = {"user": {"required": False}, "created_at": {"required": False}}
        read_only_fields = ["user", "created_at"]

    def validate(self, data):
        user = self.context["request"].user
        streak = user.streak
        seven_days_ago = timezone.now().date() - timedelta(days=6)

        if streak.current_streak <= 0:
            raise serializers.ValidationError("No streak progress to save.")
        elif StreakSaverUse.objects.filter(
            user=user, created_at__date__gte=seven_days_ago
        ).exists():
            raise serializers.ValidationError(
                "Streak saver can be used only once in a week."
            )

        created_at = get_streak_saving_date(streak)
        if not created_at:
            raise serializers.ValidationError(
                "Either streak saver is not required or it can not be used right now."
            )

        data["user"] = user
        data["created_at"] = created_at
        return data
