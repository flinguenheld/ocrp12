from rest_framework import mixins
from rest_framework import viewsets

from . import serializers
from django.contrib.auth.models import User
from .models import UserRole

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
        return User.objects.exclude(is_superuser=True).order_by('username')

    def get_serializer_class(self):

        match self.action:
            case 'list':
                return serializers.UserSerializerList

            case 'retrieve':
                return serializers.UserSerializerDetails

            case 'create' | 'update':
                return serializers.UserSerializerCreate

    def perform_create(self, serializer):

        new_user = User.objects.create_user(username=serializer.validated_data['username'],
                                            password=serializer.validated_data['password'],
                                            email=serializer.validated_data['email'],
                                            first_name=serializer.validated_data['first_name'],
                                            last_name=serializer.validated_data['last_name'])
        new_user.save()

        role = UserRole.objects.create(user=new_user, role=serializer.validated_data['role'])
        role.save()

    def perform_update(self, serializer):

        # print(serializer.validated_data)
        # user = self.instance

        user = self.get_object()

        user.username = serializer.validated_data['username']
        user.email = serializer.validated_data['email']
        user.password = serializer.validated_data['password']
        user.first_name = serializer.validated_data['first_name']
        user.last_name = serializer.validated_data['last_name']
        user.save()

        user_role = user.role_of
        user_role.role = serializer.validated_data['role']
        user_role.save()

        serializer.save()
