from django.conf.urls import patterns, include, url

from django.contrib import admin
from argparse import Namespace
admin.autodiscover()

from api import urls as api_urls

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'nyhealth.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls'))
)
