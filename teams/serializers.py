from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from common.exception import CustomException
from teams.models import Team, Agency, DataSource
from users.models import User
from common.models import CommonParameters


class TeamCreateSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(required=False)
    is_booking = serializers.BooleanField(required=False)
    members = serializers.ListField(required=False)
    admin_id = serializers.IntegerField(required=False)

    default_error_messages = {
        'invalid_name': _('Name is invalid.'),
        'invalid_booking': _('Booking is invalid.'),
        'invalid_admin': _('Admin is invalid.'),
    }

    class Meta:
        model = Team
        fields = ("team_name", "is_booking", "members", "admin_id")

    def validate(self, attrs):
        name = attrs.get("team_name")
        is_booking = attrs.get("is_booking")
        admin_id = attrs.get("admin_id")

        if not name:
            raise CustomException(code=10, message=self.error_messages['invalid_name'])
        if is_booking is None:
            raise CustomException(code=12, message=self.error_messages['invalid_booking'])
        return attrs


class AgencyAddSerializer(serializers.ModelSerializer):
    agency_name = serializers.CharField(required=True)
    admin_id = serializers.IntegerField(required=False)
    api_username = serializers.CharField(required=False)
    api_password = serializers.CharField(required=False)
    data_source = serializers.ListField(required=False)

    default_error_messages = {
        'invalid_name': _('name is invalid.'),
        'invalid_api_username': _('api_username is invalid.'),
        'invalid_data_source_id': _('data_source_id is invalid.'),
    }

    class Meta:
        model = Team
        fields = ("agency_name", "api_username", "admin_id", "api_password", "data_source")

    def validate(self, attrs):
        agency_name = attrs.get("agency_name")
        admin_id = attrs.get("admin_id")
        api_username = attrs.get("api_username")
        api_password = attrs.get("api_password")

        if not agency_name:
            raise CustomException(code=10, message=self.error_messages['invalid_name'])
        if not api_username:
            raise CustomException(code=11, message=self.error_messages['invalid_api_username'])
        if not api_password:
            raise CustomException(code=12, message=self.error_messages['invalid_api_password'])

        return attrs


class TeamSerializer(serializers.Serializer):
    team_id = serializers.IntegerField(required=False)

    default_error_messages = {
        'invalid_team': _('Team not found.'),
        'empty_team_id': _('team_id is required.'),
    }

    def validate(self, attrs):
        team_id = attrs.get("team_id")

        if not team_id:
            raise CustomException(code=10, message=self.error_messages['empty_team_id'])

        try:
            attrs['team'] = Team.objects.get(id=team_id)
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=11, message=self.error_messages['invalid_team'])


class TeamUpdateSerializer(serializers.ModelSerializer):
    team_id = serializers.IntegerField(required=False)
    team_name = serializers.CharField(required=False)
    is_booking = serializers.BooleanField(required=False)
    admin_id = serializers.IntegerField(required=False)
    members = serializers.ListField(required=False)

    default_error_messages = {
        'invalid_team_id': _('team_id is invalid.'),
        'invalid_team_name': _('team_name is invalid.'),
        'invalid_admin_id': _('admin_id is invalid.'),
        'invalid_members': _('members is invalid.'),
        'invalid_is_booking': _('is_booking is invalid.'),
        'invalid_request': _('invalid request.')
    }

    class Meta:
        model = User
        fields = ("team_id", "team_name", "is_booking", "admin_id", "members")

    def validate(self, attrs):
        team_id = attrs.get("team_id")
        team_name = attrs.get("team_name")
        is_booking = attrs.get("is_booking")

        if team_id is None:
            raise CustomException(code=10, message=self.error_messages['invalid_team_id'])
        if team_name is None:
            raise CustomException(code=11, message=self.error_messages['invalid_team_name'])
        if is_booking is None:
            raise CustomException(code=12, message=self.error_messages['invalid_is_booking'])

        try:
            attrs['team'] = Team.objects.get(id=team_id)
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=14, message=self.error_messages['invalid_request'])


class AgencySerializer(serializers.Serializer):
    agency_id = serializers.IntegerField(required=False)

    default_error_messages = {
        'invalid_agency': _('agency not found.'),
        'empty_agency_id': _('agency_id is required.'),
    }

    def validate(self, attrs):
        agency_id = attrs.get("agency_id")

        if not agency_id:
            raise CustomException(code=10, message=self.error_messages['empty_agency_id'])

        try:
            attrs['agency'] = Agency.objects.get(id=agency_id)
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=11, message=self.error_messages['invalid_agency'])


class AgencyUpdateSerializer(serializers.ModelSerializer):
    agency_id = serializers.IntegerField(required=False)
    admin_id = serializers.IntegerField(required=False)
    agency_name = serializers.CharField(required=True)
    api_username = serializers.CharField(required=False)
    api_password = serializers.CharField(required=False)
    data_source = serializers.ListField(required=False)

    default_error_messages = {
        'invalid_agency_id': _('agency_id is invalid.'),
        'invalid_name': _('name is invalid.'),
        'invalid_api_username': _('api_username is invalid.'),
    }

    class Meta:
        model = Team
        fields = ("agency_id", "agency_name", "admin_id", "api_username", "api_password", "data_source")

    def validate(self, attrs):
        agency_id = attrs.get("agency_id")
        agency_name = attrs.get("agency_name")
        admin_id = attrs.get("admin_id")
        api_username = attrs.get("api_username")
        api_password = attrs.get("api_password")

        if not agency_id:
            raise CustomException(code=10, message=self.error_messages['invalid_agency_id'])
        if not agency_name:
            raise CustomException(code=11, message=self.error_messages['invalid_name'])
        if not api_username:
            raise CustomException(code=12, message=self.error_messages['invalid_api_username'])
        if not api_password:
            raise CustomException(code=13, message=self.error_messages['invalid_api_password'])

        try:
            agency = Agency.objects.get(id=agency_id)
            attrs['agency'] = agency
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=14, message=self.error_messages['invalid_data_source_id'])