# Copyright (c) 2017 VMware, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import logging

from openstack import exceptions

from vio.pub.vim.vimapi.baseclient import baseclient
from vio.pub.vim.vimapi.nova.OperateNova import OperateNova

logger = logging.getLogger(__name__)


class OperateServers(OperateNova):

    def create_server(self, data, project_id, **kwargs):
        import pdb;pdb.set_trace()
        req = {
            "name": kwargs.get('name'),
            "networks": [
                {'id': nic['portName']} for nic in kwargs.get('nicArray')
            ],
            "attached_volumes": [v['volumeName']
                                 for v in kwargs.get('volumeArray')],
            "flavor_id": kwargs.get('flavorId'),
            "availability_zone": kwargs.get('availabilityZone'),
            "metadata": {md['keyName']: md['value']
                         for md in kwargs.get('metadata')},
            "user_data": kwargs.get('userdata'),
        }
        boot = kwargs.get('boot')
        boot_type = boot.get('type')
        if boot_type == 1:
            # boot from vol
            boot.get('volumeId')
            pass
        elif boot_type == 2:
            req['image_id'] = boot.get('imageId')
        return self.request('create_server', data,
                            project_id=project_id, **req)

    def list_servers(self, data, project_id):
        param = {'username': data['username'],
                 'user_domain_name': 'default',
                 'project_domain_name': 'default',
                 'password': data['password'],
                 'auth_url': data['url'],
                 'project_id': project_id}
        projects = self.compute(param).list_servers()
        return projects

    def get_server(self, data, project_id, server_id):
        param = {'username': data['username'],
                 'user_domain_name': 'default',
                 'project_domain_name': 'default',
                 'password': data['password'],
                 'auth_url': data['url'],
                 'project_id': project_id}
        try:
            project = self.compute(param).get_server(server_id=server_id)
            return project
        except exceptions.ResourceNotFound:
            return None

    def delete_server(self, data, project_id, server_id):
        param = {'username': data['username'],
                 'user_domain_name': 'default',
                 'project_domain_name': 'default',
                 'password': data['password'],
                 'auth_url': data['url'],
                 'project_id': project_id}
        project = self.compute(param).delete_server(server_id)
        return project
