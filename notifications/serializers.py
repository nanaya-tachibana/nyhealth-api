'''
Created on Nov 9, 2014

@author: nanaya
'''
from rest_framework import serializers
from .models import Inbox


class InboxSerializer(serializers.HyperlinkedModelSerializer):

    message_text = serializers.Field(source='message.message')
    level = serializers.Field(source='message.level')
    tags = serializers.Field(source='message.tags')
    date = serializers.SerializerMethodField('get_date')

    class Meta:
        model = Inbox
        view_name = 'inbox-detail'
        fields = ('url', 'id', 'message_text', 'level', 'tags', 'date')

    def get_date(self, obj):
        return obj.message.date.isoformat()
