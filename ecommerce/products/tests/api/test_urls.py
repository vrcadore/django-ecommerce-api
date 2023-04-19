import pytest
from django.urls import resolve, reverse

from ecommerce.products.models import Attribute, Brand, Category, Product, ProductLine

pytestmark = [pytest.mark.django_db]


class TestUrls:
    """
    Test cases for urls generation and resolution.
    """

    def test_category_detail(self, category: Category):
        """
        Test category detail url resolution.
        """
        reverse_url = reverse(
            "api:category-detail", kwargs={"slug": str(category.slug)}
        )
        resolved_url = resolve(f"/api/categories/{category.slug}/").view_name
        assert reverse_url == f"/api/categories/{category.slug}/"
        assert resolved_url == "api:category-detail"

    def test_category_list(self):
        """
        Test category list url resolution.
        """
        reverse_url = reverse("api:category-list")
        resolved_url = resolve("/api/categories/").view_name
        assert reverse_url == "/api/categories/"
        assert resolved_url == "api:category-list"

    def test_attribute_detail(self, attribute: Attribute):
        """
        Test attribute detail url resolution.
        """
        reverse_url = reverse(
            "api:attribute-detail", kwargs={"slug": str(attribute.slug)}
        )
        resolved_url = resolve(f"/api/attributes/{attribute.slug}/").view_name
        assert reverse_url == f"/api/attributes/{attribute.slug}/"
        assert resolved_url == "api:attribute-detail"

    def test_attribute_list(self):
        """
        Test attribute list url resolution.
        """
        reverse_url = reverse("api:attribute-list")
        resolved_url = resolve("/api/attributes/").view_name
        assert reverse_url == "/api/attributes/"
        assert resolved_url == "api:attribute-list"

    def test_brand_detail(self, brand: Brand):
        """
        Test brand detail url resolution.
        """
        reverse_url = reverse("api:brand-detail", kwargs={"slug": str(brand.slug)})
        resolved_url = resolve(f"/api/brands/{brand.slug}/").view_name
        assert reverse_url == f"/api/brands/{brand.slug}/"
        assert resolved_url == "api:brand-detail"

    def test_brand_list(self):
        """
        Test brand list url resolution.
        """
        reverse_url = reverse("api:brand-list")
        resolved_url = resolve("/api/brands/").view_name
        assert reverse_url == "/api/brands/"
        assert resolved_url == "api:brand-list"

    def test_product_detail(self, product: Product):
        """
        Test product detail url resolution.
        """
        reverse_url = reverse("api:product-detail", kwargs={"slug": str(product.slug)})
        resolved_url = resolve(f"/api/products/{product.slug}/").view_name
        assert reverse_url == f"/api/products/{product.slug}/"
        assert resolved_url == "api:product-detail"

    def test_product_list(self):
        """
        Test product list url resolution.
        """
        reverse_url = reverse("api:product-list")
        resolved_url = resolve("/api/products/").view_name
        assert reverse_url == "/api/products/"
        assert resolved_url == "api:product-list"

    def test_product_line_detail(self, product_line: ProductLine):
        """
        Test product detail url resolution.
        """
        reverse_url = reverse(
            "api:productline-detail", kwargs={"sku": str(product_line.sku)}
        )
        resolved_url = resolve(f"/api/product_lines/{product_line.sku}/").view_name
        assert reverse_url == f"/api/product_lines/{product_line.sku}/"
        assert resolved_url == "api:productline-detail"

    def test_product_line_list(self):
        """
        Test product list url resolution.
        """
        reverse_url = reverse("api:productline-list")
        resolved_url = resolve("/api/product_lines/").view_name
        assert reverse_url == "/api/product_lines/"
        assert resolved_url == "api:productline-list"
