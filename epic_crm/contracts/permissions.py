from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from epic_crm.users.models import UserRole
from epic_crm.clients.models import Client


class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.role == UserRole.Roles.MANAGER:
            return True

        raise PermissionDenied('Only managers are authorized to do this request')


class IsTheAssignedSalespersonOrManager(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.role == UserRole.Roles.MANAGER:
            return True

        elif request.user.role == UserRole.Roles.SALESPERSON and 'client' in request.data:

            client = Client.objects.get(pk=request.data['client'])
            if client.salesperson == request.user:
                return True

        raise PermissionDenied("Only the assigned salesperson or managers are authorized to do this request")


class IsTheAssignedSalespersonOrManagerObject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user == obj.client.salesperson or request.user.role == UserRole.Roles.MANAGER:
            return True

        raise PermissionDenied("Only the assigned salesperson or managers are authorized to do this request")
