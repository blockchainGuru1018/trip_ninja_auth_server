from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from common.exception import CustomException
from teams.models import Team, Agency
from users.models import User
from common.models import CommonParameters


class TeamSerializer(serializers.ModelSerializer):
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


class AgencySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    amadeus_branded_fares = serializers.BooleanField(required=False)
    api_username = serializers.CharField(required=False)
    api_password = serializers.CharField(required=False)
    style_group = serializers.CharField(required=False)
    is_iframe = serializers.BooleanField(required=False)
    student_and_youth = serializers.BooleanField(required=False)
    common_parameter_id = serializers.IntegerField(required=False)
    admin_id = serializers.IntegerField(required=False)

    default_error_messages = {
        'invalid_name': _('name is invalid.'),
        'invalid_amadeus_branded_fares': _('amadeus_branded_fares is invalid.'),
        'invalid_api_username': _('api_username is invalid.'),
        'invalid_api_password': _('api_password is invalid.'),
        'invalid_style_group': _('style_group is invalid.'),
        'invalid_is_iframe': _('is_iframe is invalid.'),
        'invalid_student_and_youth': _('student_and_youth is invalid.'),
        'invalid_common_parameter': _('Common_parameter is invalid.'),
        'invalid_admin': _('Admin is invalid.'),
        'invalid_request': _('Request is invalid.')
    }

    class Meta:
        model = Team
        fields = ("name", "amadeus_branded_fares", "api_username", "api_password", "style_group", "is_iframe",
                  "student_and_youth", "common_parameter_id", "admin_id")

    def validate(self, attrs):
        name = attrs.get("name")
        amadeus_branded_fares = attrs.get("amadeus_branded_fares")
        api_username = attrs.get("api_username")
        api_password = attrs.get("api_password")
        style_group = attrs.get("style_group")
        is_iframe = attrs.get("is_iframe")
        student_and_youth = attrs.get("student_and_youth")
        common_parameter_id = attrs.get("common_parameter_id")
        admin_id = attrs.get("admin_id")

        if not name:
            raise CustomException(code=10, message=self.error_messages['invalid_name'])
        if not amadeus_branded_fares:
            raise CustomException(code=11, message=self.error_messages['invalid_amadeus_branded_fares'])
        if not api_username:
            raise CustomException(code=12, message=self.error_messages['invalid_api_username'])
        if not api_password:
            raise CustomException(code=13, message=self.error_messages['invalid_api_password'])
        if not style_group:
            raise CustomException(code=14, message=self.error_messages['invalid_style_group'])
        if not is_iframe:
            raise CustomException(code=15, message=self.error_messages['invalid_is_iframe'])
        if not student_and_youth:
            raise CustomException(code=16, message=self.error_messages['invalid_student_and_youth'])
        if not common_parameter_id:
            raise CustomException(code=17, message=self.error_messages['invalid_common_parameter'])
        if not admin_id:
            raise CustomException(code=18, message=self.error_messages['invalid_admin'])

        try:
            admin = User.objects.get(id=admin_id)
            common_parameter = CommonParameters.objects.get(id=common_parameter_id)
            attrs['admin'] = admin
            attrs['common_parameter'] = common_parameter
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=19, message=self.error_messages['invalid_request'])
