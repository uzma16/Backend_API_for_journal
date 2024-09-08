from django.urls import path
from .views import UserLogin, UserDetail, LoginWithSocialAuth
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('user', UserDetail)

urlpatterns = [
    path('login', UserLogin.as_view(), name="login POST"),
    path('social_auth', LoginWithSocialAuth.as_view(), name="third party login POST"),
]

urlpatterns += router.urls
