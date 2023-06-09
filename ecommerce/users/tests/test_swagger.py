import pytest
from django.urls import reverse
from rest_framework import status


class TestSwagger:
    def test_swagger_accessible_by_admin(self, admin_client):
        url = reverse("api-docs")
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_swagger_ui_accessible_by_anonymous_user(self, client):
        url = reverse("api-docs")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_api_schema_generated_successfully(self, admin_client):
        url = reverse("api-schema")
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
