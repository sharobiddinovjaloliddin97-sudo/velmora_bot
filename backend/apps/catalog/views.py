from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .services import CatalogService
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrEmployee


#ListAPIView -> Returns a list of objects. already knows how to handle a GET request returning a list.
class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer

    # Gets data from the service. built-in
    def get_queryset(self):
        return CatalogService.get_categories()


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    # Enables filtering, search, and ordering for this view.
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "category",
        "material",
    ]

    search_fields = [
        "name",
        "description",
        "material",
    ]

    ordering_fields = [
        "price",
        "created_at",
        "name",
    ]

    def get_queryset(self):
        return CatalogService.get_products()

# RetrieveAPIView is a built-in DRF view that returns a single object based on a unique field (such as id or slug).
class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return CatalogService.get_products()

# CreateAPIView - DRF automatically builds the HTML form from the serializer.
class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminOrEmployee,
    ]
    # Built-in method called after validation and before saving.
    def perform_create(self, serializer):
        #Creates a new Product in the database.
        serializer.save()


# UpdateAPIView - DRF generic view for updating an existing object.
class ProductUpdateView(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminOrEmployee,
    ]
    lookup_field = "slug"

    #Returns the products that can be updated.
    def get_queryset(self):
        return CatalogService.get_products()

    def perform_update(self, serializer):
        serializer.save()

# DestroyAPIView → Deletes an object.
class ProductDeleteView(generics.DestroyAPIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminOrEmployee,
    ]
    lookup_field = "slug"

    def get_queryset(self):
        return CatalogService.get_products()