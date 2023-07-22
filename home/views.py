from typing import Optional
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Product, ProductCategory
from .forms import ProductForm
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm


def is_admin(user):
    return user.is_authenticated and user.is_superuser

def is_notlogin(user):
    return not user.is_authenticated

def is_login(user):
    return user.is_authenticated

# Create your views here.
def home(request):
    categories = ProductCategory.objects.filter(product__isnull=False).distinct()

    return render(request, 'home/index.html', {'categories' : categories })

class SignupView(UserPassesTestMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'home/register.html'
    success_url = '/'

    def test_func(self):
        return is_notlogin(self.request.user)
    
    def handle_no_permission(self):
        return redirect('/')
    
class LoginInterfaceView(UserPassesTestMixin, LoginView):
    template_name='home/login.html'

    def test_func(self):
        return is_notlogin(self.request.user)
    
    def handle_no_permission(self):
        return redirect('/')

class LogoutInterfaceView(UserPassesTestMixin, LogoutView):
    template_name='home/logout.html'

    def test_func(self):
        return is_login(self.request.user)
    
    def handle_no_permission(self):
        return redirect('/login')

class ProductsCreateView(UserPassesTestMixin, CreateView):
    model = Product
    success_url = '/'
    form_class = ProductForm
    template_name = 'home/form.html'

    def test_func(self):
        return is_admin(self.request.user)
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('/not_auth')
        else:
            return redirect('/login')

#products_create_view = create_admin_required(ProductsCreateView.as_view())
class ProductsEditView(UserPassesTestMixin, UpdateView):
    model = Product
    success_url ="/"
    form_class = ProductForm
    template_name = 'home/form.html'

    def test_func(self):
        return is_admin(self.request.user)
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('/not_auth')
        else:
            return redirect('/login')

class ProductsDeleteView(UserPassesTestMixin, DeleteView):
    model = Product
    success_url = "/"
    template_name = 'home/delete.html'

    def test_func(self):
        return is_admin(self.request.user)
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('/not_auth')
        else:
            return redirect('/login')
    
def cart(request):
    return render(request, "home/cart.html", {})

def about(request):
    return render(request, "home/about.html", {})
