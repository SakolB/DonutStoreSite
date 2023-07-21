from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, ProductCategory
from .forms import ProductForm
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import DeleteView

# Create your views here.
def home(request):
    categories = ProductCategory.objects.filter(product__isnull=False).distinct()

    return render(request, 'home/index.html', {'categories' : categories })

class ProductsCreateView(CreateView):
    model = Product
    success_url = '/'
    form_class = ProductForm
    template_name = 'home/form.html'

class ProductsEditView(UpdateView):
    model = Product
    success_url ="/"
    form_class = ProductForm
    template_name = 'home/form.html'

class ProductsDeleteView(DeleteView):
    model = Product
    success_url = "/"
    template_name = 'home/delete.html'
    
def cart(request):
    return render(request, "home/cart.html", {})

def about(request):
    return render(request, "home/about.html", {})

@login_required(login_url="/admin")
def edit(request):
    return render(request, "home/edit.html", {})