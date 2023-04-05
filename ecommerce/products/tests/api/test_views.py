from unittest.mock import Mock

import pytest
from rest_framework.test import APIRequestFactory

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
    ProductImageSerializer,
    ProductLineDetailSerializer,
    ProductLineSerializer,
    ProductSerializer,
)
from ecommerce.products.api.views import (
    AttributeViewSet,
    BrandViewSet,
    CategoryViewSet,
    ProductImageViewSet,
    ProductLineViewSet,
    ProductViewSet,
)
from ecommerce.products.models import (
    Attribute,
    Brand,
    Category,
    Product,
    ProductImage,
    ProductLine,
)
from ecommerce.products.tests.factories import (
    AttributeFactory,
    BrandFactory,
    CategoryFactory,
    ProductFactory,
    ProductImageFactory,
    ProductLineFactory,
)
from ecommerce.users.models import User

pytestmark = [pytest.mark.django_db]


class TestAttributeViewSet:
    """
    Test cases for TestAttributeViewSet
    """

    def test_get_queryset_when_list(
        self,
        attribute_factory: AttributeFactory,
        attribute: Attribute,
        api_rf: APIRequestFactory,
    ):
        attribute_deactivated = attribute_factory(
            slug="attribute_deactivated", is_active=False
        )
        view = AttributeViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "list"
        queryset = view.get_queryset()

        assert queryset.count() == 1
        assert queryset.first() == attribute
        assert attribute_deactivated not in queryset

    def test_get_queryset_when_not_list(
        self,
        attribute_factory: AttributeFactory,
        attribute: Attribute,
        api_rf: APIRequestFactory,
    ):
        attribute_deactivated = attribute_factory(
            slug="attribute_deactivated", is_active=False
        )

        view = AttributeViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "retrieve"
        queryset = view.get_queryset()

        assert queryset.count() == 2
        assert attribute in queryset
        assert attribute_deactivated in queryset

    def test_get_serializer_class_when_retrieve(self, api_rf: APIRequestFactory):
        view = AttributeViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "retrieve"
        serializer_when_class = view.get_serializer_class()

        assert serializer_when_class == AttributeDetailSerializer

    def test_get_serializer_class_when_list(self, api_rf: APIRequestFactory):
        view = AttributeViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "list"
        serializer_when_class = view.get_serializer_class()

        assert serializer_when_class == AttributeSerializer

    def test_perform_create_when_valid(
        self, user: User, mocker: Mock, api_rf: APIRequestFactory
    ):
        view = AttributeViewSet()
        request = api_rf.post("/fake-url/", format="json")
        request.user = user

        view.request = request

        mock_serializer = mocker.Mock()
        view.perform_create(mock_serializer)

        mock_serializer.save.assert_called_once_with(created_by=user, updated_by=user)

    def test_perform_update_when_valid(
        self, user: User, mocker: Mock, api_rf: APIRequestFactory
    ):
        view = AttributeViewSet()
        request = api_rf.post("/fake-url/", format="json")
        request.user = user

        view.request = request

        mock_serializer = mocker.Mock()
        view.perform_update(mock_serializer)

        mock_serializer.save.assert_called_once_with(updated_by=user)

    def test_perform_destroy_when_valid(
        self, user: User, mocker: Mock, api_rf: APIRequestFactory
    ):
        view = AttributeViewSet()
        request = api_rf.delete("/fake-url/", format="json")
        request.user = user

        view.request = request
        view.action = "destroy"
        mock_instance = mocker.Mock()
        view.perform_destroy(mock_instance)

        assert mock_instance.is_active is False
        assert mock_instance.updated_by == user
        mock_instance.save.assert_called_once
        mock_instance.delete.assert_not_called


