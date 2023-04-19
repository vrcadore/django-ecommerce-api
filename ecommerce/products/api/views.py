from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from ecommerce.products.api.serializers import (
    AttributeDetailSerializer,
    AttributeSerializer,
    BrandDetailSerializer,
    BrandSerializer,
    CategoryDetailSerializer,
    CategorySerializer,
    ProductDetailSerializer,
    ProductImageDetailSerializer,
    ProductImageSerializer,
    ProductLineDetailSerializer,
    ProductLineSerializer,
    ProductSerializer,
)
from ecommerce.products.models import (
    Attribute,
    Brand,
    Category,
    Product,
    ProductImage,
    ProductLine,
)
from ecommerce.utils.permissions import IsAuthenticatedReadOnly, IsOwnerOrReadOnly


class BrandViewSet(ModelViewSet):
    """
    A viewset for viewing and editing brand instances.
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser | IsAuthenticatedReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BrandDetailSerializer
        return BrandSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(updated_by=self.request.user)


class CategoryViewSet(ModelViewSet):
    """
    A viewset for viewing and editing category instances.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser | IsAuthenticatedReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CategoryDetailSerializer
        return CategorySerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(updated_by=self.request.user)


class AttributeViewSet(ModelViewSet):
    """
    A viewset for viewing and editing atributes instances.
    """

    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [IsAdminUser | IsAuthenticatedReadOnly]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AttributeDetailSerializer
        return AttributeSerializer


class ProductViewSet(ModelViewSet):
    """
    A viewset for viewing and editing product lines instances.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser | IsOwnerOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(updated_by=self.request.user)


class ProductLineViewSet(ModelViewSet):
    """
    A viewset for viewing and editing product images instances.
    """

    queryset = ProductLine.objects.all()
    serializer_class = ProductLineSerializer
    permission_classes = [IsAdminUser | IsOwnerOrReadOnly]
    lookup_field = "sku"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductLineDetailSerializer
        return ProductLineSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(updated_by=self.request.user)


class ProductImageViewSet(ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser | IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductImageDetailSerializer
        return ProductImageSerializer
