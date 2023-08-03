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
from decimal import Decimal

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
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = Decimal(0)
    for product_id, item_data in cart.items():
        product = Product.objects.get(id = product_id) 
        if product:
            total_price += Decimal(item_data['price']) * item_data['quantity']
            cart_items.append({'product': product, 'quantity': item_data['quantity']})

    return render(request, 'home/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if not product:
        return redirect('product_not_found')

    cart = request.session.get('cart', {})
    cart_item = cart.get(str(product_id))
    if cart_item:
        # If the product is already in the cart, increment the quantity
        cart_item['quantity'] += 1
    else:
        # If the product is not in the cart, add it with an initial quantity of 1
        cart_item = {'quantity': 1, 'price': float(product.price)}  # Convert Decimal to float
        cart[product_id] = cart_item

    request.session['cart'] = cart
    return redirect('/cart')

def remove_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart_item = cart.get(str(product_id))
    print(cart_item)
    err_msg = ''
    if cart_item:
        if cart_item['quantity'] > 1 :
            cart_item['quantity'] -= 1
        else:
            del cart[str(product_id)]
    else:
        err_msg = 'Items does not exist'
    request.session['cart'] = cart
    return redirect('/cart')

def clear_cart(request):
    cart = request.session.get('cart', {})
    cart.clear()
    request.session['cart'] = cart
    return redirect('/cart')
def about(request):
    return render(request, "home/about.html", {})
