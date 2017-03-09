# Copyright 2017 VMware, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from vio.pub.vim.drivers import base
from vio.pub.vim.drivers.openstacksdk import sdk

LOG = logging.getLogger(__name__)

class CinderClient(base.DriverBase):
    '''Cinder V2 driver.'''

    def __init__(self, params):
        super(CinderClient, self).__init__(params)
        LOG.info("%s", str(params))
        self.conn = sdk.create_connection(params)
        self.session = self.conn.session

    @sdk.translate_exception
    def list_volumes(self, **query):
        volumes = self.conn.block_store.volumes(**query)
        return volumes


    @sdk.translate_exception
    def create_volume(self, **body):
        volume_info = self.conn.block_store.create_volume(**body)
        return volume_info


    @sdk.translate_exception
    def delete_volume(self, volumeid):
        self.conn.block_store.delete_volume(volumeid)


    @sdk.translate_exception
    def get_volume(self, volumeid):
        volume_info = self.conn.block_store.get_volume(volumeid)
        return volume_info
