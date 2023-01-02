from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Contract
from epic_crm.users.models import User
from epic_crm.users.serializers import UserSerializerList
from epic_crm.clients.serializers import ClientSerializerList


class ContractSerializerList(ModelSerializer):

    # salesperson = UserSerializerList()

    class Meta:
        model = Contract
        fields = ['pk', 'client', 'date_signed', 'amount']


class ContractSerializerDetails(ModelSerializer):

    signatory = UserSerializerList()
    client = ClientSerializerList()

    class Meta:
        model = Contract
        fields = ['pk', 'client', 'signatory', 'date_signed', 'date_created', 'amount']


class ContractSerializerCreateByManager(ModelSerializer):

    class Meta:
        model = Contract
        fields = ['pk', 'client', 'signatory', 'date_signed', 'amount']

    def validate_signatory(self, value):

        if value.role is None or value.role == User.Roles.SALESPERSON:
            return value

        raise ValidationError("Only users with the role 'Salesperson' are valid")


class ContractSerializerCreateBySalesperson(ModelSerializer):

    class Meta:
        model = Contract
        fields = ['pk', 'client', 'date_signed', 'amount']


class ContractSerializerUpdateBySalesperson(ModelSerializer):

    class Meta:
        model = Contract
        fields = ['pk', 'date_signed', 'amount']
