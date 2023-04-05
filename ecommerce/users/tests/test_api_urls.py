import pytest
from django.urls import resolve, reverse

from ecommerce.users.models import User

pytestmark = [pytest.mark.django_db]


class TestUrls:
    def test_user_detail(self, user: User):
        assert (
            reverse("api:user-detail", kwargs={"username": user.username})
            == f"/api/users/{user.username}/"
        )
        assert resolve(f"/api/users/{user.username}/").view_name == "api:user-detail"

    def test_user_me(self):
        assert reverse("api:user-me") == "/api/users/me/"
        assert resolve("/api/users/me/").view_name == "api:user-me"
