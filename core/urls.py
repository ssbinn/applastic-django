from django.urls import path
from apps import views as app_views

app_name = "core"

urlpatterns = [
    path("", app_views.all_apps, name="home"),
]  # home > apps(?) 변경해 빨리 제발
