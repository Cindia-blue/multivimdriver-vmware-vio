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
            "name": create_req.get('name'),
            "flavorRef": cc.find_flavor(create_req.get('flavorId')).id
        }
        boot = create_req.get('boot')
        boot_type = boot.get('type')
        if boot_type == 1:
            # boot from vol
            req['block_device_mapping_v2'] = {
                'uuid': boot["volumeId"],
                'source_type': 'volume',
                'destination_type': 'volume',
                'delete_on_termination': False
            }
        elif boot_type == 2:
            req['imageRef'] = cc.find_image(boot.get('imageId')).id
        networks = create_req.get('nicArray', [])
        if networks:
            req['networks'] = [{'port': n['portId']} for n in networks]
        az = create_req.get('availabilityZone', None)
        if az:
            req['availability_zone'] = az
        md = create_req.get('metadata', [])
        if md:
            req['metadata'] = [{n['keyName']: n['Value']} for n in md]
        userdata = create_req.get('userdata', None)
        if userdata:
            req['user_data'] = base64.encodestring(userdata)
        sg = create_req.get('securityGroups', [])
        if sg:
            req['security_groups'] = sg
        # todo attach volumes after server created
        volumes = create_req.get('volumeArray', [])
        return cc.create_server(**req)

    def list_servers(self, data, project_id):
        param = {'username': data['username'],
                 'user_domain_name': 'default',
                 'project_domain_name': 'default',
                 'password': data['password'],
                 'auth_url': data['url'],
                 'project_id': project_id}
        projects = self.compute(param).list_servers()
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
