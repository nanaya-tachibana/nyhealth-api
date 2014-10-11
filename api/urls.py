# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from main import urls as user_urls
from settings import urls as setting_urls
from relations import urls as relation_urls
from vitals import urls as vital_urls

urlpatterns = patterns(
    '',
    url(r'^', include(user_urls)),
    url(r'^', include(setting_urls)),
    url(r'^', include(relation_urls)),
    url(r'^', include(vital_urls)),
)
