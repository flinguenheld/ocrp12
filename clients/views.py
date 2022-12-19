from rest_framework import mixins
from rest_framework import viewsets

from . import serializers
from .models import Client
# from users.models import User

from rest_framework.permissions import IsAuthenticated
# from .permissions import IsManager


class UsersViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        clients = Client.objects.all().order_by('name')
        return clients

    def get_serializer_class(self):

        return serializers.ClientSerializerList

        # match self.action:
            # case 'list':
                # return serializers.UserSerializerList

            # case 'retrieve':
                # return serializers.UserSerializerDetails

            # case 'create' | 'update':
                # return serializers.UserSerializerCreate
