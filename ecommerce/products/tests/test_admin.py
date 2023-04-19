import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from ecommerce.products.models import Brand, Category, Product
from ecommerce.products.tests.factories import (
    BrandFactory,
    CategoryFactory,
    ProductFactory,
)
from ecommerce.users.models import User
from ecommerce.utils.serializer import model_to_dict

pytestmark = [pytest.mark.django_db, pytest.mark.e2e]


class TestCategoryAdmin:
    """Test cases for Category Administration Pages and Actions."""

    def test_changelist(self, admin_client: Client):
        """Test that the changelist page is accessible."""
        url = reverse("admin:products_category_changelist")
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_search(self, admin_client: Client):
        """Test that the search is working."""
        url = reverse("admin:products_category_changelist")
        response = admin_client.get(url, data={"q": "test"})
        assert response.status_code == status.HTTP_200_OK

    def test_make_active(
        self, admin_client: Client, category: Category, admin_user: User
    ):
        """Test that the make_active action is working."""
        url = reverse("admin:products_category_changelist")
        response = admin_client.post(
            url, data={"action": "make_active", "_selected_action": [category.pk]}
        )
        assert response.status_code == 302

        db_category = Category.objects.get(pk=category.pk)
        assert db_category is not None
        assert db_category.is_active
        assert category.created_by == db_category.created_by
        assert admin_user == db_category.updated_by

    def test_make_inactive(
        self, admin_client: Client, category: Category, admin_user: User
    ):
        """Test that the make_inactive action is working."""
        url = reverse("admin:products_category_changelist")
        response = admin_client.post(
            url, data={"action": "make_inactive", "_selected_action": [category.pk]}
        )
        assert response.status_code == 302

        db_category = Category.objects.get(pk=category.pk)
        assert db_category is not None
        assert not db_category.is_active
        assert category.created_by == db_category.created_by
        assert admin_user == db_category.updated_by

    def test_add(
        self,
        admin_client: Client,
        category_factory: CategoryFactory,
        category: Category,
        admin_user: User,
    ):
        """Test that the add page is accessible and the category is created."""
        url = reverse("admin:products_category_add")
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        category = category_factory.build(created_by=None)

        exclude_fields = [
            "id",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "lft",
            "rgt",
            "tree_id",
            "depth",
        ]
        data = model_to_dict(category, exclude_fields=exclude_fields)
        data["_position"] = "sorted-child"

        response = admin_client.post(url, data=data)
        assert response.status_code == 302
        db_category = Category.objects.filter(name=category.name).first()
        assert db_category is not None
        assert admin_user == db_category.created_by
        assert admin_user == db_category.updated_by

    def test_delete(self, admin_client: Client, category: Category):
        """Test that the delete page is not accessible."""
        url = reverse(
            "admin:products_category_delete", kwargs={"object_id": category.pk}
        )
        response = admin_client.post(url)
        assert response.status_code == 403

    def test_edit(self, admin_client: Client, category: Category, admin_user: User):
        """Test that the edit page is accessible and the category is updated."""
        url = reverse(
            "admin:products_category_change", kwargs={"object_id": category.pk}
        )
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exclude_fields = [
            "id",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "lft",
            "rgt",
            "tree_id",
            "depth",
        ]
        data = model_to_dict(category, exclude_fields=exclude_fields)
        data["_position"] = "sorted-child"

        response = admin_client.post(url, data=data)
        assert response.status_code == 302

        db_category = Category.objects.get(pk=category.pk)
        assert db_category is not None
        assert category.created_by == db_category.created_by
        assert admin_user == db_category.updated_by

    def test_view_user(self, admin_client: Client, category: Category):
        """Test that the view page is accessible."""
        url = reverse(
            "admin:products_category_change", kwargs={"object_id": category.pk}
        )
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK


