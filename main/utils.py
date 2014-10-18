'''
Created on Oct 18, 2014

@author: nanaya
'''
from datetime import datetime
from rest_framework.exceptions import ParseError


def strtime_to_datetime(strtime):
    try:
        return datetime.strptime(strtime, '%Y-%m-%d')
    except:
        raise ParseError(
                detail='query param `since` should follow the ISO 8601 style')
