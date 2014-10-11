'''
Created on Oct 11, 2014

@author: nanaya
'''
from rest_framework import serializers
import models


class VitalSignSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.VitalSign
        fields = ('url', 'name', 'reference_value')


class UserVitalRecordSerializer(serializers.HyperlinkedModelSerializer):

    vital_name = serializers.Field(source='vital.name')

    class Meta:
        model = models.UserVitalRecord
        read_only_fields = ('user', 'created', 'updated')


class UserMonitoringVitalSerializer(serializers.HyperlinkedModelSerializer):

    vital_name = serializers.Field(source='vital.name')

    class Meta:
        model = models.UserMonitoringVital
        read_only_fields = ('user', 'created', 'updated')
