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

import logging

from vio.pub.vim.drivers import base
from vio.pub.vim.drivers.openstacksdk import sdk

LOG = logging.getLogger(__name__)


class GlanceClient(base.DriverBase):
    '''Image V1 driver.'''

    def __init__(self, params):
        super(GlanceClient, self).__init__(params)
        LOG.info("%s", str(params))
        self.conn = sdk.create_connection(params)
        self.session = self.conn.session

    @sdk.translate_exception
    def list_images(self):
        images = self.conn.image.images()
        return images

    @sdk.translate_exception
    def create_image(self):
        image = self.conn.image.upload_image()
        return image
