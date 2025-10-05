from django.views.generic import ListView, DetailView, TemplateView
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        return (
            Product.objects
            .only("id", "name", "image", "price", "description", "updated_at")
            .order_by("-updated_at")
        )


class ContactsView(TemplateView):
    template_name = "contacts.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
