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



class OperateImage(baseclient):

    def get_vim_images(self, data):
        param = {}
        param['username'] = data['username']
        param['user_domain_name'] = 'default'
        param['project_domain_name'] = 'default'
        param['password'] = data['password']
        param['auth_url'] = data['url']
        param['project_name'] = data['project_name']
        images = self.glance(param).list_images()
        return images

    def create_vim_image(self, data):
        param = {}
        param['username'] = data['username']
        param['user_domain_name'] = 'default'
        param['project_domain_name'] = 'default'
        param['password'] = data['password']
        param['auth_url'] = data['url']
        param['project_name'] = data['project_name']
        image = self.glance(param).create_image()
        return image
       
