# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from users import urls as user_urls
from profiles import urls as setting_urls
from relations import urls as relation_urls
from authorization import urls as auth_urls
from vitals import urls as vital_urls
from notifications import urls as message_urls

urlpatterns = patterns(
    '',
    url(r'^', include(auth_urls)),
    url(r'^', include(user_urls)),
    url(r'^', include(setting_urls)),
    url(r'^', include(relation_urls)),
    url(r'^', include(vital_urls)),
    url(r'^', include(message_urls)),
)
