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
            raise CustomException(code=11, message=self.error_messages['invalid_user'])


class AddUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    agency_id = serializers.IntegerField(required=False)
    team_id = serializers.IntegerField(required=False)
    common_parameters_id = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)
    is_superuser = serializers.BooleanField(required=False)
    is_agent = serializers.BooleanField(required=False)
    is_team_lead = serializers.BooleanField(required=False)
    is_agency_admin = serializers.BooleanField(required=False)

    default_error_messages = {
        'invalid_email': _('email is invalid.'),
        'invalid_username': _('username is invalid.'),
        'invalid_first_name': _('first_name is invalid.'),
        'invalid_last_name': _('last_name is invalid.'),
        'invalid_phone_number': _('phone_number is invalid.'),
        'invalid_agency': _('agency is invalid.'),
        'invalid_team': _('team is invalid.'),
        'invalid_common_parameters': _('common_parameters is invalid.'),
        'invalid_is_active': _('is_active is invalid.'),
        'invalid_is_superuser': _('is_superuser is invalid.'),
        'invalid_is_agent': _('is_agent is invalid.'),
        'invalid_is_team_lead': _('is_team_lead is invalid.'),
        'invalid_is_agency_admin': _('is_agency_admin is invalid.'),
        'invalid_request': _('Request is invalid.')
    }

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "phone_number", "agency_id", "team_id",
                  "common_parameters_id", "is_active", "is_superuser", "is_agent", "is_team_lead", "is_agency_admin")

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")
        phone_number = attrs.get("phone_number")
        agency_id = attrs.get("agency_id")
        team_id = attrs.get("team_id")
        is_active = attrs.get("is_active")
        is_superuser = attrs.get("is_superuser")
        is_agent = attrs.get("is_agent")
        is_team_lead = attrs.get("is_team_lead")
        is_agency_admin = attrs.get("is_agency_admin")
        common_parameter_id = attrs.get("common_parameter_id")

        if not email:
            raise CustomException(code=10, message=self.error_messages['invalid_email'])
        if not username:
            raise CustomException(code=11, message=self.error_messages['invalid_username'])
        if not first_name:
            raise CustomException(code=12, message=self.error_messages['invalid_first_name'])
        if not last_name:
            raise CustomException(code=13, message=self.error_messages['invalid_last_name'])
        if not phone_number:
            raise CustomException(code=14, message=self.error_messages['invalid_phone_number'])
        if not agency_id:
            raise CustomException(code=15, message=self.error_messages['invalid_agency'])
        if not team_id:
            raise CustomException(code=16, message=self.error_messages['invalid_team'])
        if not common_parameter_id:
            raise CustomException(code=17, message=self.error_messages['invalid_common_parameters'])
        if not is_active:
            raise CustomException(code=18, message=self.error_messages['invalid_is_active'])
        if not is_superuser:
            raise CustomException(code=19, message=self.error_messages['invalid_is_superuser'])
        if not is_agent:
            raise CustomException(code=20, message=self.error_messages['invalid_is_agent'])
        if not is_team_lead:
            raise CustomException(code=21, message=self.error_messages['invalid_is_team_lead'])
        if not is_agency_admin:
            raise CustomException(code=22, message=self.error_messages['invalid_is_agency_admin'])

        try:
            agency = Agency.objects.get(id=agency_id)
            team = Team.objects.get(id=team_id)
            common_parameter = CommonParameters.objects.get(id=common_parameter_id)
            attrs['agency'] = agency
            attrs['team'] = team
            attrs['common_parameter'] = common_parameter
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=23, message=self.error_messages['invalid_request'])
