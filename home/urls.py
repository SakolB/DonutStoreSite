from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "home"
urlpatterns = [
    path("", views.home, name="index"),
    path("about/", views.about, name="about"),
    path("cart/", views.cart, name="cart"),
    path("<int:pk>/edit", views.ProductsEditView.as_view(), name="edit"),
    path("<int:pk>/delete", views.ProductsDeleteView.as_view(), name="delete"),
    path("create/", views.ProductsCreateView.as_view(), name="create"),
    path('not_auth/', TemplateView.as_view(template_name='home/fail.html'), name='not_auth'),
    path('login', views.LoginInterfaceView.as_view(), name='login'),
    path('logout', views.LogoutInterfaceView.as_view(), name='logout'),
    path('register', views.SignupView.as_view(), name='signup'),
    path('add_cart/<int:product_id>', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>', views.remove_cart, name='remove_cart'),
    path('clear_cart', views.clear_cart, name='clear_cart'),
    path('profile_create', views.ProfileCreateView.as_view(), name='profile_create'),
    path('profile_edit/<int:pk>', views.ProfileEditView.as_view(), name='profile_edit'),
    path('checkout', views.checkout, name='checkout'),
    path('order_complete',TemplateView.as_view(template_name='home/order_complete.html'), name='order_complete'),
    path('admin_order_view', views.AdminOrderView.as_view(), name='admin_order_view'),
]
