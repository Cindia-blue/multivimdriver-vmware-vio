# Copyright (c) 2017 VMware, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.


import logging


from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.baseclient import baseclient

logger = logging.getLogger(__name__)



class OperateTenant(baseclient):

    def get_projects(self, data, **query):
        param = {}
        param['username'] = data['username']
        param['user_domain_name'] = 'default'
        param['project_domain_name'] = 'default'
        param['password'] = data['password']
        param['auth_url'] = data['url']
        param['project_name'] = data['project_name']
        projects = self.identity(param).project_list(**query)
        projects = list(projects)
        # fix tenant filter
        # query['name'] is a list here.
        if query.get("name"):
            projs = []
            for p in projects:
                if p.name in query['name']:
                    projs.append(p)
            projects = projs
        return projects

