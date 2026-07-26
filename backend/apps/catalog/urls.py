from django.urls import path

from .views import (
    CategoryListView,
    ProductDetailView,
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,
)

urlpatterns = [
    path(
        "categories/",
        CategoryListView.as_view(),
        name="category-list",
    ),
    path(
        "products/",
        ProductListView.as_view(),
        name="product-list",
    ),
    path(
        "products/create/",
        ProductCreateView.as_view(),
        name="product-create",
    ),
    path(
        "products/<slug:slug>/update/",
        ProductUpdateView.as_view(),
        name="product-update",
    ),
    path(
        "products/<slug:slug>/delete/",
        ProductDeleteView.as_view(),
        name="product-delete",
    ),
    path(
        "products/<slug:slug>/",
        ProductDetailView.as_view(),
        name="product-detail",
    ),
]