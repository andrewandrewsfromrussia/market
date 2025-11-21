from typing import Union

from django.conf import settings
from django.core.cache import cache

from .models import Product


def get_products_by_category(category_id: Union[int, str]):
    """
    Возвращает список (QuerySet) всех продуктов в указанной категории.
    """
    queryset = (
        Product.objects
        .filter(category_id=category_id)
        .only(
            "id",
            "name",
            "image",
            "price",
            "description",
            "updated_at",
            "owner",
            "status",
            "category",
        )
        .order_by("-updated_at")
    )

    if not getattr(settings, "CACHE_ENABLED", False):
        return queryset

    cache_key = f"products_category_{category_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    cache.set(cache_key, queryset, 300)
    return queryset
