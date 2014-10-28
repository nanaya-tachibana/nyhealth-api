'''
Created on Oct 11, 2014

@author: nanaya
'''
from rest_framework import serializers
import models


class RelationSerializer(serializers.HyperlinkedModelSerializer):

    to_username = serializers.Field(source='to_user.username')

    class Meta:
        model = models.Relation
        view_name = 'relation-detail'
        fields = ('url', 'id', 'user', 'to_user', 'to_username',
                  'description', 'created', 'updated')
        read_only_fields = ('user', 'to_user', 'created', 'updated')


class OutgoingRelationSerializer(serializers.HyperlinkedModelSerializer):

    to_username = serializers.Field(source='to_user.username')
    opposite = serializers.IntegerField(required=False, default=0)

    class Meta:
        model = models.Relation
        view_name = 'outgoing-relation-detail'
        fields = ('url', 'id', 'user', 'to_user', 'to_username',
                  'description', 'created', 'updated')
        read_only_fields = ('created', 'updated')


class IncomingRelationSerializer(serializers.HyperlinkedModelSerializer):

    to_username = serializers.Field(source='to_user.username')
    opposite = serializers.IntegerField(required=False, default=-1)

    class Meta:
        model = models.Relation
        view_name = 'incoming-relation-detail'
        fields = ('url', 'id', 'user', 'to_user', 'to_username',
                  'description', 'created', 'updated')
        read_only_fields = ('created', 'updated')
