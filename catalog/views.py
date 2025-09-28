from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    return render(request, "home.html")

def contacts(request):
    return render(request, "contacts.html")

def product_detail(request, pk: int):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})