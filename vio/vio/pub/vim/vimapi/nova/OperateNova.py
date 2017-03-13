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

from vio.pub.vim.vimapi.baseclient import baseclient


logger = logging.getLogger(__name__)


class OperateNova(baseclient):

    def __init__(self, **kwargs):
        super(OperateNova, self).__init__(**kwargs)

    def request(self, op, data, **kwargs):
        param = {'username': data['username'],
                 'user_domain_name': 'default',
                 'project_domain_name': 'default',
                 'password': data['password'],
                 'auth_url': data['url']}
        project_id = kwargs.pop('project_id', None)
        if project_id:
            param['project_id'] = project_id
        else:
            param['project_name'] = kwargs.get('project_name')
        compute = self.compute(param)
        func = getattr(compute, op)
        return func(**kwargs)
