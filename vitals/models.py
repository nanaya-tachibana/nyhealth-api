from django.db import models

from main.models import User


class VitalSign(models.Model):
    """
    Vital sign.
    """
    name = models.CharField(max_length=60, db_index=True)
    reference_value = models.CharField(max_length=128, default='')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(
        auto_now=True, auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'vitals'


class UserVitalRecord(models.Model):
    """
    User's upload vital sign records.
    """
    user = models.ForeignKey(User, related_name='vitals', db_index=True)
    vital = models.ForeignKey(VitalSign)
    value = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(
        auto_now=True, auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'user_vital_records'


class UserMonitoringVital(models.Model):
    """
    Vitals which are monitored by user.
    """
    user = models.ForeignKey(User, related_name='monitorings', db_index=True)
    vital = models.ForeignKey(VitalSign)
    level = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(
        auto_now=True, auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'user_monitoring_vitals'
