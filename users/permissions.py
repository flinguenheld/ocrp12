from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from .models import User


class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.role == User.Roles.MANAGER:
            return True

        raise PermissionDenied('Only managers are authorized to do this request')
