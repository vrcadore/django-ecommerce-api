import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = [pytest.mark.django_db, pytest.mark.e2e]


class TestCategoryEndpoint:
    def test_get_category_unauthenticated(self, api_client, category):
        url = reverse("api:category-detail", kwargs={"slug": category.slug})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_category_authenticated(self, auth_api_client, category):
        url = reverse("api:category-detail", kwargs={"slug": category.slug})
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == category.name

    def test_get_category_admin_authenticated(self, admin_api_client, category):
        url = reverse("api:category-detail", kwargs={"slug": category.slug})
        response = admin_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == category.name

    def test_get_category_not_found(self, auth_api_client):
        url = reverse("api:category-detail", kwargs={"slug": "fake-slug"})
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_category_unauthenticated(self, api_client):
        url = reverse("api:category-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_category_not_found(self, auth_api_client):
        url = reverse("api:category-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0

    def test_list_category_with_deactivated_entries(
        self, auth_api_client, category_factory, category
    ):
        category_factory.create_batch(10, is_active=False)
        url = reverse("api:category-list")
        response = auth_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["slug"] == category.slug


#     def test_create_category(self, api_client, category_factory):
#         url = reverse("api:category-list")
#         data = category_factory.attributes()
#         response = api_client.post(url, data=data)
#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data["name"] == data["name"]

#     def test_update_category(self, api_client, category_factory, category):
#         url = reverse("api:category-detail", kwargs={"pk": category.pk})
#         data = category_factory.attributes()
#         response = api_client.patch(url, data=data)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["name"] == data["name"]

#     def test_delete_category(self, api_client, category):
#         url = reverse("api:category-detail", kwargs={"pk": category.pk})
#         response = api_client.delete(url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT


# @pytest.mark.e2e
# class TestBrandEndpoint:
#     def test_get_brand(self, api_client, brand):
#         url = reverse("api:brand-detail", kwargs={"pk": brand.pk})
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["name"] == brand.name

#     def test_get_brand_not_found(self, api_client):
#         url = reverse("api:brand-detail", kwargs={"pk": 999})
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_404_NOT_FOUND

#     def test_list_brand(self, api_client, brand):
#         url = reverse("api:brand-list")
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#         assert response.data[0]["name"] == brand.name

#     def test_list_brand_not_found(self, api_client):
#         url = reverse("api:brand-list")
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 0

#     def test_list_brand_with_deactivated_entries(
#         self, api_client, brand_factory, brand
#     ):
#         brand_factory.create_batch(10, is_active=True)
#         url = reverse("api:brand-list")
#         response = api_client.get(url, data={"name": brand.name})
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#         assert response.data[0]["name"] == brand.name

#     def test_create_brand(self, api_client, brand_factory):
#         url = reverse("api:brand-list")
#         data = brand_factory.attributes()
#         response = api_client.post(url, data=data)
#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data["name"] == data["name"]

#     def test_update_brand(self, api_client, brand_factory, brand):
#         url = reverse("api:brand-detail", kwargs={"pk": brand.pk})
#         data = brand_factory.attributes()
#         response = api_client.patch(url, data=data)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["name"] == data["name"]

#     def test_delete_brand(self, api_client, brand):
#         url = reverse("api:brand-detail", kwargs={"pk": brand.pk})
#         response = api_client.delete(url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT


# @pytest.mark.e2e
# class TestAttributeEndpoint:
#     def test_get_attribute(self, api_client, attribute):
#         url = reverse("api:attribute-detail", kwargs={"pk": attribute.pk})
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["name"] == attribute.name

#     def test_get_attribute_not_found(self, api_client):
#         url = reverse("api:attribute-detail", kwargs={"pk": 999})
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_404_NOT_FOUND

#     def test_list_attribute(self, api_client, attribute):
#         url = reverse("api:attribute-list")
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#         assert response.data[0]["name"] == attribute.name

#     def test_list_attribute_not_found(self, api_client):
#         url = reverse("api:attribute-list")
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 0

#     def test_list_attribute_with_deactivated_entries(
#         self, api_client, attribute_factory, attribute
#     ):
#         attribute_factory.create_batch(10, is_active=True)
#         url = reverse("api:attribute-list")
#         response = api_client.get(url, data={"name": attribute.name})
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#         assert response.data[0]["name"] == attribute.name

#     def test_create_attribute(self, api_client, attribute_factory):
#         url = reverse("api:attribute-list")
#         data = attribute_factory.attributes()
#         response = api_client.post(url, data=data)
#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data["name"] == data["name"]

#     def test_update_attribute(self, api_client, attribute_factory, attribute):
#         url = reverse("api:attribute-detail", kwargs={"pk": attribute.pk})
#         data = attribute_factory.attributes()
#         response = api_client.patch(url, data=data)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["name"] == data["name"]

#     def test_delete_attribute(self, api_client, attribute):
#         url = reverse("api:attribute-detail", kwargs={"pk": attribute.pk})
#         response = api_client.delete(url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT


# @pytest.mark.e2e
# class TestProductEndpoint:
#     def test_get_product(self, api_client, product):
#         url = reverse("api:product-detail", kwargs={"pk": product.pk})
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["name"] == product.name

#     def test_get_product_not_found(self, api_client):
#         url = reverse("api:product-detail", kwargs={"pk": 999})
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_404_NOT_FOUND

#     def test_list_product(self, api_client, product):
#         url = reverse("api:product-list")
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#         assert response.data[0]["name"] == product.name

#     def test_list_product_not_found(self, api_client):
#         url = reverse("api:product-list")
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 0

#     def test_list_product_with_deactivated_entries(
#         self, api_client, product_factory, product
#     ):
#         product_factory.create_batch(10, is_active=True)
#         url = reverse("api:product-list")
#         response = api_client.get(url, data={"name": product.name})
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#         assert response.data[0]["name"] == product.name

#     def test_create_product(self, api_client, product_factory):
#         url = reverse("api:product-list")
#         data = product_factory.attributes()
#         response = api_client.post(url, data=data)
#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data["name"] == data["name"]

#     def test_update_product(self, api_client, product_factory, product):
#         url = reverse("api:product-detail", kwargs={"pk": product.pk})
#         data = product_factory.attributes()
#         response = api_client.patch(url, data=data)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["name"] == data["name"]

#     def test_delete_product(self, api_client, product):
#         url = reverse("api:product-detail", kwargs={"pk": product.pk})
#         response = api_client.delete(url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT


# @pytest.mark.e2e
# class TestProductLineEndpoint:
#     def test_get_product_line(self, api_client, product_line):
#         url = reverse("api:product-line-detail", kwargs={"pk": product_line.pk})
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["name"] == product_line.name

#     def test_get_product_line_not_found(self, api_client):
#         url = reverse("api:product-line-detail", kwargs={"pk": 999})
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_404_NOT_FOUND

#     def test_list_product_line(self, api_client, product_line):
#         url = reverse("api:product-line-list")
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#         assert response.data[0]["name"] == product_line.name

#     def test_list_product_line_not_found(self, api_client):
#         url = reverse("api:product-line-list")
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 0

#     def test_list_product_line_with_deactivated_entries(
#         self, api_client, product_line_factory, product_line
#     ):
#         product_line_factory.create_batch(10, is_active=True)
#         url = reverse("api:product-line-list")
#         response = api_client.get(url, data={"name": product_line.name})
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#         assert response.data[0]["name"] == product_line.name

#     def test_create_product_line(self, api_client, product_line_factory):
#         url = reverse("api:product-line-list")
#         data = product_line_factory.attributes()
#         response = api_client.post(url, data=data)
#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data["name"] == data["name"]

#     def test_update_product_line(self, api_client, product_line_factory, product_line
# ):
#         url = reverse("api:product-line-detail", kwargs={"pk": product_line.pk})
#         data = product_line_factory.attributes()
#         response = api_client.patch(url, data=data)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["name"] == data["name"]

#     def test_delete_product_line(self, api_client, product):
#         url = reverse("api:product-line-detail", kwargs={"pk": product.pk})
#         response = api_client.delete(url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT
