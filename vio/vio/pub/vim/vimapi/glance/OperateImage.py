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
from vio.swagger import image_utils

logger = logging.getLogger(__name__)



class OperateImage(baseclient):

    def get_vim_images(self, data):

        param = image_utils.sdk_param_formatter(data)
        images = self.glance(param).list_images()
        return images

    def get_vim_image(self, data, imageid):

        param = image_utils.sdk_param_formatter(data)
        image = self.glance(param).get_image(imageid)
        return image

    def delete_vim_image(self, data, imageid):

        param = image_utils.sdk_param_formatter(data)
        image = self.glance(param).delete_image(imageid)
        return image
