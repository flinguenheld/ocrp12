from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Client
from epic_crm.users.models import User
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
        fields = ['pk', 'name', 'address', 'email', 'phone', 'time_created', 'salesperson']


class ClientSerializerCreate(ModelSerializer):
    class Meta:
        model = Client
        fields = ['pk', 'name', 'address', 'email', 'phone']


class ClientSerializerCreateByManager(ModelSerializer):
    class Meta:
        model = Client
        fields = ['pk', 'name', 'address', 'email', 'phone', 'salesperson']

    def validate_salesperson(self, value):

        if value.role is None or value.role == User.Roles.SALESPERSON:
            return value

        raise ValidationError("Only users with the role 'Salesperson' are valid")
