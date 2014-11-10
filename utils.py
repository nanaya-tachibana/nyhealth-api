'''
Created on Nov 8, 2014

@author: nanaya
'''
from django.utils import timezone

from six import string_types
from django.utils.importlib import import_module


def import_callable(path_or_callable):
    if hasattr(path_or_callable, '__call__'):
        return path_or_callable
    else:
        assert isinstance(path_or_callable, string_types)
        package, attr = path_or_callable.rsplit('.', 1)
        return getattr(import_module(package), attr)


def three_month_ago():
    return timezone.now() - timezone.timedelta(weeks=12)
