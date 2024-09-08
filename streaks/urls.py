from django.urls import path
from .views import StreakViewSet, BadgeViewSet, StreakSaverViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("use-saver", StreakSaverViewSet)
router.register("badges", BadgeViewSet)

urlpatterns = [
    path("", StreakViewSet.as_view(), name="streaks GET"),
]
urlpatterns += router.urls
