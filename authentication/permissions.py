from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from .models import User


class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.role == User.Roles.MANAGER:
            return True

        user = get_object_or_404(User, pk=view.kwargs['pk'])
        if user.role == User.Roles.MANAGER:
            return True
        else:
            raise PermissionDenied('Only managers are authorized')
