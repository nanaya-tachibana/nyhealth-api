'''
Created on Nov 8, 2014

@author: nanaya
'''
from django.conf.urls import patterns, url

from .views import (Login, Logout, Signup, PasswordChange,
                    PasswordReset, PasswordResetConfirm)

urlpatterns = patterns('',
    # URLs that do not require a session or valid token
    url(r'^password/reset/$', PasswordReset.as_view(),
        name='password_reset'),
    url(r'^password/reset/confirm/$', PasswordResetConfirm.as_view(),
        name='password_reset_confirm'),
    url(r'^signup/$', Signup.as_view(), name='signup'),
    url(r'^login/$', Login.as_view(), name='login'),
    # URLs that require a user to be logged in with a valid session / token.
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^password/change/$', PasswordChange.as_view(),
        name='password_change'),
)
