from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from epic_crm.users.models import User


class IsSalesPersonOrManager(permissions.BasePermission):

    # def has_permission(self, request, view):

        # if request.user.role == User.Roles.SALESPERSON or request.user.role == User.Roles.MANAGER:
            # return True

        # raise PermissionDenied('Only salespeople or managers are authorized to do this request')

    def has_object_permission(self, request, view, obj):

        if request.user.pk == obj.salesperson.pk or request.user.role == User.Roles.MANAGER:
            return True
        else:
            raise PermissionDenied("Only the assigned salesperson or managers are authorized to do this request")
