from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models

from common.models import CommonParameters
from teams.models import Agency, Team


class UserLayer(models.Model):
    class Meta:
        db_table = 'users_layer'
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.pk


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'user'

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=20)
    user_type = models.ForeignKey(UserLayer, on_delete=models.CASCADE, related_name='user_Layer', null=True) # delete
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='user_agency', null=True) 
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='user_teams', null=True) # remove deletion cascading
    common_parameters = models.OneToOneField(CommonParameters, on_delete=models.CASCADE,
                                             related_name='user_common_parameters')
    is_active = models.BooleanField(default=True)
    is_iframe = models.BooleanField(default=True) # move to agency model
    is_superuser = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    # add is_team_lead bool
    # add is_agency_admin bool
    search_endpoint = models.CharField(max_length=8, default="prod") # use choices in ENDPOINT_CHOICES
    booking_endpoint = models.CharField(max_length=8, default="prod") # use choices in ENDPOINT_CHOICES
    ENDPOINT_CHOICES = [('prod',), ('preprod',)] # break out tuple
    created_at = models.DateTimeField(auto_now_add=True) # duplicate - part of BaseModel
    updated_at = models.DateTimeField(auto_now=True) # duplicate - part of BaseModel

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
