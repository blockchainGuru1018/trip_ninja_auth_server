# from django.utils.translation import ugettext_lazy as _
# from django.core.exceptions import ObjectDoesNotExist
# from rest_framework import serializers
#
# from common.exception import CustomException
# from teams.models import Team
#
#
# class TeamDetailSerializer(serializers.ModelSerializer):
#     team_id = serializers.IntegerField(required=False)
#
#     default_error_messages = {
#         'invalid_team': _('Team_id is invalid.'),
#     }
#
#     class Meta:
#         model = Team
#         fields = ("team_id",)
#
#     def validate(self, attrs):
#         team_id = attrs.get("team_id")
#
#         if not team_id:
#             raise CustomException(code=10, message=self.error_messages['invalid_team'])
#
#         try:
#             attrs['team'] = Team.objects.get(id=team_id)
#             return attrs
#         except ObjectDoesNotExist:
#             raise CustomException(code=10, message=self.error_messages['invalid_team'])
