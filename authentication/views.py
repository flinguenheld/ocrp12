from rest_framework import mixins
from rest_framework import viewsets

from . import serializers
from .models import User

from rest_framework.permissions import IsAuthenticated
from .permissions import IsManager


class UsersViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated, IsManager]

    def get_queryset(self):
        users = User.objects.exclude(is_superuser=True, is_staff=True)
        return users

    def get_serializer_class(self):

        match self.action:
            case 'list':
                return serializers.UsersSerializer

            case 'retrieve':
                return serializers.UserSerializerDetails

            case 'create':
                return serializers.UserSerializerCreate
