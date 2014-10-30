'''
Created on Oct 11, 2014

@author: nanaya
'''
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator

from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework.settings import api_settings

from models import User
from settings.serializers import UserSettingSerializer
from relations.models import Relation
from relations.serializers import (RelationSerializer,
                                   IncomingRelationSerializer,
                                   OutgoingRelationSerializer)
from vitals.serializers import UserMonitoringVitalSerializer


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
    monitorings = \
        serializers.SerializerMethodField('get_monitorings')

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
        fields = ('url', 'auth_token', 'username', 'phone_number',
                  'password', 'settings', 'care_relations',
                  'outgoing_care_relations', 'incoming_care_relations',
                  'monitorings')
        write_only_fields = ('password',)

    def get_pagination_serializer(self, queryset, page_number=1):
        class SerializerClass(api_settings.DEFAULT_PAGINATION_SERIALIZER_CLASS):
            class Meta:
                object_serializer_class = RelationSerializer

        paginator = Paginator(queryset, api_settings.PAGINATE_BY,
                              allow_empty_first_page=True)
        page = paginator.page(paginator.validate_number(page_number))
        return SerializerClass(instance=page, context=self.context)

    def get_confirmed_relations(self, obj):
        relations = obj.relations.filter(opposite__gt=0).order_by('-updated')
        serializer = self.get_pagination_serializer(relations)
        return serializer.data

    def get_outgoing_relations(self, obj):
        relations = obj.relations.filter(opposite=0).order_by('-updated')
        serializer = self.get_pagination_serializer(relations)
        return serializer.data

    def get_incoming_relations(self, obj):
        relations = obj.relations.filter(opposite=-1).order_by('-updated')
        serializer = self.get_pagination_serializer(relations)
        return serializer.data

    def get_monitorings(self, obj):
        monitorings = obj.monitorings.order_by('-updated')
        serializer = self.get_pagination_serializer(monitorings)
        return serializer.data


class UserPublicSerializer(serializers.HyperlinkedModelSerializer):
    """
    Display public information of the user.
    """
    phone_number = serializers.CharField()
    settings = UserSettingSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'settings')


class SubAccountSerializer(serializers.HyperlinkedModelSerializer):
    """
    Display public information of the user.
    """
    phone_number = serializers.CharField()
    settings = UserSettingSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'password')
