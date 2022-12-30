from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Event
from epic_crm.users.models import User
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


# class EventSerializerCreateByManager(ModelSerializer):

    # class Meta:
        # model = Event
        # fields = ['pk', 'client', 'signatory', 'date_signed', 'amount']

    # def validate_signatory(self, value):

        # if value.role is None or value.role == User.Roles.SALESPERSON:
            # return value

        # raise ValidationError("Only users with the role 'Salesperson' are valid")


# class EventSerializerCreateBySalesperson(ModelSerializer):

    # class Meta:
        # model = Event
        # fields = ['pk', 'client', 'date_signed', 'amount']


# class EventSerializerUpdateBySalesperson(ModelSerializer):

    # class Meta:
        # model = Event
        # fields = ['pk', 'date_signed', 'amount']