class TestProductViewSet:
    """
    Test cases for TestProductViewSet
    """

    def test_get_queryset_when_list(
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

    def test_get_queryset_when_not_list(
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

    def test_get_serializer_class_when_retrieve(self, api_rf: APIRequestFactory):
        view = ProductViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "retrieve"
        serializer_when_class = view.get_serializer_class()

        assert serializer_when_class == ProductDetailSerializer

    def test_get_serializer_class_when_create(self, api_rf: APIRequestFactory):
        view = ProductViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "create"
        serializer_when_class = view.get_serializer_class()

        assert serializer_when_class == ProductEditSerializer

    def test_get_serializer_class_when_list(self, api_rf: APIRequestFactory):
        view = ProductViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "list"
        serializer_when_class = view.get_serializer_class()

        assert serializer_when_class == ProductSerializer

    def test_perform_destroy_when_valid(
        self, user: User, mocker: Mock, api_rf: APIRequestFactory
    ):
        view = ProductViewSet()
        request = api_rf.delete("/fake-url/", format="json")
        request.user = user

        view.request = request
        view.action = "destroy"
        mock_instance = mocker.Mock()
        view.perform_destroy(mock_instance)

        assert mock_instance.is_active is False
        assert mock_instance.updated_by == user
        mock_instance.save.assert_called_once
        mock_instance.delete.assert_not_called

    def test_perform_create_when_valid(
        self, user: User, mocker: Mock, api_rf: APIRequestFactory
    ):
        view = ProductViewSet()
        request = api_rf.post("/fake-url/", format="json")
        request.user = user

        view.request = request

        mock_serializer = mocker.Mock()
        view.perform_create(mock_serializer)

        mock_serializer.save.assert_called_once_with(
            owner=user, created_by=user, updated_by=user
        )

    def test_perform_update_when_valid(
        self, user: User, mocker: Mock, api_rf: APIRequestFactory
    ):
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

    def test_get_queryset_when_list(
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

    def test_get_queryset_when_not_list(
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

    def test_get_serializer_class_when_retrieve(self, api_rf: APIRequestFactory):
        view = CategoryViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "retrieve"
        serializer_when_class = view.get_serializer_class()

        assert serializer_when_class == CategoryDetailSerializer

    def test_get_serializer_class_when_list(self, api_rf: APIRequestFactory):
        view = CategoryViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "list"
        serializer_when_class = view.get_serializer_class()

        assert serializer_when_class == CategorySerializer


class TestBrandViewSet:
    """
    Test cases for BrandViewSet
    """

    def test_get_queryset_when_list(
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

    def test_get_queryset_when_not_list(
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

    def test_get_serializer_class_when_retrieve(self, api_rf: APIRequestFactory):
        """
        Test that the get_serializer_when_class method
        is working when action is retrieve.
        """
        view = BrandViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "retrieve"
        serializer_when_class = view.get_serializer_class()

        assert serializer_when_class == BrandDetailSerializer

    def test_get_serializer_class_when_list(self, api_rf: APIRequestFactory):
        """
        Test that the get_serializer_when_class method
        is working when action isn't retrieve.
        """
        view = BrandViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "list"
        serializer_when_class = view.get_serializer_class()

        assert serializer_when_class == BrandSerializer

    def test_perform_destroy_when_valid(
        self, user: User, mocker: Mock, api_rf: APIRequestFactory
    ):
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
        assert mock_instance.updated_by == user
        mock_instance.save.assert_called_once
        mock_instance.delete.assert_not_called

    def test_perform_create_when_valid(
        self, user: User, mocker: Mock, api_rf: APIRequestFactory
    ):
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

    def test_perform_update_when_valid(
        self, user: User, mocker: Mock, api_rf: APIRequestFactory
    ):
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


class TestProductLineViewSet:
    """
    Test cases for ProductLineViewSet
    """

    def test_get_queryset_when_list(
        self,
        product_line_factory: ProductLineFactory,
        product_line: ProductLine,
        api_rf: APIRequestFactory,
    ):
        """
        Test that the get_queryset method is working when action is list.
        """
        product_line_deactivated = product_line_factory(is_active=False)
        view = ProductLineViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "list"
        queryset = view.get_queryset()

        assert queryset.count() == 1
        assert queryset.first() == product_line
        assert product_line_deactivated not in queryset

    def test_get_queryset_when_not_list(
        self,
        product_line_factory: ProductLineFactory,
        product_line: ProductLine,
        api_rf: APIRequestFactory,
    ):
        """
        Test that the get_queryset method is working when action is not list.
        """

        product_line_deactivated = product_line_factory(is_active=False)
        view = ProductLineViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "retrieve"
        queryset = view.get_queryset()

        assert queryset.count() == 2
        assert product_line in queryset
        assert product_line_deactivated in queryset

    def test_get_serializer_class_when_retrieve(self, api_rf: APIRequestFactory):
        """
        Test that the get_serializer_when_class method
        is working when action is retrieve.
        """
        view = ProductLineViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "retrieve"
        serializer_when_class = view.get_serializer_class()

        assert serializer_when_class == ProductLineDetailSerializer

    def test_get_serializer_class_when_list(self, api_rf: APIRequestFactory):
        """
        Test that the get_serializer_when_class method
        is working when action isn't retrieve.
        """
        view = ProductLineViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "list"
        serializer_when_class = view.get_serializer_class()

        assert serializer_when_class == ProductLineSerializer

    def test_perform_destroy_when_valid(
        self, user: User, mocker: Mock, api_rf: APIRequestFactory
    ):
        """
        Test that the perform_destroy method is working.
        """
        view = ProductLineViewSet()
        request = api_rf.delete("/fake-url/", format="json")
        request.user = user

        view.request = request
        view.action = "destroy"
        mock_instance = mocker.Mock()
        view.perform_destroy(mock_instance)

        assert mock_instance.is_active is False
        assert mock_instance.updated_by == user
        mock_instance.save.assert_called_once
        mock_instance.delete.assert_not_called

    def test_perform_create_when_valid(
        self, user: User, mocker: Mock, api_rf: APIRequestFactory
    ):
        """
        Test that the perform_create method is working.
        """
        view = ProductLineViewSet()
        request = api_rf.post("/fake-url/", format="json")
        request.user = user

        view.request = request

        mock_serializer = mocker.Mock()
        view.perform_create(mock_serializer)

        mock_serializer.save.assert_called_once_with(created_by=user, updated_by=user)

    def test_perform_update_when_valid(
        self, user: User, mocker: Mock, api_rf: APIRequestFactory
    ):
        """
        Test that the perform_update method is working.
        """
        view = ProductLineViewSet()
        request = api_rf.put("/fake-url/", format="json")
        request.user = user

        view.request = request

        mock_serializer = mocker.Mock()
        view.perform_update(mock_serializer)

        mock_serializer.save.assert_called_once_with(updated_by=user)


class TestProductImageViewSet:
    def test_get_queryset_when_list(
        self,
        product_image_factory: ProductImageFactory,
        product_image: ProductImage,
        api_rf: APIRequestFactory,
    ):
        """
        Test that the get_queryset method is working when action is list.
        """
        product_image_deactivated = product_image_factory()
        view = ProductImageViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "list"
        queryset = view.get_queryset()

        assert queryset.count() == 2
        assert product_image in queryset
        assert product_image_deactivated in queryset

    def test_get_serializer_class_when_retrieve(self, api_rf: APIRequestFactory):
        """
        Test that the get_serializer_when_class method
        is working when action is retrieve.
        """
        view = ProductImageViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "retrieve"
        serializer_when_class = view.get_serializer_class()

        assert serializer_when_class == ProductImageDetailSerializer

    def test_get_serializer_class_when_list(self, api_rf: APIRequestFactory):
        """
        Test that the get_serializer_when_class method
        is working when action isn't retrieve.
        """
        view = ProductImageViewSet()
        request = api_rf.get("/fake-url/", format="json")

        view.request = request
        view.action = "list"
        serializer_when_class = view.get_serializer_class()

        assert serializer_when_class == ProductImageSerializer

    def test_perform_destroy_when_valid(
        self, user: User, mocker: Mock, api_rf: APIRequestFactory
    ):
        """
        Test that the perform_destroy method is working.
        """
        view = ProductImageViewSet()
        request = api_rf.delete("/fake-url/", format="json")
        request.user = user

        view.request = request
        view.action = "destroy"
        mock_instance = mocker.Mock()
        view.perform_destroy(mock_instance)

        mock_instance.delete.assert_called_once

    def test_perform_create_when_valid(
        self, user: User, mocker: Mock, api_rf: APIRequestFactory
    ):
        """
        Test that the perform_create method is working.
        """
        view = ProductImageViewSet()
        request = api_rf.post("/fake-url/", format="json")
        request.user = user

        view.request = request

        mock_serializer = mocker.Mock()
        view.perform_create(mock_serializer)

        mock_serializer.save.assert_called_once_with(created_by=user, updated_by=user)

    def test_perform_update_when_valid(
        self, user: User, mocker: Mock, api_rf: APIRequestFactory
    ):
        """
        Test that the perform_update method is working.
        """
        view = ProductImageViewSet()
        request = api_rf.put("/fake-url/", format="json")
        request.user = user

        view.request = request

        mock_serializer = mocker.Mock()
        view.perform_update(mock_serializer)

        mock_serializer.save.assert_called_once_with(updated_by=user)
