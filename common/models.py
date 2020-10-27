from django.db import models
from django.contrib.postgres.fields import JSONField


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
    exclude_carriers = JSONField(max_length=255, default=[], blank=True)
    DATE_CHOICES = [('USA',), ('UK',)]

    def __str__(self):
        return self.pk