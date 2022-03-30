from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("apps/", include("apps.urls", namespace="apps")),
    path("admin/", admin.site.urls),
]
