'''
Created on Oct 11, 2014

@author: nanaya
'''
from django.contrib.auth.hashers import make_password
from rest_framework.reverse import reverse
from rest_framework import serializers

from models import User
from settings.serializers import UserSettingSerializer
from relations.models import Relation
from relations.serializers import (RelationSerializer, 
                                   IncomingRelationSerializer,
                                   OutgoingRelationSerializer)


class DynamicFieldsHyperlinkedModelSerializer(
        serializers.HyperlinkedModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsHyperlinkedModelSerializer, self).__init__(*args,
                                                                      **kwargs)
        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(DynamicFieldsHyperlinkedModelSerializer):

    phone_number = serializers.CharField()
    auth_token = serializers.Field(source='auth_token.key')
    settings = UserSettingSerializer(read_only=True)
    care_relations = \
        serializers.SerializerMethodField('get_confirmed_relations')
    outgoing_care_relations = \
        serializers.SerializerMethodField('get_outgoing_relations')
    incoming_care_relations = \
        serializers.SerializerMethodField('get_incoming_relations')

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if attrs.get('password', None) is not None:
            attrs['password'] = make_password(attrs['password'])
        return super(UserSerializer, self).restore_object(attrs, instance)

    class Meta:
        model = User
        fields = ('url', 'username', 'phone_number', 'password', 'settings',
                  'care_relations', 'outgoing_care_relations',
                  'incoming_care_relations')
        write_only_fields = ('password',)

    def get_confirmed_relations(self, obj):
        relations = Relation.get_confirmed_relations(obj)
        serializer = RelationSerializer(
            relations, many=True, context=self.context)
        return serializer.data

    def get_outgoing_relations(self, obj):
        relations = Relation.get_outgoing_relations(obj)
        serializer = OutgoingRelationSerializer(
            relations, many=True, context=self.context)
        return serializer.data

    def get_incoming_relations(self, obj):
        relations = Relation.get_incoming_relations(obj)
        serializer = IncomingRelationSerializer(
            relations, many=True, context=self.context)
        return serializer.data
