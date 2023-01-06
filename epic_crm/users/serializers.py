from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from django.contrib.auth.models import User
from .models import UserRole


class UserRoleSerializer(ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['role']


class UserSerializerCreate(serializers.HyperlinkedModelSerializer):

    role = serializers.ChoiceField(choices=['Manager', 'Salesperson', 'Technical support'], write_only=True)

    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'password', 'first_name', 'last_name', 'role']


class UserSerializerList(ModelSerializer):
    role_of = UserRoleSerializer()

    class Meta:
        model = User
        fields = ['pk', 'username', 'role_of']


class UserSerializerDetails(ModelSerializer):
    role_of = UserRoleSerializer()

    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'email', 'role_of']
