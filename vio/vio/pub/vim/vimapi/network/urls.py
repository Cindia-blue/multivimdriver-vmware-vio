# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from vio.pub.vim.vimapi.network import views

urlpatterns = [
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z\-\_]+)/(?P<tenantid>[0-9a-zA-Z\-\_]+)/networks$',
        views.create_list_network, name='create_list_network'),
    url(r'^openoapi/multivim-vio/v1/(?P<vimid>[0-9a-zA-Z\-\_]+)/(?P<tenantid>[0-9a-zA-Z\-\_]+)/networks/(?P<networkid>[0-9a-zA-Z\-\_]+)$',
        views.delete_list_network, name='delete_list_network'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
