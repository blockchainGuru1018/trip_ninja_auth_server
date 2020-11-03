from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from common.exception import CustomException

from users.models import User


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
