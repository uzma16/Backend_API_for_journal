from .views import ReminderDetail
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', ReminderDetail)

urlpatterns = router.urls
