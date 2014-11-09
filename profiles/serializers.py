'''
Created on Oct 11, 2014

@author: nanaya
'''
from rest_framework import serializers
import models


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Profile
        view_name = 'profile-detail'
