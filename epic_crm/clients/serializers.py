from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Client
from epic_crm.users.models import UserRole
from epic_crm.users.serializers import UserSerializerList, UserSerializerDetails


class ClientSerializerList(ModelSerializer):

    salesperson = UserSerializerList()

    class Meta:
        model = Client
        fields = ['pk', 'name', 'salesperson']


class ClientSerializerDetails(ModelSerializer):

    salesperson = UserSerializerDetails()

    class Meta:
        model = Client
        fields = ['pk', 'name', 'address', 'email', 'phone', 'date_created', 'salesperson']


class ClientSerializerCreate(ModelSerializer):
    class Meta:
        model = Client
        fields = ['pk', 'name', 'address', 'email', 'phone']


class ClientSerializerCreateByManager(ModelSerializer):
    class Meta:
        model = Client
        fields = ['pk', 'name', 'address', 'email', 'phone', 'salesperson']

    def validate_salesperson(self, value):

        if value.role_of.role is None or value.role_of.role == UserRole.Roles.SALESPERSON:
            return value

        raise ValidationError("Only users with the role 'Salesperson' are valid")
