from rest_framework import serializers

from ecommerce.products.models import (
    Attribute,
    Brand,
    Category,
    Product,
    ProductAttribute,
    ProductImage,
    ProductLine,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "url"]
        extra_kwargs = {
            "url": {"view_name": "api:category-detail", "lookup_field": "slug"}
        }


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug", "url"]
        extra_kwargs = {
            "url": {"view_name": "api:brand-detail", "lookup_field": "slug"}
        }


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["id", "name", "slug", "url"]
        extra_kwargs = {
            "url": {"view_name": "api:attribute-detail", "lookup_field": "slug"}
        }


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    brand = serializers.CharField(source="brand.name")

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "category", "brand", "url"]
        extra_kwargs = {
            "url": {"view_name": "api:product-detail", "lookup_field": "slug"}
        }


class ProductLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLine
        fields = ["id", "price", "sku", "stock_quantity", "url"]
        extra_kwargs = {
            "url": {"view_name": "api:productline-detail", "lookup_field": "sku"}
        }


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "url"]
        extra_kwargs = {"url": {"view_name": "api:productimage-detail"}}


class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer()

    class Meta:
        model = ProductAttribute
        fields = "__all__"


class CategoryDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source="created_by.username", read_only=True)
    updated_by = serializers.CharField(source="updated_by.username", read_only=True)

    def update(self, instance, validated_data):
        # prevent slug from being updated
        validated_data.pop("slug", None)
        return super().update(instance, validated_data)

    class Meta:
        model = Category
        exclude = ["lft", "rgt", "tree_id", "depth"]


class BrandDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source="created_by.username", read_only=True)
    updated_by = serializers.CharField(source="updated_by.username", read_only=True)

    def update(self, instance, validated_data):
        # prevent slug from being updated
        validated_data.pop("slug", None)
        return super().update(instance, validated_data)

    class Meta:
        model = Brand
        fields = "__all__"


class AttributeDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source="created_by.username", read_only=True)
    updated_by = serializers.CharField(source="updated_by.username", read_only=True)

    def update(self, instance, validated_data):
        # prevent slug from being updated
        validated_data.pop("slug", None)
        validated_data.pop("owner", None)
        return super().update(instance, validated_data)

    class Meta:
        model = Attribute
        fields = "__all__"


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()
    product_lines = ProductLineSerializer(many=True)
    images = ProductImageSerializer(many=True)
    owner = serializers.CharField(source="owner.username")
    created_by = serializers.CharField(source="created_by.username")
    updated_by = serializers.CharField(source="updated_by.username")

    class Meta:
        model = Product
        fields = "__all__"


class ProductEditSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        # prevent slug from being updated
        validated_data.pop("slug", None)
        return super().update(instance, validated_data)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["owner", "created_by", "updated_by"]


class ProductLineDetailSerializer(serializers.ModelSerializer):
    """
    ProductLine Detail Serializer. Used for retrieving product lines.
    """

    product = ProductSerializer()
    product_attributes = ProductAttributeSerializer(
        source="productattribute_set", many=True
    )
    created_by = serializers.CharField(source="created_by.username")
    updated_by = serializers.CharField(source="updated_by.username")

    class Meta:
        model = ProductLine
        fields = "__all__"


class ProductLineEditSerializer(serializers.ModelSerializer):
    """
    ProductLine Edit Serializer. Used for updating product lines.
    """

    product_attributes = ProductAttributeSerializer(
        source="productattribute_set", many=True, read_only=True
    )

    def validate_price(self, data):
        """Check that price is not negative"""
        if data < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return data

    def validate_product(self, data):
        """Check that the product is owned by the user"""
        request = self.context["request"]
        user = request.user
        if data.owner.id != user.id:
            raise serializers.ValidationError("You do not own this product.")
        return data

    def update(self, instance, validated_data):
        """Prevent sku and product from being updated"""
        validated_data.pop("sku", None)
        validated_data.pop("product", None)
        return super().update(instance, validated_data)

    class Meta:
        model = ProductLine
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]


class ProductImageDetailSerializer(serializers.ModelSerializer):
    """
    ProductImage Detail Serializer. Used for retrieving and updating product images.
    """

    product = ProductSerializer()
    created_by = serializers.CharField(source="created_by.username", read_only=True)
    updated_by = serializers.CharField(source="updated_by.username", read_only=True)

    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductImageEditSerializer(serializers.ModelSerializer):
    """
    ProductImage Edit Serializer. Used for updating product images.
    """

    def validate_product(self, data):
        """Check that the product is owned by the user"""
        request = self.context["request"]
        user = request.user
        if data.owner.id != user.id:
            raise serializers.ValidationError("You do not own this product.")
        return data

    def update(self, instance, validated_data):
        """Prevent sku and product from being updated"""
        validated_data.pop("product", None)
        return super().update(instance, validated_data)

    class Meta:
        model = ProductImage
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]