class TestProductAdmin:
    """Test cases for Product Administration Pages and Actions."""

    def test_changelist(self, admin_client: Client):
        """Test that the changelist page is accessible."""
        url = reverse("admin:products_product_changelist")
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_search(self, admin_client: Client):
        """Test that the search is working."""
        url = reverse("admin:products_product_changelist")
        response = admin_client.get(url, data={"q": "test"})
        assert response.status_code == status.HTTP_200_OK

    def test_make_active(
        self, admin_client: Client, product: Product, admin_user: User
    ):
        """Test that the make_active action is working."""
        url = reverse("admin:products_product_changelist")
        response = admin_client.post(
            url, data={"action": "make_active", "_selected_action": [product.pk]}
        )
        assert response.status_code == 302

        db_product = Product.objects.get(pk=product.pk)
        assert db_product is not None
        assert db_product.is_active
        assert product.created_by == db_product.created_by
        assert admin_user == db_product.updated_by

    def test_make_inactive(
        self, admin_client: Client, product: Product, admin_user: User
    ):
        """Test that the make_inactive action is working."""
        url = reverse("admin:products_product_changelist")
        response = admin_client.post(
            url, data={"action": "make_inactive", "_selected_action": [product.pk]}
        )
        assert response.status_code == 302

        db_product = Product.objects.get(pk=product.pk)
        assert db_product is not None
        assert not db_product.is_active
        assert product.created_by == db_product.created_by
        assert admin_user == db_product.updated_by

    def test_add(
        self,
        admin_client: Client,
        product_factory: ProductFactory,
        brand: Brand,
        category: Category,
        admin_user: User,
    ):
        """Test that the add page is accessible and the product is created."""
        url = reverse("admin:products_product_add")
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        product = product_factory.build(
            owner=admin_user,
            brand=brand,
            category=category,
            product_lines=None,
        )

        exclude_fields = [
            "id",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        data = model_to_dict(product, exclude_fields=exclude_fields)
        data["images-TOTAL_FORMS"] = 0
        data["images-INITIAL_FORMS"] = 0

        response = admin_client.post(url, data=data)
        assert response.status_code == 302
        db_product = Product.objects.filter(name=product.name).first()
        assert db_product is not None
        assert admin_user == db_product.created_by
        assert admin_user == db_product.updated_by

    def test_delete(self, admin_client: Client, product: Product):
        """Test that the delete page is accessible and the product is deleted."""
        url = reverse("admin:products_product_delete", kwargs={"object_id": product.pk})
        response = admin_client.post(url)
        assert response.status_code == 403

    def test_edit(self, admin_client: Client, product: Product, admin_user: User):
        """Test that the edit page is accessible and the product is updated."""
        url = reverse("admin:products_product_change", kwargs={"object_id": product.pk})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exclude_fields = [
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        data = model_to_dict(product, exclude_fields=exclude_fields)
        data["images-TOTAL_FORMS"] = 0
        data["images-INITIAL_FORMS"] = 0

        response = admin_client.post(url, data=data)
        assert response.status_code == 302

        db_product = Product.objects.get(pk=product.pk)
        assert db_product is not None
        assert product.created_by == db_product.created_by
        assert admin_user == db_product.updated_by

    def test_view_user(self, admin_client: Client, product: Product):
        """Test that the view user page is accessible.""" ""
        url = reverse("admin:products_product_change", kwargs={"object_id": product.pk})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK


class TestBrandAdmin:
    """
    Test cases for Brand Administration Pages and Actions.
    """

    def test_changelist(self, admin_client: Client):
        """Test that the changelist page is accessible."""
        url = reverse("admin:products_brand_changelist")
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_search(self, admin_client: Client):
        """Test that the search is working."""
        url = reverse("admin:products_brand_changelist")
        response = admin_client.get(url, data={"q": "test"})
        assert response.status_code == status.HTTP_200_OK

    def test_make_active(self, admin_client: Client, brand: Brand, admin_user: User):
        """Test that the make_active action is working."""
        url = reverse("admin:products_brand_changelist")
        response = admin_client.post(
            url, data={"action": "make_active", "_selected_action": [brand.pk]}
        )
        assert response.status_code == 302

        db_brand = Brand.objects.get(pk=brand.pk)
        assert db_brand is not None
        assert db_brand.is_active
        assert brand.created_by == db_brand.created_by
        assert admin_user == db_brand.updated_by

    def test_make_inactive(self, admin_client: Client, brand: Brand, admin_user: User):
        """Test that the make_inactive action is working."""
        url = reverse("admin:products_brand_changelist")
        response = admin_client.post(
            url, data={"action": "make_inactive", "_selected_action": [brand.pk]}
        )
        assert response.status_code == status.HTTP_302_FOUND

        db_brand = Brand.objects.get(pk=brand.pk)
        assert db_brand is not None
        assert not db_brand.is_active
        assert brand.created_by == db_brand.created_by
        assert admin_user == db_brand.updated_by

    def test_add(
        self, admin_client: Client, brand_factory: BrandFactory, admin_user: User
    ):
        """Test that the add page is accessible and the add action is working."""
        url = reverse("admin:products_brand_add")
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        brand = brand_factory.build(created_by=None)

        exclude_fields = ["id", "created_by", "updated_by", "created_at", "updated_at"]
        data = model_to_dict(brand, exclude_fields=exclude_fields)

        response = admin_client.post(url, data=data)
        assert response.status_code == status.HTTP_302_FOUND
        db_brand = Brand.objects.filter(name=brand.name).first()
        assert db_brand is not None
        assert admin_user == db_brand.created_by
        assert admin_user == db_brand.updated_by

    def test_delete(self, admin_client: Client, brand: Brand):
        """Test that the delete action is disabled."""
        url = reverse("admin:products_brand_delete", kwargs={"object_id": brand.pk})
        response = admin_client.post(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_edit(self, admin_client: Client, brand: Brand, admin_user: User):
        """Test that the edit page is accessible and the edit action is working."""
        url = reverse("admin:products_brand_change", kwargs={"object_id": brand.pk})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exclude_fields = ["created_by", "updated_by", "created_at", "updated_at"]
        data = model_to_dict(brand, exclude_fields=exclude_fields)

        response = admin_client.post(url, data=data)
        assert response.status_code == status.HTTP_302_FOUND

        db_brand = Brand.objects.get(pk=brand.pk)
        assert db_brand is not None
        assert brand.created_by == db_brand.created_by
        assert admin_user == db_brand.updated_by

    def test_view_user(self, admin_client: Client, brand: Brand):
        """Test that the view page is accessible.""" ""
        url = reverse("admin:products_brand_change", kwargs={"object_id": brand.pk})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
