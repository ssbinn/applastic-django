from django.urls import URLPattern, path
from . import views

app_name = "apps"

urlpatterns = [
    path("", views.home, name="home"),
    path("apps/", views.all_apps, name="apps"),
    path("tag/<str:tag>/", views.tag, name="tag"),
    path("search/", views.search, name="search"),
    path("apps/<int:id>/", views.app_detail, name="detail"),
    path("analysis/", views.analysis, name="analysis"),
]  # url dispatcher
