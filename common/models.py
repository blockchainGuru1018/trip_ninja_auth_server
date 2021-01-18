from django.db import models
from django.db.models import *


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CommonParameters(models.Model):
    class Meta:
        db_table = 'common_parameters'

    currency = models.CharField(max_length=3)
    date_type = models.CharField(max_length=10)
    booking_enabled = models.BooleanField(default=True)
    virtual_interlining = models.BooleanField(default=True)
    view_pnr_pricing = models.BooleanField(default=True)
    amadeus_branded_fares = models.BooleanField(default=False)
    markup = models.BooleanField(default=True)
    markup_visible = models.BooleanField(default=False)
    markup_by_itinerary = models.BooleanField(default=False)
    consolidate_ticket = models.BooleanField(default=False)
    exclude_carriers = JSONField(max_length=255, default=dict, blank=True)
    DATE_CHOICES = ("USA", "UK", "CAD", "INR")

    def __str__(self):
        return self.pk
