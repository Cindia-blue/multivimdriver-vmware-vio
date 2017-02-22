# Copyright 2016 ZTE Corporation.
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


from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.baseclient import baseclient

logger = logging.getLogger(__name__)


class OperatorInstance(baseclient):
    def __init__(self, data):
        self._novaclient = None

    def create_image(self, data):
        pass

    def list_images(self, data):
        pass

    def delete_image(self, data):
        pass

    def get_image(self, data):
        kwargs = {}
        image = self.compute(obj).image_find(name_or_id)

        # wait for new version of openstacksdk to fix this
        kwargs.pop(self.IMAGE)
        kwargs['imageRef'] = image.id


