from django.urls import URLPattern, path
from . import views

app_name = "apps"

urlpatterns = [path("<int:pk>", views.app_detail, name="detail")]
