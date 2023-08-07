from typing import Optional
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Product, ProductCategory, Profile, Order, ProductOrder
from .forms import ProductForm, ProfileForm
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
    success_url = '/profile_create'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        self.request.session['created_user_id'] = user.id
        print(self.request.session.get('created_user_id', None))
        return response
        
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

class ProfileCreateView(UserPassesTestMixin, CreateView):
    form_class = ProfileForm
    success_url = '/'
    template_name = 'home/profileform.html'
    extra_context = {'action' : 'Create'}
    def test_func(self):
        return 'created_user_id' in self.request.session
    def handle_no_permission(self):
        return redirect('/not_auth')
    def form_valid(self, form):
        print(self.request.session.get('created_user_id', None))
        user_id = self.request.session.get('created_user_id', None)
        if not user_id:
            return redirect('index')
        user = get_object_or_404(User, id=user_id)
        profile = form.save(commit=False)
        profile.user = user
        profile.save()  
        self.request.session.pop('created_user_id', None)      
        return super().form_valid(form)


class ProfileEditView(UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = '/'
    template_name = 'home/profileform.html'
    extra_context = {'action': 'Edit'}
    def test_func(self):
        profile = self.get_object()
        return is_login(self.request.user) and self.request.user == profile.user
    def handle_no_permission(self):
        return redirect('/not_auth')
    def get_queryset(self):
        # Limit the queryset to profiles that belong to the currently logged-in user
        return Profile.objects.filter(user=self.request.user)

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
        
def checkout(request):
    cart = request.session.get('cart', {})
    total_price = Decimal(0)
    order = Order.objects.create()
    order.special_instruction="blank"
    for product_id, item_data in cart.items():
        product = Product.objects.get(id = product_id) 
        if product:
            total_price += Decimal(item_data['price']) * item_data['quantity']
            ProductOrder.objects.create(product=product, order=order, quantity=item_data['quantity'])
    order.total_price = total_price
    print(order.total_price)
    user = request.user
    if is_login(user):
        profile = get_object_or_404(Profile, user=user)
        order.profile = profile
    order.save()
    return redirect('/order_complete')
    
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
