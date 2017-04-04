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

from vio.pub.vim.vimapi.nova.OperateNova import OperateNova

logger = logging.getLogger(__name__)


class OperateHypervisor(OperateNova):

    def get_hypervisor(self, data, hypervisor, **kwargs):
        try:
            return self.request('get_hypervisor', data,
                                project_id=data['project_id'],
                                hypervisor=hypervisor,
                                **kwargs)
        except exceptions.ResourceNotFound:
            return None
