from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateView, ProductDeleteView,
    ContactsView, ProductUnpublishView
)

app_name = "catalog"

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path('products/', ProductListView.as_view(), name='product_list'),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("products/<int:pk>/unpublish/", ProductUnpublishView.as_view(), name="product_unpublish"),
]
