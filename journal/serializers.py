from django.utils import timezone
from .models import Journal
from rest_framework import serializers
from .service import calculate_coins
from streaks.models import UserBadge, Badge
from streaks.serializers import BadgeSerializer


class JournalSerializer(serializers.ModelSerializer):
    badge_earned = serializers.SerializerMethodField()
    sentiments = serializers.IntegerField(source="emotions", read_only=True)
    current_streak = serializers.SerializerMethodField(read_only=True)
    coins = serializers.SerializerMethodField(read_only=True)

    # Adding is_created to check if the journal is created or not and then sending coins, badge_earned only when journal is created
    def __init__(self, *args, **kwargs):
        super(JournalSerializer, self).__init__(*args, **kwargs)
        self.is_created = False

    def create(self, validated_data):
        self.is_created = True
        journal = Journal.objects.create(
            user=self.context.get("request").user, **validated_data
        )
        return journal

    class Meta:
        model = Journal
        fields = [
            "id",
            "title",
            "description",
            "transcript",
            "audio",
            "image",
            "created_at",
            "current_streak",
            "sentiments",
            "coins",
            "badge_earned",
        ]

    def get_current_streak(self, instance):
        user = instance.user
        return user.streak.current_streak if hasattr(user, "streak") else 1

    def get_coins(self, instance):
        if not self.is_created:
            return 0
        entry_type = instance.entry_type
        entry_length = instance.entry_length
        coins = calculate_coins(entry_type, entry_length)
        return coins

    def get_badge_earned(self, instance):
        if not self.is_created:
            return None
        user = self.context["request"].user
        current_streak = user.streak.current_streak
        badge = Badge.objects.filter(
            streak_length=current_streak,
        ).first()
        if (
            badge
            and UserBadge.objects.filter(
                user=user, badge=badge, created_at__date=timezone.now().date()
            ).exists()
            and user.journal_set.filter(created_at__date=timezone.now().date()).count()
            == 1
        ):
            return BadgeSerializer(badge).data
        return None
