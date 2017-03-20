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

import base64
import logging

from openstack import exceptions
from rest_framework import status

from vio.pub.exceptions import VimDriverVioException
from vio.pub.vim.vimapi.nova.OperateNova import OperateNova

logger = logging.getLogger(__name__)


class OperateServers(OperateNova):

    def create_server(self, data, project_id, create_req):
        param = {'username': data['username'],
                 'user_domain_name': 'default',
                 'project_domain_name': 'default',
                 'password': data['password'],
                 'auth_url': data['url'],
                 'project_id': project_id}
        cc = self.compute(param)
        req = {
            "name": create_req['name'],
            "flavorRef": cc.find_flavor(create_req['flavorId']).id
        }
        boot = create_req['boot']
        boot_type = boot['type']
        if int(boot_type) == 1:
            # boot from vol
            req['block_device_mapping_v2'] = [{
                'boot_index': "0",
                'uuid': boot["volumeId"],
                'source_type': 'volume',
                'destination_type': 'volume',
                'delete_on_termination': False
            }]
        elif int(boot_type) == 2:
            req['imageRef'] = cc.find_image(boot['imageId']).id
        else:
            raise VimDriverVioException(
                'Boot type should be 1 or 2.',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        networks = create_req.get('nicArray', [])
        if networks:
            req['networks'] = [{'port': n['portId']} for n in networks]
        az = create_req.get('availabilityZone', None)
        if az:
            req['availability_zone'] = az
        md = create_req.get('metadata', [])
        if md:
            req['metadata'] = {n['keyName']: n['value'] for n in md}
        userdata = create_req.get('userdata', None)
        if userdata:
            req['user_data'] = base64.encodestring(userdata)
        sg = create_req.get('securityGroups', [])
        if sg:
            req['security_groups'] = []
            for v in sg:
                req['security_groups'].append({'name':v})
        # todo attach volumes after server created
        volumes = create_req.get('volumeArray', [])
        if volumes:
            if not req.get('block_device_mapping_v2'):
                req['block_device_mapping_v2'] = []
            for vol in volumes:
                req['block_device_mapping_v2'].append(
                    {
                        'uuid': vol["volumeId"],
                        'source_type': 'volume',
                        'destination_type': 'volume',
                        'delete_on_termination': False
                    }
                )
        inject_files = create_req.get('contextArray', [])
        if inject_files:
            req['personality'] = []
            for i in inject_files:
                req['personality'].append(
                    {"path": i["fileName"], "contents": i["fileData"]})

        return cc.create_server(**req)

    def list_servers(self, data, project_id, **query):
        param = {'username': data['username'],
                 'user_domain_name': 'default',
                 'project_domain_name': 'default',
                 'password': data['password'],
                 'auth_url': data['url'],
                 'project_id': project_id}
        projects = self.compute(param).list_servers(**query)
        return projects

    def list_server_interfaces(self, data, project_id, server):
        param = {'username': data['username'],
                 'user_domain_name': 'default',
                 'project_domain_name': 'default',
                 'password': data['password'],
                 'auth_url': data['url'],
                 'project_id': project_id}
        interfaces = self.compute(param).list_server_interfaces(server)
        return list(interfaces)

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

    def find_server(self, data, project_id, server_id):
        param = {'username': data['username'],
                 'user_domain_name': 'default',
                 'project_domain_name': 'default',
                 'password': data['password'],
                 'auth_url': data['url'],
                 'project_id': project_id}
        server = self.compute(param).find_server(
            server_id, ignore_missing=True)
        return server

    def delete_server(self, data, project_id, server_id):
        param = {'username': data['username'],
                 'user_domain_name': 'default',
                 'project_domain_name': 'default',
                 'password': data['password'],
                 'auth_url': data['url'],
                 'project_id': project_id}
        project = self.compute(param).delete_server(server_id)
        return project
