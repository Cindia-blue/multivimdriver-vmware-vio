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

    def create_server(self, data, project_id, create_req):
        import pdb;pdb.set_trace()
        req = {
            "name": create_req.get('name'),
            "networks": [
                {'id': nic['portName']} for nic in create_req.get('nicArray')
            ],
            "attached_volumes": [v['volumeName']
                                 for v in create_req.get('volumeArray')],
            "flavor_id": create_req.get('flavorId'),
            "availability_zone": create_req.get('availabilityZone'),
            "metadata": {md['keyName']: md['value']
                         for md in create_req.get('metadata')},
            "user_data": create_req.get('userdata'),
        }
        boot = create_req.get('boot')
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
