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



class OperateVolume(baseclient):

    def get_vim_volumes(self, data, project_id):
        param = {
            'username' : data['username'],
            'user_domain_name' : 'default',
            'project_domain_name' : 'default',
            'password' : data['password'],
            'auth_url' : data['url'],
            'project_id' : project_id
        }

        volumes = self.cinder(param).list_volumes()
        return volumes


    def create_vim_volume(self, data, project_id, body):
        param = {
            'username' : data['username'],
            'user_domain_name' : 'default',
            'project_domain_name' : 'default',
            'password' : data['password'],
            'auth_url' : data['url'],
            'project_id' : project_id
        }
        logger.debug(body)
        volume = self.cinder(param).create_volume(**body)
        return volume

    def get_vim_volume(self, data, project_id, volume_id):
        param = {
            'username' : data['username'],
            'user_domain_name' : 'default',
            'project_domain_name' : 'default',
            'password' : data['password'],
            'auth_url' : data['url'],
            'project_id' : project_id
        }
        volume = self.cinder(param).get_volume(volume_id)
        return volume

    def delete_vim_volume(self, data, project_id, volume_id):
        param = {
            'username' : data['username'],
            'user_domain_name' : 'default',
            'project_domain_name' : 'default',
            'password' : data['password'],
            'auth_url' : data['url'],
            'project_id' : project_id
        }
        volume = self.cinder(param).delete_volume(volume_id)
        return volume
