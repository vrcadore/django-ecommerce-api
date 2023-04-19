import pytest

from ecommerce.products.models import (
    Brand,
    Category,
    Product,
    ProductAttribute,
    ProductImage,
    ProductLine,
)

pytestmark = [pytest.mark.django_db]


class TestCategoryModels:
    def test_category_str(self, category: Category):
        assert str(category) == f"{category.slug}"


class TestBrandModels:
    def test_brand_str(self, brand: Brand):
        assert str(brand) == f"{brand.slug}"


class TestProductModels:
    def test_product_str(self, product: Product):
        assert str(product) == f"{product.slug}"


class TestProductLineModels:
    def test_product_line_str(self, product_line: ProductLine):
        assert str(product_line) == (
            f"{product_line.stock_quantity} of "
            f"{product_line.product.slug}({product_line.sku})"
        )


class TestProductImageModels:
    def test_product_image_str(self, product_image: ProductImage):
        assert str(product_image) == f"{product_image.product} image"


class TestAttributeModels:
    def test_attribute_str(self, attribute: Product):
        assert str(attribute) == f"{attribute.slug}"


class TestProductAttributeModels:
    def test_product_attribute_str(self, product_attribute: ProductAttribute):
        assert str(product_attribute) == (
            f"{product_attribute.product_line.product.slug}"
            f"({product_attribute.attribute.slug}) - {product_attribute.value}"
        )
