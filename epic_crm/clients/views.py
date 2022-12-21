from rest_framework import mixins
from rest_framework import viewsets

from . import serializers
from .models import Client
from epic_crm.users.models import User

from rest_framework.permissions import IsAuthenticated
from .permissions import IsSalesPersonOrManager


# TODO :
# Add routes or options to list clients with contracts or without it


class UsersViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action != 'retrieve':
            permission_classes.append(IsSalesPersonOrManager)

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

                elif self.request.user.role == User.Roles.SALESPERSON:
                    return serializers.ClientSerializerCreate

    def perform_create(self, serializer):

        if self.request.user.role == User.Roles.SALESPERSON:
            serializer.save(salesperson=self.request.user)

        serializer.save()
