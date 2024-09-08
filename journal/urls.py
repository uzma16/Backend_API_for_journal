from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', JournalDetail)

urlpatterns = router.urls
