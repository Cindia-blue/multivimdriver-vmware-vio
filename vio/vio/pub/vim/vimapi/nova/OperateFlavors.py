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


class OperateFlavors(OperateNova):

    def __init__(self, **kwargs):
        super(OperateFlavors, self).__init__(**kwargs)

    def list_flavors(self, data, project_id):
        flavors = self.request('list_flavors', data, project_id=project_id)
        flavors = list(flavors)
        result = []
        for flavor in flavors:
            extra_specs = self.request('get_flavor_extra_specs', data,
                                       project_id=project_id, flavor_id=flavor.id)
            result.append((flavor, extra_specs))
        return result

    def get_flavor(self, data, project_id, flavor_id):
        try:
            flavor = self.request('get_flavor', data,
                                  project_id=project_id, flavor_id=flavor_id)
            extra_specs = self.request('get_flavor_extra_specs', data,
                                       project_id=project_id, flavor_id=flavor_id)
            return flavor, extra_specs

        except exceptions.ResourceNotFound:
            return None, None

    def delete_flavor(self, data, project_id, flavor_id):
        return self.request('delete_flavor', data, project_id=project_id)
