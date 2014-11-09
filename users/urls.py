'''
Created on Oct 11, 2014

@author: nanaya
'''
from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter

import views


urlpatterns = patterns(
    '',
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserView.as_view(),
        name='user-detail'),
    url(r'^users/search/$', views.SearchUser.as_view(), name='user-search'),
    url(r'^invite/$', views.InviteUser.as_view(), name='user-invite'),
)
