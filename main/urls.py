'''
Created on Oct 11, 2014

@author: nanaya
'''
from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter

import views


router = DefaultRouter()
router.register(r'users', views.UserViewSet)
auth = views.GetAuthTokenAndUserInformation.as_view()


urlpatterns = patterns(
    '',
    url(r'^token/$', auth, name='signin'),
    url(r'^', include(router.urls)),
)
