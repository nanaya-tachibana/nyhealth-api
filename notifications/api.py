'''
Created on Nov 9, 2014

@author: nanaya
'''
__all__ = (
    'add_message_for', 'broadcast_message',
)

from django.contrib.auth import get_user_model
from .models import Inbox


def add_message_for(users, level, message_text,
                    extra_tags='', fail_silently=False):
    """
    Send a message to a list of users without passing through `django.contrib.messages`
    :param users: an iterable containing the recipients of the messages
    :param level: message level
    :param message_text: the string containing the message
    :param extra_tags: like the Django api, a string containing extra tags for the message
    :param fail_silently: not used at the moment
    """
    m = Inbox.create_message(level, message_text, extra_tags)
    for user in users:
        Inbox.restore(user, m)


def broadcast_message(level, message_text, extra_tags='', fail_silently=False):
    """
    Send a message to all users aka broadcast.
    :param level: message level
    :param message_text: the string containing the message
    :param extra_tags: like the Django api, a string containing extra tags for the message
    :param fail_silently: not used at the moment
    """
    users = get_user_model().objects.all()
    add_message_for(users, level, message_text, extra_tags=extra_tags,
                    fail_silently=fail_silently)
