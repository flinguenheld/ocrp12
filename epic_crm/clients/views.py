from rest_framework import mixins
from rest_framework import viewsets
import django_filters

from . import serializers
from .models import Client
from epic_crm.users.models import User

from rest_framework.permissions import IsAuthenticated
from .permissions import IsTheAssignedSalespersonOrManager, IsSalespersonOrManager, IsManager


class ClientsFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        fields = {
            'name': ['exact', 'contains'],
            'email': ['exact', 'contains'],
        }


class ClientsViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    filterset_class = ClientsFilter

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        match self.action:
            case 'create':
                permission_classes.append(IsSalespersonOrManager)

            case 'update':
                permission_classes.append(IsTheAssignedSalespersonOrManager)

            case 'destroy':
                permission_classes.append(IsManager)

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        clients = Client.objects.all().order_by('name')
        return clients

    def get_serializer_class(self):

        match self.action:
            case 'list':
                return serializers.ClientSerializerList

            case 'retrieve':
                return serializers.ClientSerializerDetails

            case 'create' | 'update':
                if self.request.user.role == User.Roles.MANAGER:
                    return serializers.ClientSerializerCreateByManager

                else:
                    return serializers.ClientSerializerCreate

    def perform_create(self, serializer):

        if self.request.user.role == User.Roles.SALESPERSON:
            serializer.save(salesperson=self.request.user)

        serializer.save()
