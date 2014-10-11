'''
Created on Oct 11, 2014

@author: nanaya
'''
from rest_framework import serializers
import models


class UserSettingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Setting
