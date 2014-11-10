'''
Created on Nov 9, 2014

@author: nanaya
'''
from django.conf import settings
from django.db import models
from django.utils import timezone

from .exceptions import MessageTypeNotSupported


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Message(models.Model):
    """
    This model represents a message on the database. Fields are the same as in
    `contrib.messages`
    """
    message = models.TextField()
    level = models.IntegerField()
    tags = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'messages'


class Inbox(models.Model):
    """
    Inbox messages are stored in this model until users read them. Once read,
    inbox messages are deleted. Inbox messages have an expire time, after
    that they could be removed by a proper django command. We do not expect
    database table corresponding to this model to grow much.
    """
    user = models.ForeignKey(USER_MODEL, db_index=True,
                             related_name='messages')
    message = models.ForeignKey(Message)

    class Meta:
        db_table = 'inbox'

    def expired(self):
        expiration_date = self.message.date + timezone.timedelta(days=7)
        return expiration_date <= timezone.now()

    expired.boolean = True  # show a nifty icon in the admin

    def destroy(self):
        self.delete()

    @classmethod
    def restore(cls, user, msg):
        if not isinstance(msg, Message):
            raise MessageTypeNotSupported()
        cls.objects.get_or_create(user=user, message=msg)

    @classmethod
    def delete_all(cls, user):
        cls.objects.filter(user=user).delete()

    @classmethod
    def create_message(cls, level, msg_text, extra_tags=''):
        m_instance = Message.objects.create(message=msg_text, level=level,
                                            tags=extra_tags)
        return m_instance
