from typing import Any, cast

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from .models import Product, Category
from .services import get_products_by_category
from django.conf import settings
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset =  (
            Product.objects
            .only(
                "id",
                "name",
                "image",
                "price",
                "description",
                "updated_at",
                "owner",
                "status",
            )
            .order_by("-updated_at")
        )

        if not getattr(settings, "CACHE_ENABLED", False):
            return queryset

        cache_key = "products_list"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        cache.set(cache_key, queryset, 300)
        return queryset


class CategoryProductListView(ListView):
    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")
        context["category"] = Category.objects.only("id", "name").get(pk=category_id)
        return context


class OwnerRequiredMixin(UserPassesTestMixin):
    """
    Пускает владельца продукта ИЛИ модератора/пользователя с нужными правами.
    Отдаёт 403 вместо редиректа.
    """

    raise_exception = True

    def _get_target_object(self) -> Product:
        """
        Достаём объект безопасно:
        1) если self.object уже есть, используем его;
        2) иначе пробуем super().get_object();
        3) в крайнем случае берём по pk из kwargs.
        """
        obj = getattr(self, "object", None)
        if obj is not None:
            return obj

        get_obj = getattr(super(), "get_object", None)
        if callable(get_obj):
            return get_obj()

        pk = self.kwargs.get("pk")
        if pk is not None:
            return Product.objects.get(pk=pk)

        raise PermissionDenied("Эта операция требует объект продукта.")

    def test_func(self) -> bool:
        request: Any = getattr(self, "request", None)
        if request is None:
            return False

        user = request.user
        if not user.is_authenticated:
            return False

        obj: Product = cast(Product, self._get_target_object())

        # 1) владелец
        if obj.owner_id == user.id:
            return True

        # 2) группа модераторов
        if user.groups.filter(name="Модератор продуктов").exists():
            return True

        # 3) явные права
        if (
            user.has_perm("catalog.delete_product")
            or user.has_perm("catalog.can_unpublish_product")
        ):
            return True

        return False


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"


@method_decorator(cache_page(300), name="dispatch")
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


class ProductUnpublishView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Снимает продукт с публикации (status -> draft).
    Доступно модераторам или тем, у кого есть право can_unpublish_product.
    """

    success_url = reverse_lazy("catalog:home")
    raise_exception = True  # 403 вместо редиректа

    def test_func(self) -> bool:
        request: Any = getattr(self, "request", None)
        if request is None or not request.user.is_authenticated:
            return False

        user = request.user
        if user.groups.filter(name="Модератор продуктов").exists():
            return True

        return user.has_perm("catalog.can_unpublish_product")

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs["pk"])
        # меняем статус только если уже опубликован; тихо игнорим прочее
        if product.status != Product.PublishStatus.DRAFT:
            product.status = Product.PublishStatus.DRAFT
            product.save(update_fields=["status"])
        return_url = request.POST.get("next") or self.success_url
        return self._redirect(return_url)

    def _redirect(self, url):
        from django.shortcuts import redirect
        return redirect(url)
