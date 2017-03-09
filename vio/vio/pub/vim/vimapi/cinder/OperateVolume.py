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


from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.baseclient import baseclient
from vio.swagger import volume_utils

logger = logging.getLogger(__name__)


class OperateVolume(baseclient):

    def __init__(self, params):
        super(OperateVolume, self).__init__()
        self.param = volume_utils.sdk_param_formatter(params)

    def get_vim_volumes(self, **query):

        volumes = self.cinder(self.param).list_volumes(**query)
        return volumes

    def create_vim_volume(self, **body):

        volume = self.cinder(self.param).create_volume(**body)
        return volume

    def get_vim_volume(self, volume_id):

        volume = self.cinder(self.param).get_volume(volume_id)
        return volume

    def delete_vim_volume(self, volume_id):

        volume = self.cinder(self.param).delete_volume(volume_id)
        return volume