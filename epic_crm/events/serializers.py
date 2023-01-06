from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Event
from epic_crm.users.models import UserRole
from epic_crm.contracts.models import Contract
from epic_crm.users.serializers import UserSerializerList
from epic_crm.contracts.serializers import ContractSerializerList


class EventSerializerList(ModelSerializer):

    class Meta:
        model = Event
        fields = ['pk', 'name', 'date', 'contract']


class EventSerializerDetails(ModelSerializer):

    contract = ContractSerializerList()
    technical_support = UserSerializerList()

    class Meta:
        model = Event
        fields = ['pk', 'name', 'date', 'date_updated', 'date_created',
                  'informations', 'contract', 'technical_support']


class EventSerializerCreateByManager(ModelSerializer):

    class Meta:
        model = Event
        fields = ['pk', 'name', 'date', 'informations', 'contract', 'technical_support']

    def validate_technical_support(self, value):
        if value.role is None or value.role == UserRole.Roles.TECH_SUPPORT:
            return value

        raise ValidationError("Only users with the role 'Technical support' are valid")


class EventSerializerCreateBySalesPerson(ModelSerializer):

    class Meta:
        model = Event
        fields = ['pk', 'name', 'date', 'informations', 'contract']


class EventSerializerUpdateBySalesperson(ModelSerializer):

    class Meta:
        model = Event
        fields = ['pk', 'name', 'date', 'informations']
