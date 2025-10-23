from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm

# Список продуктов
class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    def get_queryset(self):
        return Product.objects.only("id", "name", "image", "price", "description", "updated_at").order_by("-updated_at")

# Детальная страница
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

# Контакты
class ContactsView(TemplateView):
    template_name = "contacts.html"

# Создание продукта
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

# Редактирование продукта
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

# Удаление продукта
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")
