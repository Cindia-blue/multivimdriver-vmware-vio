# Copyright (c) 2017 VMware, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from vio.swagger.views.hypervisor.views import HostView
from vio.swagger.views.limits.views import LimitsView
from vio.swagger.views.service.views import HostsView
from vio.swagger.views.swagger_json import SwaggerJsonView
from vio.swagger.views.tenant.views import ListTenantsView
from vio.swagger.views.image.views import CreateListImagesView
from vio.swagger.views.image.views import GetDeleteImageView
from vio.swagger.views.volume.views import CreateListVolumeView
from vio.swagger.views.volume.views import GetDeleteVolumeView
from vio.swagger.views.server.views import ListServersView, GetServerView
from vio.swagger.views.flavor.views import FlavorsView, FlavorView
from vio.swagger.views.network.views import CreateNetworkView, DeleteNetworkView

urlpatterns = [
    url(r'^openoapi/multivim-vio/v1/swagger.json$', SwaggerJsonView.as_view()),
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'tenants$', ListTenantsView.as_view()),
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z_-]+)/images$',
         CreateListImagesView.as_view()),
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z_-]+)/images/(?P<imageid>[0-9a-zA-Z_-]+)$',
        GetDeleteImageView.as_view()),
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z_-]+)/volumes$',
        CreateListVolumeView.as_view()),
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z_-]+)/volumes/(?P<volumeid>[0-9a-zA-Z_-]+)$',
        GetDeleteVolumeView.as_view()),
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z]+)/servers$', ListServersView.as_view()),
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z]+)/servers/(?P<serverid>[0-9a-zA-Z_-]+)$',
        GetServerView.as_view()),
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z]+)/flavors$',
        FlavorsView.as_view()),
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z]+)/flavors/(?P<flavorid>[0-9a-zA-Z_-]+)$',
        FlavorView.as_view()),
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z]+)/limits$',
        LimitsView.as_view()),
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z]+)/hosts$',
        HostsView.as_view()),
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z]+)/hosts/(?P<hostname>[0-9a-zA-Z_-]+)$',
        HostView.as_view()),
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z\-\_]+)/'
        r'(?P<tenantid>[0-9a-zA-Z\-\_]+)/networks$',
        CreateNetworkView.as_view()),
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z\-\_]+)/'
        r'(?P<tenantid>[0-9a-zA-Z\-\_]+)/networks/'
        r'(?P<networkid>[0-9a-zA-Z\-\_]+)$',
        DeleteNetworkView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
