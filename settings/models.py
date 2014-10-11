from django.db import models

from main.models import User


class Setting(models.Model):
    """
    User's settings.
    """
    user = models.OneToOneField(
        User, primary_key=True, related_name='settings')
    language = models.CharField(max_length=8, default='en')
    timezone = models.CharField(max_length=8, default='UTC')
    location = models.CharField(max_length=8, default='UTC')
    birthday = models.DateField('iso-8601', default='1970-01-01')

    class Meta:
        db_table = 'user_settings'
