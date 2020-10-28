from django.db import models

from common.models import BaseModel, CommonParameters


class Agency(BaseModel):

    name = models.CharField(max_length=100)
    amadeus_branded_fares = models.BooleanField(default=False)
    api_username = models.CharField(max_length=40, default="trialaccount")
    api_password = models.CharField(max_length=40, default="p#F91Snf#Pr3Yr")
    travelport_itx = models.BooleanField(default=False)
    student_and_youth = models.BooleanField(default=False)
    common_parameters = models.OneToOneField(CommonParameters, on_delete=models.CASCADE,
                                             related_name='agency_common_parameters')

    def __str__(self):
        return self.pk


class DataSource(BaseModel):
    class Meta:
        db_table = 'data_source'

    PROVIDER_CHOICES = [('1A', '1A'), ('1V', '1V'), ('1G', '1G'), ('1P', '1P')]
    name = models.CharField(max_length=40, blank=True)
    pcc = models.CharField(max_length=15, default="2G3C")
    provider = models.CharField(max_length=2, choices=PROVIDER_CHOICES, default="1V")
    active = models.BooleanField(default=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='datasource_agency')
    queue = models.CharField(max_length=40, default="01")


class Team(BaseModel):

    name = models.CharField(max_length=100)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='teams_agency')
    common_parameters = models.OneToOneField(CommonParameters, on_delete=models.CASCADE,
                                             related_name='teams_common_parameters')

    def __str__(self):
        return self.pk