from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from ecommerce.products.api.serializers import (
    AttributeDetailSerializer,
    AttributeSerializer,
    BrandDetailSerializer,
    BrandSerializer,
    CategoryDetailSerializer,
    CategorySerializer,
    ProductDetailSerializer,
    ProductEditSerializer,
    ProductImageDetailSerializer,
    ProductImageEditSerializer,
    ProductImageSerializer,
    ProductLineDetailSerializer,
    ProductLineEditSerializer,
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
from ecommerce.utils.permissions import IsAuthenticatedReadOnly, IsOwner


class BrandViewSet(ModelViewSet):
    """
    A viewset for viewing and editing brand instances.
    """

    queryset = Brand.objects.all()
    serializer_class = BrandDetailSerializer
    permission_classes = [IsAdminUser | IsAuthenticatedReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BrandSerializer
        return BrandDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.updated_by = self.request.user
        instance.save()


class CategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    A viewset for viewing and editing category instances.
    """

    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAuthenticatedReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return CategorySerializer
        return CategoryDetailSerializer


class AttributeViewSet(ModelViewSet):
    """
    A viewset for viewing and editing atributes instances.
    """

    queryset = Attribute.objects.all()
    serializer_class = AttributeDetailSerializer
    add_serializer_class = AttributeSerializer
    permission_classes = [IsAdminUser | IsAuthenticatedReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return AttributeSerializer
        return AttributeDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.updated_by = self.request.user
        instance.save()


class ProductViewSet(ModelViewSet):
    """
    A viewset for viewing and editing product lines instances.
    """

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminUser | IsOwner | IsAuthenticatedReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ProductSerializer
        if self.action in ["create", "update", "partial_update"]:
            return ProductEditSerializer
        return ProductDetailSerializer

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
            created_by=self.request.user,
            updated_by=self.request.user,
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.updated_by = self.request.user
        instance.save()


class ProductLineViewSet(ModelViewSet):
    """
    A viewset for viewing and editing product images instances.
    """

    queryset = ProductLine.objects.all()
    serializer_class = ProductLineDetailSerializer
    permission_classes = [IsAdminUser | IsOwner | IsAuthenticatedReadOnly]
    lookup_field = "sku"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ProductLineSerializer
        if self.action in ["create", "update", "partial_update"]:
            return ProductLineEditSerializer
        return ProductLineDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.updated_by = self.request.user
        instance.save()


class ProductImageViewSet(ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageDetailSerializer
    permission_classes = [IsAdminUser | IsOwner | IsAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return ProductImageSerializer
        if self.action in ["create", "update", "partial_update"]:
            return ProductImageEditSerializer
        return ProductImageDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
