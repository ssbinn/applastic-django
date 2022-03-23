from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("apps/", include("apps.urls", namespace="apps")),
]
# apps/ 뭐여이거
