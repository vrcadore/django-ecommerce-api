from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status

from ecommerce.products.models import Attribute, Brand, Product
from ecommerce.utils.serializer import model_to_dict

pytestmark = [pytest.mark.django_db, pytest.mark.e2e]


class TestCategoryEndpoint:
    def test_get_category_when_unauthenticated(self, api_client, category):
        url = reverse("api:category-detail", kwargs={"slug": category.slug})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_category_when_authenticated(self, auth_api_client, category):
        url = reverse("api:category-detail", kwargs={"slug": category.slug})
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == category.name

    def test_get_category_when_admin_authenticated(self, admin_api_client, category):
        url = reverse("api:category-detail", kwargs={"slug": category.slug})
        response = admin_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == category.name

    def test_get_category_when_dont_exists(self, auth_api_client):
        url = reverse("api:category-detail", kwargs={"slug": "fake-slug"})
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_category_when_unauthenticated(self, api_client):
        url = reverse("api:category-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_category_when_authenticated(self, auth_api_client, category_factory):
        category_factory.create_batch(10)
        url = reverse("api:category-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 10
        assert len(response.data["results"]) == 10

    def test_list_category_when_dont_exists(self, auth_api_client):
        url = reverse("api:category-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert len(response.data["results"]) == 0

    def test_list_category_when_has_deactivated_entries(
        self, auth_api_client, category_factory, category
    ):
        category_factory.create_batch(10, is_active=False)
        url = reverse("api:category-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == str(category.id)
        assert response.data["results"][0]["name"] == category.name
        assert response.data["results"][0]["slug"] == category.slug


@pytest.mark.e2e
class TestBrandEndpoint:
    VALID_BRAND_DATA = [
        ("name", "Brand Name"),
        ("description", "New description"),
        ("is_active", True),
    ]

    INVALID_BRAND_DATA = [
        ("name", None),
        ("slug", "invalid slug"),
        ("description", None),
        ("is_active", None),
    ]

    def test_get_brand_when_unauthenticated(self, api_client, brand):
        url = reverse("api:brand-detail", kwargs={"slug": brand.slug})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_brand_when_authenticated(self, auth_api_client, brand):
        url = reverse("api:brand-detail", kwargs={"slug": brand.slug})
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == brand.name

    def test_get_brand_when_admin_authenticated(self, admin_api_client, brand):
        url = reverse("api:brand-detail", kwargs={"slug": brand.slug})
        response = admin_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == brand.name

    def test_get_brand_when_dont_exists(self, auth_api_client):
        url = reverse("api:brand-detail", kwargs={"slug": "fake-slug"})
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_brand_when_unauthenticated(self, api_client):
        url = reverse("api:brand-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_brand_when_authenticated(self, auth_api_client, brand_factory):
        brand_factory.create_batch(10)
        url = reverse("api:brand-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 10
        assert len(response.data["results"]) == 10

    def test_list_brand_when_dont_exists(self, auth_api_client):
        url = reverse("api:brand-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0

    def test_list_brand_when_has_deactivated_entries(
        self, auth_api_client, brand_factory, brand
    ):
        brand_factory.create_batch(10, is_active=False)
        url = reverse("api:brand-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == str(brand.id)
        assert response.data["results"][0]["name"] == brand.name
        assert response.data["results"][0]["slug"] == brand.slug

    def test_create_brand_when_unauthenticated(self, api_client, brand_factory):
        url = reverse("api:brand-list")
        data = model_to_dict(brand_factory.build())
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_brand_when_authenticated(self, auth_api_client, brand_factory):
        url = reverse("api:brand-list")
        data = model_to_dict(brand_factory.build())
        response = auth_api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_brand_when_duplicate(self, admin_api_client, brand, brand_factory):
        other_brand = brand_factory(slug=brand.slug)
        url = reverse("api:brand-list")
        data = model_to_dict(other_brand)
        response = admin_api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize("field_key, field_value", VALID_BRAND_DATA)
    def test_create_brand_when_admin_authenticated(
        self, admin_api_client, brand_factory, field_key, field_value
    ):
        url = reverse("api:brand-list")
        data = model_to_dict(brand_factory.build())
        data[field_key] = field_value
        response = admin_api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data[field_key] == data[field_key]

    @pytest.mark.parametrize("field_key, field_value", INVALID_BRAND_DATA)
    def test_create_brand_when_invalid_value(
        self, admin_api_client, brand_factory, field_key, field_value
    ):
        url = reverse("api:brand-list")
        data = model_to_dict(brand_factory.build())
        data[field_key] = field_value
        response = admin_api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field_key in response.data

    def test_update_brand_when_unauthenticated(self, api_client, brand):
        url = reverse("api:brand-detail", kwargs={"slug": brand.slug})
        data = model_to_dict(brand)
        response = api_client.put(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_brand_when_authenticated(self, auth_api_client, brand):
        url = reverse("api:brand-detail", kwargs={"slug": brand.slug})
        data = model_to_dict(brand)
        response = auth_api_client.put(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("field_key, field_value", VALID_BRAND_DATA)
    def test_update_brand_when_admin_authenticated(
        self, admin_api_client, brand, field_key, field_value
    ):
        url = reverse("api:brand-detail", kwargs={"slug": brand.slug})
        data = model_to_dict(brand)
        data[field_key] = field_value
        response = admin_api_client.put(url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[field_key] == data[field_key]

    @pytest.mark.parametrize("field_key, field_value", INVALID_BRAND_DATA)
    def test_update_brand_when_invalid_value(
        self, admin_api_client, brand, field_key, field_value
    ):
        url = reverse("api:brand-detail", kwargs={"slug": brand.slug})
        data = model_to_dict(brand)
        data[field_key] = field_value
        response = admin_api_client.put(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field_key in response.data

    def test_patch_brand_when_unauthenticated(self, api_client, brand):
        url = reverse("api:brand-detail", kwargs={"slug": brand.slug})
        data = {"name": "new name"}
        response = api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_brand_when_authenticated(self, auth_api_client, brand):
        url = reverse("api:brand-detail", kwargs={"slug": brand.slug})
        data = {"name": "new name"}
        response = auth_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("field_key, field_value", VALID_BRAND_DATA)
    def test_patch_brand_when_admin_authenticated(
        self, admin_api_client, brand, field_key, field_value
    ):
        url = reverse("api:brand-detail", kwargs={"slug": brand.slug})
        data = {field_key: field_value}
        response = admin_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[field_key] == data[field_key]

    def test_delete_brand_when_admin_authenticated(self, admin_api_client, brand):
        url = reverse("api:brand-detail", kwargs={"slug": brand.slug})
        response = admin_api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        db_brand = Brand.objects.get(pk=brand.pk)
        assert db_brand is not None
        assert db_brand.is_active is False

    def test_delete_brand_when_authenticated(self, auth_api_client, brand):
        url = reverse("api:brand-detail", kwargs={"slug": brand.slug})
        response = auth_api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_brand_when_unauthenticated(self, api_client, brand):
        url = reverse("api:brand-detail", kwargs={"slug": brand.slug})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.e2e
class TestAttributeEndpoint:
    VALID_ATTRIBUTE_DATA = [
        ("name", "Attribute Name"),
        ("description", "New description"),
        ("is_active", True),
    ]

    def test_get_attribute_when_unauthenticated(self, api_client, attribute):
        url = reverse("api:attribute-detail", kwargs={"slug": attribute.slug})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_attribute_when_authenticated(self, auth_api_client, attribute):
        url = reverse("api:attribute-detail", kwargs={"slug": attribute.slug})
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == attribute.name

    def test_get_attribute_when_admin_authenticated(self, admin_api_client, attribute):
        url = reverse("api:attribute-detail", kwargs={"slug": attribute.slug})
        response = admin_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == attribute.name

    def test_get_attribute_when_dont_exists(self, auth_api_client):
        url = reverse("api:attribute-detail", kwargs={"slug": "fake-slug"})
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_attribute_when_unauthenticated(self, api_client):
        url = reverse("api:attribute-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_attribute_when_authenticated(
        self, auth_api_client, attribute_factory
    ):
        attribute_factory.create_batch(10)
        url = reverse("api:attribute-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 10
        assert len(response.data["results"]) == 10

    def test_list_attribute_when_dont_exists(self, auth_api_client):
        url = reverse("api:attribute-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert len(response.data["results"]) == 0

    def test_list_attribute_when_has_deactivated_entries(
        self, auth_api_client, attribute_factory, attribute
    ):
        attribute_factory.create_batch(10, is_active=False)
        url = reverse("api:attribute-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == str(attribute.id)
        assert response.data["results"][0]["name"] == attribute.name
        assert response.data["results"][0]["slug"] == attribute.slug

    def test_delete_attribute_when_administrator(
        self, admin_api_client, attribute_factory
    ):
        attribute = attribute_factory(is_active=True)
        url = reverse("api:attribute-detail", kwargs={"slug": attribute.slug})
        response = admin_api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        db_attribute = Attribute.objects.get(pk=attribute.pk)
        assert db_attribute is not None
        assert db_attribute.is_active is False

    def test_create_attribute_when_unauthenticated(self, api_client, attribute_factory):
        url = reverse("api:attribute-list")
        data = model_to_dict(attribute_factory.build())
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_attribute_when_authenticated(
        self, auth_api_client, attribute_factory
    ):
        url = reverse("api:attribute-list")
        data = model_to_dict(attribute_factory.build())
        response = auth_api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("field_key, field_value", VALID_ATTRIBUTE_DATA)
    def test_create_attribute_when_administrator(
        self, admin_api_client, attribute_factory, field_key, field_value
    ):
        url = reverse("api:attribute-list")
        data = model_to_dict(attribute_factory.build())
        data[field_key] = field_value
        response = admin_api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data[field_key] == data[field_key]

    def test_create_attribute_when_duplicated(
        self, admin_api_client, attribute, attribute_factory
    ):
        other_attribute = attribute_factory(slug=attribute.slug)
        url = reverse("api:attribute-list")
        data = model_to_dict(other_attribute)
        response = admin_api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_attribute_when_unauthenticated(self, api_client, attribute):
        url = reverse("api:attribute-detail", kwargs={"slug": attribute.slug})
        data = model_to_dict(attribute)
        response = api_client.put(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_attribute_when_authenticated(self, auth_api_client, attribute):
        url = reverse("api:attribute-detail", kwargs={"slug": attribute.slug})
        data = model_to_dict(attribute)
        response = auth_api_client.put(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("field_key, field_value", VALID_ATTRIBUTE_DATA)
    def test_update_attribute_when_administrator(
        self, admin_api_client, attribute, field_key, field_value
    ):
        url = reverse("api:attribute-detail", kwargs={"slug": attribute.slug})
        data = model_to_dict(attribute)
        data[field_key] = field_value
        response = admin_api_client.put(url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[field_key] == data[field_key]

    def test_patch_attribute_when_unauthenticated(self, api_client, attribute):
        url = reverse("api:attribute-detail", kwargs={"slug": attribute.slug})
        data = {"name": "new name"}
        response = api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_attribute_when_authenticated(self, auth_api_client, attribute):
        url = reverse("api:attribute-detail", kwargs={"slug": attribute.slug})
        data = {"name": "new name"}
        response = auth_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("field_key, field_value", VALID_ATTRIBUTE_DATA)
    def test_patch_attribute_when_administrator(
        self, admin_api_client, attribute, field_key, field_value
    ):
        url = reverse("api:attribute-detail", kwargs={"slug": attribute.slug})
        data = {field_key: field_value}
        response = admin_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[field_key] == data[field_key]

    def test_delete_attribute_when_authenticated(self, auth_api_client, attribute):
        url = reverse("api:attribute-detail", kwargs={"slug": attribute.slug})
        response = auth_api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_attribute_when_unauthenticated(self, api_client, attribute):
        url = reverse("api:attribute-detail", kwargs={"slug": attribute.slug})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.e2e
class TestProductEndpoint:
    VALID_PRODUCT_DATA = [
        ("name", "new name"),
        ("description", "new description"),
        ("is_active", True),
    ]

    INVALID_PRODUCT_DATA = [
        ("name", None),
        ("slug", "invalid slug"),
        ("description", None),
        ("is_active", None),
    ]

    def test_get_product_when_unauthenticated(self, api_client, product):
        url = reverse("api:product-detail", kwargs={"slug": product.slug})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_product_when_authenticated(self, auth_api_client, product):
        url = reverse("api:product-detail", kwargs={"slug": product.slug})
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == product.name

    def test_get_product_when_admin_authenticated(self, admin_api_client, product):
        url = reverse("api:product-detail", kwargs={"slug": product.slug})
        response = admin_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == product.name

    def test_get_product_when_dont_exists(self, auth_api_client):
        url = reverse("api:product-detail", kwargs={"slug": "fake-slug"})
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_product_when_unauthenticated(self, api_client):
        url = reverse("api:product-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_product_when_authenticated(self, auth_api_client, product_factory):
        product_factory.create_batch(10)
        url = reverse("api:product-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 10
        assert len(response.data["results"]) == 10

    def test_list_product_when_dont_exists(self, auth_api_client):
        url = reverse("api:product-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert len(response.data["results"]) == 0

    def test_list_product_when_has_deactivated_entries(
        self, auth_api_client, product_factory, product
    ):
        product_factory.create_batch(10, is_active=False)
        url = reverse("api:product-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == str(product.id)
        assert response.data["results"][0]["name"] == product.name
        assert response.data["results"][0]["slug"] == product.slug

    def test_create_product_when_unauthenticated(self, api_client, product_factory):
        url = reverse("api:product-list")
        data = model_to_dict(product_factory.build())
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("field_key, field_value", VALID_PRODUCT_DATA)
    def test_create_product_when_authenticated(
        self,
        auth_api_client,
        user,
        category,
        brand,
        product_factory,
        field_key,
        field_value,
    ):
        url = reverse("api:product-list")
        data = model_to_dict(
            product_factory.build(owner=None, category=category, brand=brand)
        )
        data[field_key] = field_value
        response = auth_api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data[field_key] == field_value
        assert str(response.data["owner"]) == str(user.id)

    @pytest.mark.parametrize("field_key, field_value", INVALID_PRODUCT_DATA)
    def test_create_product_when_invalid_value(
        self,
        auth_api_client,
        category,
        brand,
        product_factory,
        field_key,
        field_value,
    ):
        url = reverse("api:product-list")
        data = model_to_dict(
            product_factory.build(owner=None, category=category, brand=brand)
        )
        data[field_key] = field_value
        response = auth_api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field_key in response.data

    def test_create_product_when_duplicated(self, auth_api_client, product):
        url = reverse("api:product-list")
        data = model_to_dict(product)
        response = auth_api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["slug"][0].code == "unique"

    def test_update_product_when_unauthenticated(self, api_client, product):
        url = reverse("api:product-detail", kwargs={"slug": product.slug})
        data = model_to_dict(product)
        response = api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("field_key, field_value", VALID_PRODUCT_DATA)
    def test_update_product_when_owner(
        self, auth_api_client, user, product_factory, field_key, field_value
    ):
        product = product_factory(owner=user)
        url = reverse("api:product-detail", kwargs={"slug": product.slug})
        data = model_to_dict(product)
        data[field_key] = field_value
        response = auth_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[field_key] == field_value

    @pytest.mark.parametrize("field_key, field_value", INVALID_PRODUCT_DATA)
    def test_update_product_when_invalid_value(
        self, auth_api_client, user, product_factory, field_key, field_value
    ):
        product = product_factory(owner=user)
        url = reverse("api:product-detail", kwargs={"slug": product.slug})
        data = model_to_dict(product)
        data[field_key] = field_value
        response = auth_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field_key in response.data

    def test_update_product_when_not_owner(
        self, auth_api_client, user_factory, product_factory
    ):
        owner = user_factory()
        product = product_factory(owner=owner)
        url = reverse("api:product-detail", kwargs={"slug": product.slug})
        data = model_to_dict(product)
        response = auth_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_product_when_unauthenticated(self, api_client, product):
        url = reverse("api:product-detail", kwargs={"slug": product.slug})
        response = api_client.patch(url, data={"name": "New Name"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_product_when_not_owner(
        self, auth_api_client, user_factory, product_factory
    ):
        owner = user_factory()
        product = product_factory(owner=owner)
        url = reverse("api:product-detail", kwargs={"slug": product.slug})
        response = auth_api_client.patch(url, data={"name": "New Name"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("field_key, field_value", VALID_PRODUCT_DATA)
    def test_patch_product_when_owner(
        self, auth_api_client, user, product_factory, field_key, field_value
    ):
        product = product_factory(owner=user)
        url = reverse("api:product-detail", kwargs={"slug": product.slug})
        data = {field_key: field_value}
        response = auth_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[field_key] == field_value

    @pytest.mark.parametrize("field_key, field_value", INVALID_PRODUCT_DATA)
    def test_patch_product_when_invalid_value(
        self, auth_api_client, user, product_factory, field_key, field_value
    ):
        product = product_factory(owner=user)
        url = reverse("api:product-detail", kwargs={"slug": product.slug})
        data = {field_key: field_value}
        response = auth_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field_key in response.data

    def test_delete_product_when_admin_authenticated(self, admin_api_client, product):
        url = reverse("api:product-detail", kwargs={"slug": product.slug})
        response = admin_api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        db_product = Product.objects.get(pk=product.pk)
        assert db_product is not None
        assert db_product.is_active is False

    def test_delete_product_when_owner(self, auth_api_client, user, product_factory):
        product = product_factory(owner=user)
        url = reverse("api:product-detail", kwargs={"slug": product.slug})
        response = auth_api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        db_product = Product.objects.get(pk=product.pk)
        assert db_product is not None
        assert db_product.is_active is False

    def test_delete_product_when_not_owner(
        self, auth_api_client, user_factory, product_factory
    ):
        other_user = user_factory(username="other_user")
        product = product_factory(owner=other_user)
        url = reverse("api:product-detail", kwargs={"slug": product.slug})
        response = auth_api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_product_when_unauthenticated(self, api_client, attribute):
        url = reverse("api:product-detail", kwargs={"slug": attribute.slug})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.e2e
class TestProductLineEndpoint:
    VALID_PRODUCT_LINE_DATA = [
        ("price", "12.34"),
        ("stock_quantity", 10),
        ("is_active", False),
    ]

    INVALID_PRODUCT_LINE_DATA = [
        ("sku", None),
        ("price", "-12.34"),
        ("price", ""),
        ("price", "abc"),
        ("price", None),
        ("stock_quantity", -10),
        ("stock_quantity", "abc"),
        ("stock_quantity", None),
        ("is_active", None),
        ("is_active", "abc"),
    ]

    def test_get_product_line_when_unauthenticated(self, api_client, product_line):
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_product_line_when_authenticated(self, auth_api_client, product_line):
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["sku"] == product_line.sku
        assert response.data["product"]["id"] == str(product_line.product.id)

    def test_get_product_line_when_admin_authenticated(
        self, admin_api_client, product_line
    ):
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        response = admin_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["sku"] == product_line.sku
        assert response.data["product"]["id"] == str(product_line.product.id)

    def test_get_product_line_when_dont_exists(self, admin_api_client):
        url = reverse("api:productline-detail", kwargs={"sku": "test-sku"})
        response = admin_api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_product_line_when_unauthenticated(self, api_client):
        url = reverse("api:productline-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_product_line_when_authenticated(
        self, auth_api_client, product_line_factory
    ):
        product_line_factory.create_batch(10)
        url = reverse("api:productline-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 10
        assert len(response.data["results"]) == 10

    def test_list_product_line_when_dont_exists(self, admin_api_client):
        url = reverse("api:productline-list")
        response = admin_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert len(response.data["results"]) == 0

    def test_create_product_line_when_unauthenticated(self, api_client, product_line):
        url = reverse("api:productline-list")
        data = model_to_dict(product_line)
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("field_key, field_value", VALID_PRODUCT_LINE_DATA)
    def test_create_product_line_when_admin_authenticated(
        self,
        admin_api_client,
        admin_user,
        product_factory,
        product_line,
        product_line_factory,
        field_key,
        field_value,
    ):
        url = reverse("api:productline-list")
        product = product_factory(owner=admin_user)
        product_line = product_line_factory.build(product=product)
        data = model_to_dict(product_line)
        data[field_key] = field_value
        response = admin_api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data[field_key] == field_value

    @pytest.mark.parametrize("field_key, field_value", INVALID_PRODUCT_LINE_DATA)
    def test_create_product_line_when_invalid_data(
        self,
        admin_api_client,
        admin_user,
        product_factory,
        product_line,
        product_line_factory,
        field_key,
        field_value,
    ):
        url = reverse("api:productline-list")
        product = product_factory(owner=admin_user)
        product_line = product_line_factory.build(product=product)
        data = model_to_dict(product_line)
        data[field_key] = field_value
        response = admin_api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field_key in response.data

    def test_create_product_line_when_owner(
        self, auth_api_client, user, product_factory, product_line_factory
    ):
        product = product_factory(owner=user)
        product_line = product_line_factory.build(product=product)
        url = reverse("api:productline-list")
        data = model_to_dict(product_line)
        response = auth_api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Decimal(response.data["price"]) == data["price"]

    def test_create_product_line_when_not_owner(
        self, auth_api_client, user_factory, product_factory, product_line_factory
    ):
        other_user = user_factory(username="other_user")
        product = product_factory(owner=other_user)
        product_line = product_line_factory.build(product=product)
        url = reverse("api:productline-list")
        data = model_to_dict(product_line)
        response = auth_api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response.data["product"][0].startswith("You do not own this product.")

    def test_create_product_line_when_duplicated(
        self, admin_api_client, product_line_factory, product_line
    ):
        other_product_line = product_line_factory.build(sku=product_line.sku)
        url = reverse("api:productline-list")
        data = model_to_dict(other_product_line)
        response = admin_api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_product_line_when_unauthenticated(self, api_client, product_line):
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        data = model_to_dict(product_line)
        response = api_client.put(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("field_key, field_value", VALID_PRODUCT_LINE_DATA)
    def test_update_product_line_when_admin_authenticated(
        self, admin_api_client, admin_user, product_line_factory, field_key, field_value
    ):
        product_line = product_line_factory(product__owner=admin_user)
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        data = model_to_dict(product_line)
        data[field_key] = field_value
        response = admin_api_client.put(url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[field_key] == field_value

    @pytest.mark.parametrize("field_key, field_value", INVALID_PRODUCT_LINE_DATA)
    def test_update_product_line_when_invalid_value(
        self, admin_api_client, admin_user, product_line_factory, field_key, field_value
    ):
        product_line = product_line_factory(product__owner=admin_user)
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        data = model_to_dict(product_line)
        data[field_key] = field_value
        response = admin_api_client.put(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field_key in response.data

    def test_update_product_line_when_owner(
        self, auth_api_client, user, product_line_factory
    ):
        product_line = product_line_factory(product__owner=user)
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        data = model_to_dict(product_line)
        response = auth_api_client.put(url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert Decimal(response.data["price"]) == data["price"]

    def test_update_product_line_when_not_owner(
        self, auth_api_client, product_line_factory, user_factory
    ):
        other_user = user_factory(username="other_user")
        product_line = product_line_factory(product__owner=other_user)
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        data = model_to_dict(product_line)
        response = auth_api_client.put(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_product_line_when_unauthenticated(self, api_client, product_line):
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        data = {"price": "99.99"}
        response = api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("field_key, field_value", VALID_PRODUCT_LINE_DATA)
    def test_patch_product_line_when_admin_authenticated(
        self, admin_api_client, product_line, field_key, field_value
    ):
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        data = {field_key: field_value}
        response = admin_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[field_key] == field_value

    @pytest.mark.parametrize("field_key, field_value", INVALID_PRODUCT_LINE_DATA)
    def test_patch_product_line_when_invalid_value(
        self, admin_api_client, product_line, field_key, field_value
    ):
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        data = {field_key: field_value}
        response = admin_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field_key in response.data

    def test_patch_product_line_when_owner(self, auth_api_client, product_line):
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        data = {"price": "99.99"}
        response = auth_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["price"] == data["price"]

    def test_patch_product_line_when_not_owner(
        self, auth_api_client, product_line_factory, user_factory
    ):
        other_user = user_factory(username="other_user")
        product_line = product_line_factory(product__owner=other_user)
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        data = {"price": 99.99}
        response = auth_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_product_line_when_unauthenticated(self, api_client, product_line):
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_product_line_when_admin_authenticated(
        self, admin_api_client, product_line
    ):
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        response = admin_api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_product_line_when_owner(self, auth_api_client, product_line):
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        response = auth_api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_product_line_when_not_owner(
        self, auth_api_client, product_line_factory, user_factory
    ):
        other_user = user_factory(username="other_user")
        product_line = product_line_factory(product__owner=other_user)
        url = reverse("api:productline-detail", kwargs={"sku": product_line.sku})
        response = auth_api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestProductImageEndpoint:
    def test_get_product_image_when_unauthenticated(self, api_client, product_image):
        url = reverse("api:productimage-detail", kwargs={"pk": product_image.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_product_image_when_authenticated(self, auth_api_client, product_image):
        url = reverse("api:productimage-detail", kwargs={"pk": product_image.pk})
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["product"]["id"] == str(product_image.product.id)

    def test_get_product_image_when_admin_authenticated(
        self, admin_api_client, product_image
    ):
        url = reverse("api:productimage-detail", kwargs={"pk": product_image.pk})
        response = admin_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["product"]["id"] == str(product_image.product.id)

    def test_get_product_image_when_dont_exist(self, auth_api_client):
        url = reverse("api:productimage-detail", kwargs={"pk": 999})
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_product_image_when_unauthenticated(
        self, api_client, product_image_factory
    ):
        product_image_factory()
        url = reverse("api:productimage-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_product_image_when_authenticated(
        self, auth_api_client, product_image_factory
    ):
        product_image_factory.create_batch(10)
        url = reverse("api:productimage-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 10
        assert len(response.data["results"]) == 10

    def test_list_product_image_when_dont_exists(self, auth_api_client):
        url = reverse("api:productimage-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert len(response.data["results"]) == 0

    def test_create_product_image_when_unauthenticated(self, api_client, product_image):
        url = reverse("api:productimage-list")
        data = model_to_dict(product_image)
        response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_product_image_when_admin_authenticated(
        self, admin_api_client, admin_user, product_factory, product_image_factory
    ):
        product = product_factory(owner=admin_user)
        product_image = product_image_factory.build(product=product)
        url = reverse("api:productimage-list")
        data = model_to_dict(product_image)
        response = admin_api_client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert str(response.data["product"]) == str(product.id)

    def test_create_product_image_when_owner(
        self, auth_api_client, user, product_factory, product_image_factory
    ):
        product = product_factory(owner=user)
        product_image = product_image_factory.build(product=product)
        url = reverse("api:productimage-list")
        data = model_to_dict(product_image)
        response = auth_api_client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert str(response.data["product"]) == str(product.id)
        assert response.data["alt_text"] == data["alt_text"]

    def test_create_product_image_when_not_owner(
        self, auth_api_client, product_factory, product_image_factory, user_factory
    ):
        other_user = user_factory(username="other_user")
        product = product_factory(owner=other_user)
        product_image = product_image_factory.build(product=product)
        url = reverse("api:productimage-list")
        data = model_to_dict(product_image)
        response = auth_api_client.post(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["product"][0].startswith("You do not own this product.")

    def test_update_product_image_when_unauthenticated(self, api_client, product_image):
        url = reverse("api:productimage-detail", kwargs={"pk": product_image.pk})
        data = model_to_dict(product_image)
        response = api_client.put(url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_product_image_when_admin_authenticated(
        self, admin_api_client, admin_user, product_factory, product_image_factory
    ):
        product = product_factory(owner=admin_user)
        product_image = product_image_factory.create(product=product)
        url = reverse("api:productimage-detail", kwargs={"pk": product_image.pk})
        data = model_to_dict(product_image)
        response = admin_api_client.put(url, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert str(response.data["product"]) == str(product.id)

    def test_update_product_image_when_owner(
        self, auth_api_client, user, product_factory, product_image_factory
    ):
        product = product_factory(owner=user)
        product_image = product_image_factory.create(product=product)
        url = reverse("api:productimage-detail", kwargs={"pk": product_image.pk})
        data = model_to_dict(product_image)
        response = auth_api_client.put(url, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert str(response.data["product"]) == str(product.id)

    def test_update_product_image_when_not_owner(
        self, auth_api_client, product_factory, product_image_factory, user_factory
    ):
        other_user = user_factory(username="other_user")
        product = product_factory(owner=other_user)
        product_image = product_image_factory.create(product=product)
        url = reverse("api:productimage-detail", kwargs={"pk": product_image.pk})
        data = model_to_dict(product_image)
        response = auth_api_client.put(url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_product_image_when_unauthenticated(self, api_client, product_image):
        url = reverse("api:productimage-detail", kwargs={"pk": product_image.pk})
        data = {"product": product_image.product.pk}
        response = api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_product_image_when_admin_authenticated(
        self, admin_api_client, admin_user, product_factory, product_image_factory
    ):
        product = product_factory(owner=admin_user)
        product_image = product_image_factory.create(product=product)
        url = reverse("api:productimage-detail", kwargs={"pk": product_image.pk})
        data = {"alt_text": "new alt text"}
        response = admin_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert str(response.data["product"]) == str(product.id)
        assert response.data["alt_text"] == data["alt_text"]

    def test_patch_product_image_when_owner(
        self, auth_api_client, user, product_factory, product_image_factory
    ):
        product = product_factory(owner=user)
        product_image = product_image_factory.create(product=product)
        url = reverse("api:productimage-detail", kwargs={"pk": product_image.pk})
        data = {"alt_text": "new alt text"}
        response = auth_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert str(response.data["product"]) == str(product.id)
        assert response.data["alt_text"] == data["alt_text"]

    def test_patch_product_image_when_not_owner(
        self, auth_api_client, product_factory, product_image_factory, user_factory
    ):
        other_user = user_factory(username="other_user")
        product = product_factory(owner=other_user)
        product_image = product_image_factory.create(product=product)
        url = reverse("api:productimage-detail", kwargs={"pk": product_image.pk})
        data = {"product": product_image.product.pk}
        response = auth_api_client.patch(url, data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_product_image_when_unauthenticated(self, api_client, product_image):
        url = reverse("api:productimage-detail", kwargs={"pk": product_image.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_product_image_when_admin_authenticated(
        self, admin_api_client, admin_user, product_factory, product_image_factory
    ):
        product = product_factory(owner=admin_user)
        product_image = product_image_factory.create(product=product)
        url = reverse("api:productimage-detail", kwargs={"pk": product_image.pk})
        response = admin_api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_product_image_when_owner(
        self, auth_api_client, user, product_factory, product_image_factory
    ):
        product = product_factory(owner=user)
        product_image = product_image_factory.create(product=product)
        url = reverse("api:productimage-detail", kwargs={"pk": product_image.pk})
        response = auth_api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_product_image_when_not_owner(
        self, auth_api_client, product_factory, product_image_factory, user_factory
    ):
        other_user = user_factory(username="other_user")
        product = product_factory(owner=other_user)
        product_image = product_image_factory.create(product=product)
        url = reverse("api:productimage-detail", kwargs={"pk": product_image.pk})
        response = auth_api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
