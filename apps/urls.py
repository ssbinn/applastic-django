from django.urls import URLPattern, path
from . import views

app_name = "apps"

urlpatterns = [path("<int:id>", views.app_detail, name="detail")]  # url dispatcher
