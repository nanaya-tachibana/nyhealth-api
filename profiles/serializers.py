'''
Created on Oct 11, 2014

@author: nanaya
'''
from rest_framework import serializers
import models


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    birthday = serializers.DateField(format='iso-8601')

    class Meta:
        model = models.Profile
        view_name = 'profile-detail'
