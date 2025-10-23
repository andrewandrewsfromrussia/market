from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import ProductListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", ProductListView.as_view(), name="home"),
    path("catalog/", include("catalog.urls", namespace="catalog")),
    path("blogs/", include("blogs.urls", namespace="blogs")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
