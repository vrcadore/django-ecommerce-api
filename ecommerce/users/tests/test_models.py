import pytest

from ecommerce.users.models import User

pytestmark = [pytest.mark.django_db]


class TestUserModels:
    def test_user_str(self, user: User):
        assert str(user) == f"{user.username}"
