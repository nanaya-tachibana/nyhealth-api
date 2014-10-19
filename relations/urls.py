'''
Created on Oct 11, 2014

@author: nanaya
'''
from django.conf.urls import patterns, url

import views


relation_list = views.UserRelationViewSet.as_view({
    'get': 'list',
})
relation_detail = views.UserRelationViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update'
})
outgoing_relation_list = views.UserOutgoingRelationViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
outgoing_relation_detail = views.UserOutgoingRelationViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
})
incoming_relation_list = views.UserIncomingRelationViewSet.as_view({
    'get': 'list',
})
incoming_relation_detail = views.UserIncomingRelationViewSet.as_view({
    'get': 'retrieve',
    'patch': 'allow',
    'delete': 'deny',
})

urlpatterns = patterns(
    '',
    url(r'^relations/$', relation_list, name='relation-list'),
    url(r'^relations/(?P<pk>[0-9]+)/$',
        relation_detail, name='relation-detail'),
    url(r'^relations/outgoings/$',
        outgoing_relation_list, name='outgoing-relation-list'),
    url(r'^relations/outgoings/(?P<pk>[0-9]+)/$',
        outgoing_relation_detail, name='outgoing-relation-detail'),
    url(r'^relations/incomings/$',
        incoming_relation_list, name='incoming-relation-list'),
    url(r'^relations/incomings/(?P<pk>[0-9]+)/$',
        incoming_relation_detail, name='incoming-relation-detail'),
)
