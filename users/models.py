from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from common.models import CommonParameters
from teams.models import Agency, Team


class UserLayer(models.Model):
    class Meta:
        db_table = 'User_Layer'
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.pk


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    user_type = models.ForeignKey(UserLayer, on_delete=models.CASCADE, related_name='userlayer')
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='agency')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='agency')
    common_parameters = models.OneToOneField(CommonParameters, on_delete=models.CASCADE, related_name='agency')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    search_endpoint = models.CharField(max_length=8, default="prod")
    booking_endpoint = models.CharField(max_length=8, default="prod")
    ENDPOINT_CHOICES = [('prod',), ('preprod',)]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email