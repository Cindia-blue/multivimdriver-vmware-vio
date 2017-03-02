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

import copy

import logging

from vio.pub.vim.drivers import vimdriver as driver_base

LOG = logging.getLogger(__name__)


class baseclient(object):


    def __init__(self,  **kwargs):

        # initialize clients
        self._identityclient = None
        self._glanceclient = None


    def identity(self, data):
        '''Construct compute client based on object.

        :param obj: Object for which the client is created. It is expected to
                    be None when retrieving an existing client. When creating
                    a client, it contains the user and project to be used.
        '''

        if self._identityclient is not None:
            return self._identityclient
        self._identityclient = driver_base.VimDriver().identity(data)
        return self._identityclient


    def glance(self, data):
        if self._glanceclient is not None:
            return self._glanceclient
        self._glanceclient = driver_base.VimDriver().glance(data)
        return self._glanceclient


