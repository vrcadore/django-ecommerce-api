from unittest.mock import Mock

import pytest
from rest_framework.test import APIRequestFactory

from ecommerce.products.api.serializers import (
    BrandDetailSerializer,
    BrandSerializer,
    CategoryDetailSerializer,
    CategorySerializer,
    ProductDetailSerializer,
    ProductSerializer,
)
from ecommerce.products.api.views import BrandViewSet, CategoryViewSet, ProductViewSet
from ecommerce.products.models import Brand, Category, Product
from ecommerce.products.tests.factories import (
    BrandFactory,
    CategoryFactory,
    ProductFactory,
)
from ecommerce.users.models import User

pytestmark = [pytest.mark.django_db]


class TestProductViewSet:
    """
    Test cases for TestProductViewSet
    """

    def test_get_queryset_list(
        self,
        product_factory: ProductFactory,
        product: Product,
        api_rf: APIRequestFactory,
    ):
        product_deactivated = product_factory(
            slug="product_deactivated", is_active=False
        )
        view = ProductViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "list"
        queryset = view.get_queryset()

        assert queryset.count() == 1
        assert queryset.first() == product
        assert product_deactivated not in queryset

    def test_get_queryset_not_list(
        self,
        product_factory: ProductFactory,
        product: Product,
        api_rf: APIRequestFactory,
    ):
        product_deactivated = product_factory(
            slug="product_deactivated", is_active=False
        )

        view = ProductViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "retrieve"
        queryset = view.get_queryset()

        assert queryset.count() == 2
        assert product in queryset
        assert product_deactivated in queryset

    def test_get_serializer_class_retrieve(self, api_rf: APIRequestFactory):
        view = ProductViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "retrieve"
        serializer_class = view.get_serializer_class()

        assert serializer_class == ProductDetailSerializer

    def test_get_serializer_class_not_retrieve(self, api_rf: APIRequestFactory):
        view = ProductViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "list"
        serializer_class = view.get_serializer_class()

        assert serializer_class == ProductSerializer

    def test_perform_destroy(self, user: User, mocker: Mock, api_rf: APIRequestFactory):
        view = ProductViewSet()
        request = api_rf.delete("/fake-url/", format="json")
        request.user = user

        view.request = request
        view.action = "destroy"
        mock_instance = mocker.Mock()
        view.perform_destroy(mock_instance)

        assert mock_instance.is_active is False
        mock_instance.save.assert_called_once_with(updated_by=user)
        mock_instance.delete.assert_not_called

    def test_perform_create(self, user: User, mocker: Mock, api_rf: APIRequestFactory):
        view = ProductViewSet()
        request = api_rf.post("/fake-url/", format="json")
        request.user = user

        view.request = request

        mock_serializer = mocker.Mock()
        view.perform_create(mock_serializer)

        mock_serializer.save.assert_called_once_with(created_by=user, updated_by=user)

    def test_perform_update(self, user: User, mocker: Mock, api_rf: APIRequestFactory):
        view = ProductViewSet()
        request = api_rf.put("/fake-url/", format="json")
        request.user = user

        view.request = request

        mock_serializer = mocker.Mock()
        view.perform_update(mock_serializer)

        mock_serializer.save.assert_called_once_with(updated_by=user)


