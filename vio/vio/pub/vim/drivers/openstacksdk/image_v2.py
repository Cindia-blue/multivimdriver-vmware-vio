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

    def __init__(self, params):
        super(GlanceClient, self).__init__(params)
        LOG.info("%s", str(params))
        self.conn = sdk.create_connection(params)
        self.session = self.conn.session
        self._proxy = self.conn.image

    @sdk.translate_exception
    def list_images(self, **query):
        images = self._proxy.images(**query)
        return images

    @sdk.translate_exception
    def get_image(self, imageid):
        image = self._proxy.get_image(imageid)
        return image

    @sdk.translate_exception
    def delete_image(self, imageid):
        self._proxy.delete_image(imageid)

    @sdk.translate_exception
    def create_image(self,  **data):

        disk_format = data.get('imageType')
        container_format = data.get('containerFormat')

        if not all([container_format, disk_format]):
            LOG.error( "Both container_format and disk_format are required")

        param = {}
        param['name'] = data.get('name')
        param['visibility'] = data.get('visibility')
        #param['properties'] = data.get('properties')
        try:
            img = self._proxy._create(_image.Image, disk_format=disk_format,
                                      container_format=container_format, **param)
        except Exception as ex:
            pass
        return img

    @sdk.translate_exception
    def upload_image(self, data, image):
        image.data = data
        image.upload(self.session)