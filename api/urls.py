# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'vitals', views.VitalSignViewSet)
care_relations_list = views.UserCareRelationViewSet.as_view({
    'get': 'list',
})
care_relation_detail = views.UserCareRelationViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})
outgoing_care_relations_list = views.UserOutgoingCareRelationViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
outgoing_care_relation_detail = views.UserOutgoingCareRelationViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
})
incoming_care_relations_list = views.UserIncomingCareRelationViewSet.as_view({
    'get': 'list',
})
incoming_care_relation_detail = views.UserIncomingCareRelationViewSet.as_view({
    'get': 'retrieve',
    'patch': 'allow',
    'delete': 'deny',
})
user_vitals_list = views.UserVitalViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
user_vital_detail = views.UserVitalViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})
user_settings = views.UserSettingsViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^users/(?P<user_id>[0-9]+)/relations/$',
        care_relations_list, name='care-relations-list'),
    url(r'^users/(?P<user_id>[0-9]+)/relations/(?P<pk>[0-9]+)/$',
        care_relation_detail, name='care-relation-detail'),
    url(r'^users/(?P<user_id>[0-9]+)/relations/outgoings/$',
        outgoing_care_relations_list, name='outgoing-care-relations-list'),
    url(r'^users/(?P<user_id>[0-9]+)/relations/outgoings/(?P<pk>[0-9]+)/$',
        outgoing_care_relation_detail, name='outgoing-care-relation-detail'),
    url(r'^users/(?P<user_id>[0-9]+)/relations/incomings/$',
        incoming_care_relations_list, name='incoming-care-relations-list'),
    url(r'^users/(?P<user_id>[0-9]+)/relations/incomings/(?P<pk>[0-9]+)/$',
        incoming_care_relation_detail, name='incoming-care-relation-detail'),
    url(r'^users/(?P<user_id>[0-9]+)/vitals/$',
        user_vitals_list, name='user-vitals-list'),
    url(r'^users/(?P<user_id>[0-9]+)/vitals/(?P<pk>[0-9]+)/$',
        user_vital_detail, name='user-vital-detail'),
    url(r'^users/(?P<user_id>[0-9]+)/settings/$',
        user_settings, name='user-settings')
)
