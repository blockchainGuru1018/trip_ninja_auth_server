from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
import re

from common.exception import CustomException
from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_email': _('Email is invalid or already taken.'),
        'invalid_first_name': _(
            'Username may only contain alphanumeric characters, and must be no more than 40 characters.'),
        'invalid_last_name': _('Your full name is required.'),
        'invalid_password': _('Password must have at least 6 characters.'),
    }

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password")

    def validate(self, attrs):
        email = attrs.get("email")
        first_name = attrs.get("username")
        last_name = attrs.get("name")
        password = attrs.get("password")
        email_re = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

        if not email or not bool(re.match(email_re, email)) or User.objects.filter(email=email).exists():
            raise CustomException(code=11, message=self.error_messages['invalid_email'])
        if first_name:
            if not bool(re.match('^[a-zA-Z0-9]+$', first_name)) or len(first_name) > 40:
                raise CustomException(code=12, message=self.error_messages['invalid_first_name'])
            elif User.objects.filter(username=first_name).exists():
                raise CustomException(code=15, message=self.error_messages['invalid_first_name'])
        if not last_name:
            raise CustomException(code=13, message=self.error_messages['invalid_last_name'])
        if not password or len(password) < 6:
            raise CustomException(code=14, message=self.error_messages['invalid_password'])

        attrs['password'] = make_password(attrs['password'])
        return attrs