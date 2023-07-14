from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, 'home/index.html', {})

def cart(request):
    return

@login_required(login_url="/admin")
def edit(request):
    return render(request, "home/edit.html", {})