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

logger = logging.getLogger(__name__)


class OperateServers(baseclient):

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
