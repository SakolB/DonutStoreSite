from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, ProductCategory
from .forms import CreateProductForm

# Create your views here.
def home(request):
    categories = ProductCategory.objects.filter(product__isnull=False).distinct()

    return render(request, 'home/index.html', {'categories' : categories })

def create(request):
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CreateProductForm()
    return render(request, 'home/create.html', {'form' : form})

def cart(request):
    return render(request, "home/cart.html", {})

def about(request):
    return render(request, "home/about.html", {})

@login_required(login_url="/admin")
def edit(request):
    return render(request, "home/edit.html", {})