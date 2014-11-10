'''
Created on Nov 9, 2014

@author: nanaya
'''
from django.conf.urls import patterns, url

from .views import InboxViewSet


inbox_list = InboxViewSet.as_view({
    'get': 'list',
})
inbox_detail = InboxViewSet.as_view({
    'get': 'read',
})


urlpatterns = patterns(
    '',
    url(r'^inbox/$', inbox_list, name='inbox-list'),
    url(r'^inbox/(?P<pk>[0-9]+)/$', inbox_detail, name='inbox-detail'),
)

