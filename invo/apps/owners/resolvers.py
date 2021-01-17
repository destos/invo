from rest_framework.permissions import BasePermission, IsAuthenticated


class SitePermission(BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class OwnerResolverMixin:
    permission_classes = [IsAuthenticated & SitePermission]
