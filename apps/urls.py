from django.urls import URLPattern, path
from . import views

app_name = "apps"

urlpatterns = [
    path("<str:id>", views.app_detail, name="detail"),
    path("search/", views.search, name="search"),
]  # url dispatcher
