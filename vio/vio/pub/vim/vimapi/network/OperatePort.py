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

from vio.pub.msapi.extsys import get_vim_by_id
from vio.pub.vim.drivers.vimsdk import neutron_v2_0
from vio.pub.vim.vimapi.network.OperateNetwork import BaseNet, translate


logger = logging.getLogger(__name__)


class OperatePort(BaseNet):
    keys_mapping = {"tenantId": "project_id",
                    "networkId": "network_id",
                    "vnicType": "binding:vnic_type",
                    "securityGroups": "security_groups",
                    "macAddress": "mac_address",
                    # "subnetId": "subnet_id",
                    "ip": "ip_address"
                    }

    def ___init__(self, params):
        super(OperatePort, self).__init__(params)

    def _convert(self, port):
        result = {}
        result['status'] = 'ok'
        result['id'] = port.id
        result['networkId'] = port.network_id
        result['name'] = port.name
        result['vnicType'] = port.binding_vnic_type
        result['macAddress'] = port.mac_address
        if port.fixed_ips:
            subnet_id = port.fixed_ips[0]['subnet_id']
        else:
            subnet_id = port.subnet_id
        result['subnetId'] = subnet_id
        result['securityGroups'] = port.security_group_ids
        return result

    def create_port(self, vimid, tenantid, body):
        vim_info = self.get_vim_info(vimid)
        network = self.auth(vim_info)
        body = translate(self.keys_mapping, body)
        if body.get('subnetId'):
            body['fixed_ips'] = [{'subnet_id': body.pop('subnetId')}]
        port = network.port_create(**body)
        vim_dict = {"vimName": vim_info['name'], "vimId": vim_info['vimId']}
        resp = self._convert(port)
        resp.update(vim_dict)
        return resp

    def list_port(self, vimid, tenantid, portid, ignore_missing=False):
        vim_info = self.get_vim_info(vimid)
        network = self.auth(vim_info)
        port = network.port_find(portid, ignore_missing=ignore_missing)
        if port is None:
            return port
        vim_dict = {"vimName": vim_info['name'], "vimId": vim_info['vimId']}
        resp = self._convert(port)
        resp.update(vim_dict)
        return resp

    def delete_port(self, vimid, tenantid, portid):
        vim_info = self.get_vim_info(vimid)
        network = self.auth(vim_info)
        return network.port_delete(portid)

    def list_ports(self, vimid, tenantid, **query):
        vim_info = self.get_vim_info(vimid)
        network = self.auth(vim_info)
        query.update({"project_id": tenantid})
        resp = network.ports_get(**query)
        vim_dict = {"vimName": vim_info['name'], "vimId": vim_info['vimId']}
        ports = {'ports': []}
        if resp:
            for port in resp:
                ports['ports'].append(self._convert(port))
        ports.update(vim_dict)
        return ports
