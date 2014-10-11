'''
Created on Oct 11, 2014

@author: nanaya
'''
from rest_framework import serializers
import models


class RelationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Relation
        fields = ('url', 'user', 'to_user', 'description', 'created', 'updated')
        read_only_fields = ('user', 'to_user', 'created', 'updated')


class OutgoingRelationSerializer(serializers.HyperlinkedModelSerializer):

    opposite = serializers.IntegerField(required=False, default=0)

    class Meta:
        model = models.Relation
        fields = ('url', 'user', 'to_user', 'description', 'created', 'updated')
        read_only_fields = ('created', 'updated')


class IncomingRelationSerializer(serializers.HyperlinkedModelSerializer):

    opposite = serializers.IntegerField(required=False, default=-1)

    class Meta:
        model = models.Relation
        fields = ('url', 'user', 'to_user', 'description', 'created', 'updated')
        read_only_fields = ('created', 'updated')


