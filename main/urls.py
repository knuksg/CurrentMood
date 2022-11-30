from django.urls import path
from . import views

app_name = "base"

urlpatterns = [
    path("", views.base, name="base"),
    path("test", views.test, name="test"),
]