from django.db import models

from main.models import User


class VitalSign(models.Model):
    """
    Vital sign.

    `name` ... the name of vital sign
    `reference_value` ... the normal value of vital sign
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
    User's uploaded vital sign records.

    `user` ... the user who uploaded the record
    `vital` ...  the vital sign that the record recorded
    `value` ... value of the vital sign
    `created` .. created time
    `updated` ... last updated time

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

    `user` ... the user who are monitoring
    `vital` ...  the vital sign that are monitored
    `value` ... dangerous level for the vital of the user
    `created` .. created time
    `updated` ... last updated time
    """
    user = models.ForeignKey(User, related_name='monitorings', db_index=True)
    vital = models.ForeignKey(VitalSign)
    level = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(
        auto_now=True, auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'user_monitoring_vitals'
        unique_together = ('user', 'vital')
