from rest_framework.serializers import ModelSerializer

from .models import Client
from users.serializers import UserSerializerList


class ClientSerializerList(ModelSerializer):

    salesperson = UserSerializerList()

    class Meta:
        model = Client
        fields = ['pk', 'name', 'salesperson']