class TestCategoryViewSet:
    """
    Test cases for TestCategoryViewSet
    """

    def test_get_queryset_list(
        self,
        category_factory: CategoryFactory,
        category: Category,
        api_rf: APIRequestFactory,
    ):
        category_deactivated = category_factory(
            name="Category Deactivated", is_active=False
        )
        view = CategoryViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "list"
        queryset = view.get_queryset()

        assert queryset.count() == 1
        assert queryset.first() == category
        assert category_deactivated not in queryset

    def test_get_queryset_not_list(
        self,
        category_factory: CategoryFactory,
        category: Category,
        api_rf: APIRequestFactory,
    ):
        category_deactivated = category_factory(
            name="Category Deactivated", is_active=False
        )

        view = CategoryViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "retrieve"
        queryset = view.get_queryset()

        assert queryset.count() == 2
        assert category in queryset
        assert category_deactivated in queryset

    def test_get_serializer_class_retrieve(self, api_rf: APIRequestFactory):
        view = CategoryViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "retrieve"
        serializer_class = view.get_serializer_class()

        assert serializer_class == CategoryDetailSerializer

    def test_get_serializer_class_not_retrieve(self, api_rf: APIRequestFactory):
        view = CategoryViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "list"
        serializer_class = view.get_serializer_class()

        assert serializer_class == CategorySerializer

    def test_perform_destroy(self, user: User, mocker: Mock, api_rf: APIRequestFactory):
        view = CategoryViewSet()
        request = api_rf.delete("/fake-url/", format="json")
        request.user = user

        view.request = request
        view.action = "destroy"
        mock_instance = mocker.Mock()
        view.perform_destroy(mock_instance)

        assert mock_instance.is_active is False
        mock_instance.save.assert_called_once_with(updated_by=user)
        mock_instance.delete.assert_not_called

    def test_perform_create(self, user: User, mocker: Mock, api_rf: APIRequestFactory):
        view = CategoryViewSet()
        request = api_rf.post("/fake-url/", format="json")
        request.user = user

        view.request = request

        mock_serializer = mocker.Mock()
        view.perform_create(mock_serializer)

        mock_serializer.save.assert_called_once_with(created_by=user, updated_by=user)

    def test_perform_update(self, user: User, mocker: Mock, api_rf: APIRequestFactory):
        view = CategoryViewSet()
        request = api_rf.put("/fake-url/", format="json")
        request.user = user

        view.request = request

        mock_serializer = mocker.Mock()
        view.perform_update(mock_serializer)

        mock_serializer.save.assert_called_once_with(updated_by=user)


class TestBrandViewSet:
    """
    Test cases for BrandViewSet
    """

    def test_get_queryset_list(
        self, brand_factory: BrandFactory, brand: Brand, api_rf: APIRequestFactory
    ):
        """
        Test that the get_queryset method is working when action is list.
        """
        brand_deactivated = brand_factory(name="Brand Deactivated", is_active=False)
        view = BrandViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "list"
        queryset = view.get_queryset()

        assert queryset.count() == 1
        assert queryset.first() == brand
        assert brand_deactivated not in queryset

    def test_get_queryset_not_list(
        self, brand_factory: BrandFactory, brand: Brand, api_rf: APIRequestFactory
    ):
        """
        Test that the get_queryset method is working when action is not list.
        """
        brand_deactivated = brand_factory(name="Brand Deactivated", is_active=False)

        view = BrandViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "retrieve"
        queryset = view.get_queryset()

        assert queryset.count() == 2
        assert brand in queryset
        assert brand_deactivated in queryset

    def test_get_serializer_class_retrieve(self, api_rf: APIRequestFactory):
        """
        Test that the get_serializer_class method is working when action is retrieve.
        """
        view = BrandViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "retrieve"
        serializer_class = view.get_serializer_class()

        assert serializer_class == BrandDetailSerializer

    def test_get_serializer_class_not_retrieve(self, api_rf: APIRequestFactory):
        """
        Test that the get_serializer_class method is working when action isn't retrieve.
        """
        view = BrandViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "list"
        serializer_class = view.get_serializer_class()

        assert serializer_class == BrandSerializer

    def test_perform_destroy(self, user: User, mocker: Mock, api_rf: APIRequestFactory):
        """
        Test that the perform_destroy method is working.
        """
        view = BrandViewSet()
        request = api_rf.delete("/fake-url/", format="json")
        request.user = user

        view.request = request
        view.action = "destroy"
        mock_instance = mocker.Mock()
        view.perform_destroy(mock_instance)

        assert mock_instance.is_active is False
        mock_instance.save.assert_called_once_with(updated_by=user)
        mock_instance.delete.assert_not_called

    def test_perform_create(self, user: User, mocker: Mock, api_rf: APIRequestFactory):
        """
        Test that the perform_create method is working.
        """
        view = BrandViewSet()
        request = api_rf.post("/fake-url/", format="json")
        request.user = user

        view.request = request

        mock_serializer = mocker.Mock()
        view.perform_create(mock_serializer)

        mock_serializer.save.assert_called_once_with(created_by=user, updated_by=user)

    def test_perform_update(self, user: User, mocker: Mock, api_rf: APIRequestFactory):
        """
        Test that the perform_update method is working.
        """
        view = BrandViewSet()
        request = api_rf.put("/fake-url/", format="json")
        request.user = user

        view.request = request

        mock_serializer = mocker.Mock()
        view.perform_update(mock_serializer)

        mock_serializer.save.assert_called_once_with(updated_by=user)
