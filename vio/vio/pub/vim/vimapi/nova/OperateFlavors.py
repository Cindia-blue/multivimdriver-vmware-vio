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

    def create_flavor(self, data, project_id, create_req):
        req = {
            "name": create_req.get('name'),
            "vcpus": create_req.get('vcpu'),
            "ram": create_req.get('memory'),
            "disk": create_req.get('disk'),
            "ephemeral": create_req.get('ephemeral', 0),
            "swap": create_req.get('swap', 0),
            "is_public": create_req.get('isPublic', True)
        }
        # TODO: support extraSpecs
        return self.request('create_flavor', data,
                            project_id=project_id, **req), None

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
        return self.request('delete_flavor', data, project_id=project_id,
                            flavor_id=flavor_id)
