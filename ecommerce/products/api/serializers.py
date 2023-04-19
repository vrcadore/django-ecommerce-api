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
        fields = ["id", "name", "url"]
        extra_kwargs = {
            "url": {"view_name": "api:brand-detail", "lookup_field": "slug"}
        }


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["id", "name", "url"]
        extra_kwargs = {
            "url": {"view_name": "api:attribute-detail", "lookup_field": "slug"}
        }


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "url"]
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
    class Meta:
        model = Category
        exclude = ["lft", "rgt", "tree_id", "depth"]


class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class AttributeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = "__all__"


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()
    product_lines = ProductLineSerializer(many=True)
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductLineDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    product_attributes = ProductAttributeSerializer(
        source="productattribute_set", many=True
    )

    class Meta:
        model = ProductLine
        fields = "__all__"


class ProductImageDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductImage
        fields = "__all__"
