from django.urls import URLPattern, path
from . import views

app_name = "apps"

urlpatterns = [
    path("<str:id>", views.app_detail, name="detail")
]  # url dispatcher 다시 공부하기
