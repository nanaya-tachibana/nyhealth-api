'''
Created on Oct 11, 2014

@author: nanaya
'''
from rest_framework import serializers
import models


class VitalSignSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.VitalSign
        view_name = 'vital-detail'
        fields = ('url', 'id', 'name', 'reference_value')


class UserVitalRecordSerializer(serializers.HyperlinkedModelSerializer):

    vital = serializers.HyperlinkedRelatedField(view_name='vital-detail')
    vital_name = serializers.Field(source='vital.name')

    class Meta:
        model = models.UserVitalRecord
        view_name = 'vital-record-detail'
        read_only_fields = ('user', 'created', 'updated')


class UserMonitoringVitalSerializer(serializers.HyperlinkedModelSerializer):

    vital = serializers.HyperlinkedRelatedField(view_name='vital-detail')
    vital_name = serializers.Field(source='vital.name')

    class Meta:
        model = models.UserMonitoringVital
        view_name = 'monitoring-detail'
        read_only_fields = ('user', 'created', 'updated')
