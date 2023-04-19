import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient, APIRequestFactory

from ecommerce.products.tests.factories import (
    AttributeFactory,
    BrandFactory,
    CategoryFactory,
    ProductAttributeFactory,
    ProductFactory,
    ProductImageFactory,
    ProductLineFactory,
)
from ecommerce.users.models import User
from ecommerce.users.tests.factories import UserFactory

register(BrandFactory)
register(CategoryFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductImageFactory)
register(ProductAttributeFactory)
register(AttributeFactory)
register(UserFactory)


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    """
    Use local media storage for tests.
    """
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
@pytest.mark.django_db
def user(user_factory) -> User:
    """
    A user instance.
    """
    return user_factory(username="testuser")


@pytest.fixture
@pytest.mark.django_db
def admin_user(user_factory) -> User:
    """
    A user instance.
    """
    return user_factory(username="testadminuser", is_staff=True, is_superuser=True)


@pytest.fixture
@pytest.mark.django_db
def api_rf() -> APIRequestFactory:
    """
    A Django RequestFactory instance.
    """ ""
    return APIRequestFactory()


@pytest.fixture
@pytest.mark.django_db
def auth_api_client(user) -> APIClient:
    """
    A Django test client instance autheticated as a user.
    """
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
@pytest.mark.django_db
def admin_api_client(admin_user) -> APIClient:
    """
    A Django test client instance autheticated as a user.
    """
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
@pytest.mark.django_db
def api_client() -> APIClient:
    """
    A Django test client instance.
    """
    return APIClient()
