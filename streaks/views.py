from .serializers import (
    StreakQuerySerializer,
    StreakSerializer,
    BadgeSerializer,
    StreakSaverSerializer,
)
from .models import Badge, UserBadge, StreakSaverUse
from rest_framework import status
from rest_framework.response import Response
from response import CustomJsonRender
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .utils import get_calendar_data
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema


class StreakViewSet(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = (CustomJsonRender,)

    @extend_schema(
        parameters=[StreakQuerySerializer],
        responses={200: StreakSerializer},
    )
    def get(self, request, *args, **kwargs): 
        """
        Send year and month as query params to get the streak data for that month.
        If year and month not sent, it will return the current week's data.
        """
        year = int(request.query_params.get("year", 0))
        month = int(request.query_params.get("month", 0))
        streak = request.user.streak
        calendar_data = get_calendar_data(streak, year, month)
        streak_serializer = StreakSerializer(
            {   
                "current_streak": streak.current_streak,
                "highest_streak": streak.highest_streak,
                "start_date": streak.start_date,
                "calendar": calendar_data,
                "coins_balance": request.user.coins_balance,
                "sign_up_date":request.user.date_joined,
            }
        )
        return Response(streak_serializer.data, status=status.HTTP_200_OK)


class BadgeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    This class contains the badges function
    """

    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

    def get_queryset(self):
        return Badge.objects.all().prefetch_related(
            Prefetch(
                "userbadge_set",
                queryset=UserBadge.objects.filter(user=self.request.user),
                to_attr="userbadges",
            )
        )


class StreakSaverViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    No need to pass anything in arguments or body
    """

    queryset = StreakSaverUse.objects.all()
    serializer_class = StreakSaverSerializer
    permission_classes = [IsAuthenticated]
