'''
Created on Oct 11, 2014

@author: nanaya
'''
from django.conf.urls import patterns, url

import views


vital_list = views.VitalSignViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
vital_detail = views.VitalSignViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
    'patch': 'partial_update',
})
vital_record_list = views.UserVitalRecordViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
vital_record_detail = views.UserVitalRecordViewSet.as_view({
    'get': 'retrieve',
})
monitoring_list = views.UserMonitoringVitalViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
monitoring_detail = views.UserMonitoringVitalViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = patterns(
    '',
    url(r'^available_vitals/$', vital_list, name='vital-list'),
    url(r'^available_vitals/(?P<pk>[0-9]+)/$',
        vital_detail, name='vital-detail'),
    url(r'^vitals/$', vital_record_list, name='vital-record-list'),
    url(r'^vitals/(?P<pk>[0-9]+)/$',
        vital_record_detail, name='vital-record-detail'),
    url(r'^vitals/monitorings/$', monitoring_list, name='monitoring-list'),
    url(r'^vitals/monitorings/(?P<pk>[0-9]+)/$',
        monitoring_detail, name='monitoring-detail')
)
