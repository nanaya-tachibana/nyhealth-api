'''
Created on Oct 11, 2014

@author: nanaya
'''
from django.conf.urls import patterns, url

import views


setting_detail = views.UserSettingsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'
})


urlpatterns = patterns(
    '',
    url(r'^profiles/(?P<pk>[0-9]+)/$', setting_detail, name='profile-detail'),
)
