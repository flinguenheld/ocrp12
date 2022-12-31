from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from epic_crm.users.models import User
from epic_crm.contracts.models import Contract


class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.role == User.Roles.MANAGER:
            return True

        raise PermissionDenied('Only managers are authorized to do this request')


class IsTheAssignedSalespersonOrManager(permissions.BasePermission):
    """ Check if the client's contract's event is assigned to the user who is sending the request """

    def has_permission(self, request, view):

        if request.user.role == User.Roles.MANAGER:
            return True

        elif request.user.role == User.Roles.SALESPERSON and 'contract' in request.data:

            contract = Contract.objects.get(pk=request.data['contract'])
            if contract.client.salesperson == request.user:
                return True

        raise PermissionDenied("Only the client assigned salesperson or managers are authorized to do this request")


class IsTheAssignedOrManagerObject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user == obj.contract.client.salesperson or request.user == obj.technical_support or request.user.role == User.Roles.MANAGER:
            return True

        raise PermissionDenied("Only the client assigned salesperson or managers are authorized to do this request")
