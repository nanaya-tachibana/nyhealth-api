from django.conf import settings
from django.db import models

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Profile(models.Model):
    """
    Profile model
    """
    user = models.OneToOneField(
        USER_MODEL, primary_key=True, related_name='profiles')
    profile_photo = models.URLField(default='', blank=True)
    language = models.CharField(max_length=8, default='en')
    timezone = models.CharField(max_length=8, default='UTC')
    location = models.CharField(max_length=32, default='HK')
    birthday = models.DateField('iso-8601', default='1970-01-01')

    class Meta:
        db_table = 'user_profiles'
