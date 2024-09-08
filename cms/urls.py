from .views import CoindetailViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("coindetail", CoindetailViewSet)
urlpatterns = router.urls
