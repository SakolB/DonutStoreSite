from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path("", views.home, name="index"),
    path("edit/", views.edit, name="edit"),
]
