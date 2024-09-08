from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('prompts', PromptDetail)

urlpatterns = router.urls
