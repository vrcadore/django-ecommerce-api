from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class ReadOnly(permissions.BasePermission):
    """
    Global permission check for read-only requests.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        return request.method in SAFE_METHODS


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        owner = None
        if hasattr(obj, "owner"):
            owner = obj.owner
        else:
            get_owner = getattr(obj, "get_owner", None)
            if callable(get_owner):
                owner = get_owner()

        return bool(owner is not None and owner == request.user)


class IsOwnerOrReadOnly(IsOwner):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner` or `get_owner` function.
        return super().has_object_permission(request, view, obj)


class IsAuthenticatedReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user and is a safe method request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        )
