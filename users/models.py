from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from common.models import CommonParameters
from teams.models import Agency, Team


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'user'

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='user_agency', null=True) 
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='user', null=True)
    common_parameters = models.OneToOneField(CommonParameters, on_delete=models.CASCADE,
                                             related_name='user_common_parameters', null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_team_lead = models.BooleanField(default=False)
    is_agency_admin = models.BooleanField(default=False)
    ENDPOINT_CHOICES = [("prod", "prod"), ("preprod", "preprod")]
    search_endpoint = models.CharField(max_length=8, choices=ENDPOINT_CHOICES, default="preprod")
    booking_endpoint = models.CharField(max_length=8, choices=ENDPOINT_CHOICES, default="preprod")
    password_reset_token = models.CharField(null=True, max_length=100)
    password_reset_sent_at = models.DateTimeField(null=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
