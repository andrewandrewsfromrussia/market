from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"         # ← обязательно home.html
    context_object_name = "products"

    def get_queryset(self):
        return (Product.objects
                .only("id","name","image","price","description","updated_at","owner")
                .order_by("-updated_at"))

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner_id == self.request.user.id

class ContactsView(TemplateView):  # ⬅️ добавь обратно
    template_name = "catalog/contacts.html"

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ["name", "category", "description", "price", "image"]
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Product
    fields = ["name", "category", "description", "price", "image"]
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

class ProductDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")
