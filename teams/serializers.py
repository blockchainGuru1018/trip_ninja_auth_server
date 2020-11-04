from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from common.exception import CustomException
from teams.models import Team, Agency
from users.models import User
from common.models import CommonParameters


class TeamAddSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    agency_id = serializers.IntegerField(required=False)
    admin_id = serializers.IntegerField(required=False)
    common_parameter_id = serializers.IntegerField(required=False)

    default_error_messages = {
        'invalid_name': _('Name is invalid.'),
        'invalid_agency': _('Agency is invalid.'),
        'invalid_admin': _('Admin is invalid.'),
        'invalid_common_parameter': _('Common_parameter is invalid.'),
        'invalid_request': _('Request is invalid.')
    }

    class Meta:
        model = Team
        fields = ("name", "agency_id", "common_parameter_id", "admin_id")

    def validate(self, attrs):
        name = attrs.get("name")
        agency_id = attrs.get("agency_id")
        admin_id = attrs.get("admin_id")
        common_parameter_id = attrs.get("common_parameter_id")

        if not name:
            raise CustomException(code=10, message=self.error_messages['invalid_name'])
        if not agency_id:
            raise CustomException(code=11, message=self.error_messages['invalid_agency'])
        if not admin_id:
            raise CustomException(code=12, message=self.error_messages['invalid_admin'])
        if not common_parameter_id:
            raise CustomException(code=13, message=self.error_messages['invalid_common_parameter'])

        try:
            agency = Agency.objects.get(id=agency_id)
            admin = User.objects.get(id=admin_id)
            common_parameter = CommonParameters.objects.get(id=common_parameter_id)
            attrs['agency'] = agency
            attrs['admin'] = admin
            attrs['common_parameter'] = common_parameter
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=14, message=self.error_messages['invalid_request'])


class TeamUpdateSerializer(serializers.ModelSerializer):
    team_id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    agency_id = serializers.IntegerField(required=False)
    admin_id = serializers.IntegerField(required=False)
    common_parameter_id = serializers.IntegerField(required=False)

    default_error_messages = {
        'invalid_team': _('team_id is invalid.'),
        'invalid_name': _('Name is invalid.'),
        'invalid_agency': _('Agency is invalid.'),
        'invalid_admin': _('Admin is invalid.'),
        'invalid_common_parameter': _('Common_parameter is invalid.'),
        'invalid_request': _('Request is invalid.')
    }

    class Meta:
        model = Team
        fields = ("team_id", "name", "agency_id", "common_parameter_id", "admin_id")

    def validate(self, attrs):
        team_id = attrs.get("team_id")
        name = attrs.get("name")
        agency_id = attrs.get("agency_id")
        admin_id = attrs.get("admin_id")
        common_parameter_id = attrs.get("common_parameter_id")

        if not team_id:
            raise CustomException(code=10, message=self.error_messages['invalid_team'])
        if not name:
            raise CustomException(code=11, message=self.error_messages['invalid_name'])
        if not agency_id:
            raise CustomException(code=12, message=self.error_messages['invalid_agency'])
        if not admin_id:
            raise CustomException(code=13, message=self.error_messages['invalid_admin'])
        if not common_parameter_id:
            raise CustomException(code=14, message=self.error_messages['invalid_common_parameter'])
        try:
            team = Team.objects.get(id=team_id)
            agency = Agency.objects.get(id=agency_id)
            admin = User.objects.get(id=admin_id)
            common_parameter = CommonParameters.objects.get(id=common_parameter_id)
            attrs['team'] = team
            attrs['agency'] = agency
            attrs['admin'] = admin
            attrs['common_parameter'] = common_parameter
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=15, message=self.error_messages['invalid_request'])
