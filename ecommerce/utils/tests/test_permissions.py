from unittest.mock import Mock

import pytest
from django.test import RequestFactory

from ecommerce.utils.permissions import (
    IsAuthenticatedReadOnly,
    IsOwner,
    IsOwnerOrReadOnly,
    ReadOnly,
)


class TestPermissions:
    @pytest.mark.parametrize(
        "method, expected_result",
        [
            ("GET", True),
            ("HEAD", True),
            ("OPTIONS", True),
            ("POST", False),
            ("PATCH", False),
            ("PUT", False),
            ("DELETE", False),
        ],
    )
    def test_readonly_permission(
        self, mocker: Mock, api_rf: RequestFactory, method: str, expected_result: bool
    ):
        # Arrange
        request = api_rf.get("/fake-url/", format="json")
        request.method = method
        view = mocker.Mock()
        permission = ReadOnly()

        # Act
        result = permission.has_permission(request, view)

        # Assert
        assert result == expected_result

    @pytest.mark.parametrize(
        "method, is_authenticated, expected_result",
        [
            ("GET", False, False),
            ("HEAD", False, False),
            ("OPTIONS", False, False),
            ("POST", False, False),
            ("PATCH", False, False),
            ("PUT", False, False),
            ("DELETE", False, False),
            ("GET", True, True),
            ("HEAD", True, True),
            ("OPTIONS", True, True),
            ("POST", True, False),
            ("PATCH", True, False),
            ("PUT", True, False),
            ("DELETE", True, False),
        ],
    )
    def test_isauthenticatedreadonly_permission(
        self,
        mocker: Mock,
        api_rf: RequestFactory,
        method: str,
        is_authenticated: bool,
        expected_result: bool,
    ):
        # Arrange
        request = api_rf.get("/fake-url/", format="json")
        request.method = method
        if is_authenticated:
            request.user = mocker.Mock()
            request.user.is_authenticated = is_authenticated
        else:
            request.user = None

        view = mocker.Mock()
        permission = IsAuthenticatedReadOnly()

        # Act
        result = permission.has_permission(request, view)

        # Assert
        assert result == expected_result

    @pytest.mark.parametrize(
        "method, expected_result",
        [
            ("GET", True),
            ("HEAD", True),
            ("OPTIONS", True),
            ("POST", True),
            ("PATCH", True),
            ("PUT", True),
            ("DELETE", True),
        ],
    )
    def test_isownerorreadonly_permission_same_owner(
        self, mocker: Mock, api_rf: RequestFactory, method: str, expected_result: bool
    ):
        # Arrange
        request = api_rf.get("/fake-url/", format="json")
        request.method = method
        request.user = mocker.Mock()
        view = mocker.Mock()
        obj = mocker.Mock()
        obj.owner = request.user
        permission = IsOwnerOrReadOnly()

        # Act
        result = permission.has_object_permission(request, view, obj)

        # Assert
        assert result == expected_result

    @pytest.mark.parametrize(
        "method, expected_result",
        [
            ("GET", True),
            ("HEAD", True),
            ("OPTIONS", True),
            ("POST", False),
            ("PATCH", False),
            ("PUT", False),
            ("DELETE", False),
        ],
    )
    def test_isownerorreadonly_permission_different_owner(
        self, mocker: Mock, api_rf: RequestFactory, method: str, expected_result: bool
    ):
        # Arrange
        request = api_rf.get("/fake-url/", format="json")
        request.method = method
        request.user = mocker.Mock()
        view = mocker.Mock()
        obj = mocker.Mock()
        obj.owner = mocker.Mock()
        permission = IsOwnerOrReadOnly()

        # Act
        result = permission.has_object_permission(request, view, obj)

        # Assert
        assert result == expected_result

    def test_isowner_permission_same_owner(self, mocker: Mock, api_rf: RequestFactory):
        # Arrange
        request = api_rf.get("/fake-url/", format="json")
        request.user = mocker.Mock()
        view = mocker.Mock()
        obj = mocker.Mock()
        obj.owner = request.user
        permission = IsOwner()

        # Act
        result = permission.has_object_permission(request, view, obj)

        # Assert
        assert result

    def test_isowner_permission_different_owner(
        self, mocker: Mock, api_rf: RequestFactory
    ):
        # Arrange
        request = api_rf.get("/fake-url/", format="json")
        request.user = mocker.Mock()
        view = mocker.Mock()
        obj = mocker.Mock()
        obj.owner = mocker.Mock()
        permission = IsOwner()

        # Act
        result = permission.has_object_permission(request, view, obj)

        # Assert
        assert not result

    @pytest.mark.parametrize(
        "get_owner, expected_result",
        [
            (False, False),
            (False, False),
        ],
    )
    def test_isowner_permission_custom_get_owner_false(
        self,
        mocker: Mock,
        api_rf: RequestFactory,
        get_owner: bool,
        expected_result: bool,
    ):
        # Arrange
        request = api_rf.get("/fake-url/", format="json")
        request.user = mocker.Mock()
        view = mocker.Mock()
        obj = mocker.Mock()
        obj.get_owner.return_value = get_owner
        permission = IsOwner()

        # Act
        result = permission.has_object_permission(request, view, obj)

        # Assert
        assert result == expected_result
