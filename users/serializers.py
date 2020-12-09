from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from common.exception import CustomException

from users.models import User
from teams.models import Agency, Team
from common.models import CommonParameters


class GetUserByIdSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)

    default_error_messages = {
        'invalid_user': _('User not found.'),
        'empty_user_id': _('User_id is required.'),
    }

    def validate(self, attrs):
        user_id = attrs.get("user_id")

        if not user_id:
            raise CustomException(code=10, message=self.error_messages['empty_user_id'])

        try:
            attrs['user'] = User.objects.get(id=user_id)
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=10, message=self.error_messages['invalid_user'])


class SingleAddUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    team_id = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)

    default_error_messages = {
        'invalid_email': _('email is invalid.'),
        'invalid_first_name': _('first_name is invalid.'),
        'invalid_last_name': _('last_name is invalid.'),
        'invalid_team': _('team is invalid.'),
        'invalid_is_active': _('is_active is invalid.'),
        'invalid_request': _('Request is invalid.')
    }

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "team_id", "is_active")

    def validate(self, attrs):
        email = attrs.get("email")
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")
        team_id = attrs.get("team_id")

        if not email:
            raise CustomException(code=10, message=self.error_messages['invalid_email'])
        if not first_name:
            raise CustomException(code=12, message=self.error_messages['invalid_first_name'])
        if not last_name:
            raise CustomException(code=13, message=self.error_messages['invalid_last_name'])

        try:
            team = Team.objects.get(id=team_id)
            attrs['team'] = team
            return attrs
        except ObjectDoesNotExist:
            attrs['team'] = None
            return attrs


class BulkAddUserSerializer(serializers.ModelSerializer):
    emails = serializers.ListField(required=False)
    team_id = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)

    default_error_messages = {
        'invalid_is_active': _('is_active is invalid.'),
    }

    class Meta:
        model = User
        fields = ("emails", "team_id", "is_active")

    def validate(self, attrs):
        is_active = attrs.get("is_active")

        if is_active is None:
            raise CustomException(code=11, message=self.error_messages['invalid_is_active'])

        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)
    team_id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)

    default_error_messages = {
        'invalid_user_id': _('user_id is invalid.'),
        'invalid_team_id': _('team_id is invalid.'),
        'invalid_username': _('username is invalid.'),
        'invalid_email': _('email is invalid.'),
        'invalid_phone_number': _('phone_number is invalid.'),
        'invalid_is_active': _('is_active is invalid.'),
    }

    class Meta:
        model = User
        fields = ("user_id", "team_id", "username", "email", "phone_number", "is_active")

    def validate(self, attrs):
        user_id = attrs.get("user_id")
        is_active = attrs.get("is_active")
        username = attrs.get("username")
        email = attrs.get("email")

        if user_id is None:
            raise CustomException(code=10, message=self.error_messages['invalid_user_id'])
        if is_active is None:
            raise CustomException(code=12, message=self.error_messages['invalid_is_active'])
        if username is None:
            raise CustomException(code=13, message=self.error_messages['invalid_username'])
        if email is None:
            raise CustomException(code=14, message=self.error_messages['invalid_email'])

        try:
            attrs['user'] = User.objects.get(id=user_id)
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=15, message=self.error_messages['invalid_user_id'])


class BasicInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=True)
    email_address = serializers.CharField(required=False)
    currency = serializers.CharField(required=False)
    date_type = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_name': _('name is invalid.'),
        'invalid_phone_number': _('phone_number is invalid.'),
        'invalid_email_address': _('email_address is invalid.'),
        'invalid_currency': _('currency is invalid.'),
        'invalid_date_type': _('date_type is invalid.'),
    }

    class Meta:
        model = Team
        fields = ("name", "phone_number", "email_address", "currency", "date_type")

    def validate(self, attrs):
        name = attrs.get("name")
        phone_number = attrs.get("phone_number")
        email_address = attrs.get("email_address")
        currency = attrs.get("currency")
        date_type = attrs.get("date_type")

        if not name:
            raise CustomException(code=10, message=self.error_messages['invalid_name'])
        if not phone_number:
            raise CustomException(code=11, message=self.error_messages['invalid_phone_number'])
        if not email_address:
            raise CustomException(code=12, message=self.error_messages['invalid_email_address'])
        if not currency:
            raise CustomException(code=13, message=self.error_messages['invalid_currency'])
        if not date_type:
            raise CustomException(code=14, message=self.error_messages['invalid_date_type'])

        return attrs


class GeneralInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    currency = serializers.CharField(required=False)
    date_type = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_name': _('name is invalid.'),
        'invalid_currency': _('currency is invalid.'),
        'invalid_date_type': _('date_type is invalid.'),
    }

    class Meta:
        model = Team
        fields = ("name", "currency", "date_type")

    def validate(self, attrs):
        name = attrs.get("name")
        currency = attrs.get("currency")
        date_type = attrs.get("date_type")

        if not name:
            raise CustomException(code=10, message=self.error_messages['invalid_name'])
        if not currency:
            raise CustomException(code=11, message=self.error_messages['invalid_currency'])
        if not date_type:
            raise CustomException(code=12, message=self.error_messages['invalid_date_type'])

        return attrs
