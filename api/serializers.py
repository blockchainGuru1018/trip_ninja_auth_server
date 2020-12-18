from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from datetime import datetime, timedelta
import re

from common.exception import CustomException
from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_email': _('Email is invalid or already taken.'),
        'invalid_username': _(
            'Username may only contain alphanumeric characters, and must be no more than 40 characters.'),
        'invalid_first_name': _('Your first_name is required.'),
        'invalid_last_name': _('Your last_name is required.'),
        'invalid_password': _('Password is invalid.'),
    }

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "password", "phone_number")

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")
        password = attrs.get("password")
        email_re = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

        if not email or not bool(re.match(email_re, email)) or User.objects.filter(email=email).exists():
            raise CustomException(code=11, message=self.error_messages['invalid_email'])
        if username:
            if not bool(re.match('^[a-zA-Z0-9]+$', username)) or len(username) > 40:
                raise CustomException(code=12, message=self.error_messages['invalid_username'])
            elif User.objects.filter(username=username).exists():
                raise CustomException(code=13, message=self.error_messages['invalid_username'])
        if not first_name:
            raise CustomException(code=14, message=self.error_messages['invalid_first_name'])
        if not last_name:
            raise CustomException(code=15, message=self.error_messages['invalid_last_name'])
        if not password or len(password) < 6:
            raise CustomException(code=16, message=self.error_messages['invalid_password'])

        attrs['password'] = make_password(attrs['password'])
        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_username': _('Username or email is required.'),
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.')
    }

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        if not username:
            raise CustomException(code=10, message=self.error_messages['invalid_username'])

        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}

        try:
            self.user = get_user_model().objects.get(**kwargs)
            if self.user.check_password(password):
                if self.user.is_active:
                    attrs['user'] = self.user
                    return attrs
                else:
                    raise CustomException(code=12, message=self.error_messages['inactive_account'])
        except User.DoesNotExist:
            pass
        raise CustomException(code=11, message=self.error_messages['invalid_credentials'])


class ForgotSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_username': _('Username or email is required.'),
    }

    def validate(self, attrs):
        username = attrs.get("username")
        if not username:
            raise CustomException(code=10, message=self.error_messages['invalid_username'])

        return attrs


class ConfirmTokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_token': _('Token is invalid.'),
        'token_expired': _('Reset Token has been expired.'),
        'inactive_account': _('User account is disabled.'),
    }

    def validate(self, attrs):
        token = attrs.get("token")
        if not token or not token.isdigit():
            raise CustomException(code=10, message=self.error_messages['invalid_token'])

        try:
            user = User.objects.get(password_reset_token=int(token))
            if not user.is_active:
                raise CustomException(code=11, message=self.error_messages['inactive_account'])
            if user.password_reset_sent_at.replace(tzinfo=None) < datetime.now() - timedelta(minutes=10):
                raise CustomException(code=12, message=self.error_messages['token_expired'])

            return attrs
        except User.DoesNotExist:
            pass
        raise CustomException(code=10, message=self.error_messages['invalid_token'])


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_token': _('Token is invalid.'),
        'inactive_account': _('User account is disabled.'),
        'invalid_password': _('Password is invalid.'),
    }

    def validate(self, attrs):
        token = attrs.get("token")
        password = attrs.get("password")
        if not token or not token.isdigit():
            raise CustomException(code=10, message=self.error_messages['invalid_token'])
        if not password or len(password) < 6:
            raise CustomException(code=11, message=self.error_messages['invalid_password'])

        try:
            user = User.objects.get(password_reset_token=int(token))
            if user.password_reset_sent_at.replace(tzinfo=None) < datetime.now() - timedelta(minutes=10):
                raise CustomException(code=12, message=self.error_messages['token_expired'])
            if not user.is_active:
                raise CustomException(code=12, message=self.error_messages['inactive_account'])

            attrs['password'] = make_password(attrs['password'])
            return attrs
        except User.DoesNotExist:
            pass
        raise CustomException(code=10, message=self.error_messages['invalid_token'])


class ChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    current_password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_current_password': _('Current_password is incorrect.'),
        'invalid_password': _('Password is invalid.'),
        'invalid_user': _('User is invalid'),
    }

    def validate(self, attrs):
        current_password = attrs.get("current_password")
        new_password = attrs.get("new_password")
        user_id = attrs.get("user_id")

        if not current_password:
            raise CustomException(code=10, message=self.error_messages['invalid_current_password'])
        if not new_password:
            raise CustomException(code=11, message=self.error_messages['invalid_password'])

        user = User.objects.get(pk=user_id)
        if user.check_password(current_password):
            attrs['new_password'] = make_password(attrs['new_password'])
            return attrs
        else:
            raise CustomException(code=10, message=self.error_messages['invalid_current_password'])
