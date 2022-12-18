from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import PasswordField

from .models import User


class UserSerializerCreate(ModelSerializer):

    password = PasswordField()

    class Meta:
        model = User
        fields = ['pk', 'email', 'password', 'first_name', 'last_name', 'role']

    def validate_password(self, password):
        if validate_password(password) is None:  # Raise a ValidationError with messages
            return make_password(password)


class UserSerializer(ModelSerializer):
    """ Simple serializer, used to display user in nested serializers """

    class Meta:
        model = User
        fields = ['pk', 'email']


class UserSerializerList(ModelSerializer):
    class Meta:
        model = User
        fields = ['role', 'email', 'pk']


class UserSerializerDetails(ModelSerializer):
    class Meta:
        model = User
        fields = ['role', 'first_name', 'last_name', 'email', 'pk']
