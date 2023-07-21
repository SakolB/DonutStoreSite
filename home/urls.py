from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path("", views.home, name="index"),
    path("about/", views.about, name="about"),
    path("cart/", views.cart, name="cart"),
    path("<int:pk>/edit", views.ProductsEditView.as_view(), name="edit"),
    path("<int:pk>/delete", views.ProductsDeleteView.as_view(), name="delete"),
    path("create/", views.ProductsCreateView.as_view(), name="create"),
]
