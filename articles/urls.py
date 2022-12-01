from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.private, name="private"),
    path("index", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/update/", views.update, name="update"),
    path("locations", views.location_get, name="locations"),
    path("public/", views.public, name="public"),
    path("test/", views.test, name="test"),
]
