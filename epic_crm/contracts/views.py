from rest_framework import mixins
from rest_framework import viewsets

from . import serializers
from .models import Contract
from epic_crm.users.models import User


from rest_framework.permissions import IsAuthenticated
# from .permissions import IsTheAssignedSalespersonOrManager, IsSalespersonOrManager, IsManager
from .permissions import IsTheAssignedSalespersonOrManager, IsManager


class UsersViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        match self.action:
            # case 'create':
                # permission_classes.append(IsTheAssignedSalespersonOrManager)

            case 'update':
                permission_classes.append(IsTheAssignedSalespersonOrManager)

            case 'destroy':
                permission_classes.append(IsManager)

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        contracts = Contract.objects.all().order_by('date_created')
        return contracts

    def get_serializer_class(self):

        match self.action:
            case 'list':
                return serializers.ContractSerializerList

            case 'retrieve':
                return serializers.ContractSerializerDetails

            case 'create':
                if self.request.user.role == User.Roles.MANAGER:
                    return serializers.ContractSerializerCreateByManager

                else:
                    return serializers.ContractSerializerCreateBySalesperson

            case 'update':
                if self.request.user.role == User.Roles.MANAGER:
                    return serializers.ContractSerializerCreateByManager

                else:
                    return serializers.ContractSerializerUpdateBySalesperson

    def perform_create(self, serializer):

        if self.request.user.role == User.Roles.SALESPERSON:

            if serializer.validated_data['client'].salesperson != self.request.user:
                raise serializers.ValidationError("Only the assigned salesperson and managers"
                                                  " are authorized to create a contract")

            serializer.save(signatory=self.request.user)

        serializer.save()
