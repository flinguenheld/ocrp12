from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Contract
from epic_crm.users.models import User
from epic_crm.users.serializers import UserSerializerList, UserSerializerDetails
from epic_crm.clients.serializers import ClientSerializerList


class ContractSerializerList(ModelSerializer):

    # salesperson = UserSerializerList()

    class Meta:
        model = Contract
        fields = ['pk', 'client', 'date_signed']


class ContractSerializerDetails(ModelSerializer):

    signatory = UserSerializerList()
    client = ClientSerializerList()

    class Meta:
        model = Contract
        fields = ['pk', 'client', 'signatory', 'date_signed', 'date_created']


class ContractSerializerCreateByManager(ModelSerializer):

    class Meta:
        model = Contract
        fields = ['pk', 'client', 'signatory', 'date_signed']
