from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    products = (
        Product.objects
        .only("id", "name", "image", "price", "description", "updated_at")
        .order_by("-updated_at")
    )
    return render(request, "catalog/home.html", {"products": products})

def contacts(request):
    return render(request, "contacts.html")

def product_detail(request, pk: int):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})
