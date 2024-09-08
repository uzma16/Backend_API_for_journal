"""lby_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
) 


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("cms/", include("cms.urls")),
    path("journals/", include("journal.urls")),
    path("reminders/", include("reminders.urls")),
    path("streak/", include("streaks.urls")),
    path("", include("prompts.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "doc/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Mindfulness"
admin.site.site_title = "Mindfulness"
admin.site.index_title = "Mindfulness"
