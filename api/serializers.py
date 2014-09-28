# -*- coding: utf-8 -*-
from django.contrib.auth.hashers import make_password
from rest_framework.reverse import reverse
from rest_framework import serializers

from main import models


###############################################################################
#  custom fields
###############################################################################
class UseridPkHyperlinkedIdentityField(
        serializers.HyperlinkedIdentityField):
    """
    An url field uses user_id and pk to reference the object. 
    """
    def get_url(self, obj, view_name, request, format):
        kwargs = {'pk': obj.pk, 'user_id': obj.user_id}
        return reverse(view_name, kwargs=kwargs, request=request, format=format)

    def get_object(self, queryset, view_name, view_args, view_kwargs):
        pk = view_kwargs['pk']
        user_id = view_kwargs['user_id']
        return queryset.get(pk=pk, user_id=user_id)


###############################################################################
#  custom serializers
###############################################################################

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


######################################################################

class VitalSignSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.VitalSign
        fields = ('url', 'name', 'reference_value')


###############################################################################
#  user related serializers
###############################################################################
class UserSettingSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='user-settings',
                                               lookup_field='user_id')

    class Meta:
        model = models.UserSetting


class UserSerializer(DynamicFieldsHyperlinkedModelSerializer):

    settings = UserSettingSerializer(read_only=True)
    phone_number = serializers.CharField()
    care_relations = \
        serializers.SerializerMethodField('get_confirmed_relations')
    outgoing_care_requests = \
        serializers.SerializerMethodField('get_outgoing_requests')
    incoming_care_requests = \
        serializers.SerializerMethodField('get_incoming_requests')

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if attrs.get('password', None) is not None:
            attrs['password'] = make_password(attrs['password'])
        attrs['settings'] = models.UserSetting()
        return super(UserSerializer, self).restore_object(attrs, instance)

    class Meta:
        model = models.User
        fields = ('url', 'username', 'phone_number', 'password', 'settings',
                  'care_relations', 'outgoing_care_requests',
                  'incoming_care_requests')
        write_only_fields = ('password',)

    def get_confirmed_relations(self, obj):
        relations = models.CareRelation.get_confirmed_relations(obj)
        serializer = CareRelationSerializer(
            relations, many=True, context=self.context)
        return serializer.data

    def get_outgoing_requests(self, obj):
        relations = models.CareRelation.get_outgoing_requests(obj)
        serializer = OutgoingCareRelationSerializer(
            relations, many=True, context=self.context)
        return serializer.data

    def get_incoming_requests(self, obj):
        relations = models.CareRelation.get_incoming_requests(obj)
        serializer = IncomingCareRelationSerializer(
            relations, many=True, context=self.context)
        return serializer.data


class CareRelationSerializer(serializers.HyperlinkedModelSerializer):

    url = UseridPkHyperlinkedIdentityField(
        view_name='care-relation-detail')

    class Meta:
        model = models.CareRelation
        fields = ('url', 'user', 'to_user', 'description', 'created', 'updated')
        read_only_fields = ('user', 'to_user', 'created', 'updated')


class OutgoingCareRelationSerializer(serializers.ModelSerializer):

    url = UseridPkHyperlinkedIdentityField(
        view_name='outgoing-care-relation-detail')
    to_user = serializers.HyperlinkedRelatedField(view_name='user-detail',
                                                  many=False)
    opposite = serializers.IntegerField(required=False, default=0)

    class Meta:
        model = models.CareRelation
        fields = ('url', 'user', 'to_user', 'description', 'created', 'updated')
        read_only_fields = ('created', 'updated')


class IncomingCareRelationSerializer(serializers.ModelSerializer):

    url = UseridPkHyperlinkedIdentityField(
        view_name='incoming-care-relation-detail')
    to_user = serializers.HyperlinkedRelatedField(view_name='user-detail',
                                                  many=False)
    opposite = serializers.IntegerField(required=False, default=-1)

    class Meta:
        model = models.CareRelation
        fields = ('url', 'user', 'to_user', 'description', 'created', 'updated')
        read_only_fields = ('created', 'updated')


class UserVitalSerializer(serializers.HyperlinkedModelSerializer):

    url = UseridPkHyperlinkedIdentityField(view_name='user-vital-detail')
    vital_name = serializers.Field(source='vital.name')

    class Meta:
        model = models.UserVital
        read_only_fields = ('user',)


class UserCaredVitalSerializer(serializers.HyperlinkedModelSerializer):

    url = UseridPkHyperlinkedIdentityField(view_name='user-cared-vital-detail')
    vital_name = serializers.Field(source='vital.name')

    class Meta:
        model = models.UserCaredVital
        read_only_fields = ('user',)
