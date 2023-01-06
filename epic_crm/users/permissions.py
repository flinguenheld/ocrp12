from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from .models import UserRole


class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.role_of.role == UserRole.Roles.MANAGER:
            return True

        raise PermissionDenied('Only managers are authorized to do this request')
