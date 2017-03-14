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
from vio.pub.vim.vimapi.network.OperateNetwork import BaseNet,translate


logger = logging.getLogger(__name__)


class OperateSubnet(BaseNet):
    keys_mapping = {"tenantId": "project_id",
                    "networkId": "network_id",
                    "ipVersion": "ip_version",
                    "gaetwayIp": "gateway_ip",
                    "dnsNameservers": "dns_nameservers",
                    "hostRoutes": "host_routes",
                    "allocationPools": "allocation_pools",
                    "enableDhcp": "is_dhcp_enabled"
                    }

    def ___init__(self, params):
        super(OperateSubnet, self).__init__(params)

    def _convert(self, subnet):
        result = {}
        result['status'] = 'ok'
        result['id'] = subnet.id
        result['networkId'] = subnet.network_id
        result['name'] = subnet.name
        result['allocationPools'] = subnet.allocation_pools
        result['gatewayIp'] = subnet.gateway_ip
        result['dnsNameServers'] = subnet.dns_nameservers
        result['ipVersion'] = subnet.ip_version
        result['enableDhcp'] = subnet.is_dhcp_enabled
        result['hostRoutes'] = subnet.host_routes
        result['cidr'] = subnet.cidr
        return result

    def create_subnet(self, vimid, tenantid, body):
        vim_info = self.get_vim_info(vimid)
        network = self.auth(vim_info)
        body = translate(self.keys_mapping, body)
        subnet = network.subnet_create(**body)
        vim_dict = {"vimName": vim_info['name'], "vimId": vim_info['vimId']}
        resp = self._convert(subnet)
        resp.update(vim_dict)
        return resp

    def list_subnet(self, vimid, tenantid, subnetid):
        vim_info = self.get_vim_info(vimid)
        network = self.auth(vim_info)
        subnet = network.subnet_get(subnetid)
        if subnet is None:
            return subnet
        vim_dict = {"vimName": vim_info['name'], "vimId": vim_info['vimId']}
        resp = self._convert(subnet)
        resp.update(vim_dict)
        return resp

    def delete_subnet(self, vimid, tenantid, subnetid):
        vim_info = self.get_vim_info(vimid)
        network = self.auth(vim_info)
        return network.subnet_delete(subnetid)

    def list_subnets(self, vimid, tenantid):
        vim_info = self.get_vim_info(vimid)
        network = self.auth(vim_info)
        tenant = {"project_id": tenantid}
        resp = network.subnets_get(**tenant)
        vim_dict = {"vimName": vim_info['name'], "vimId": vim_info['vimId']}
        subnets = {'subnets': []}
        if resp:
            for subnet in resp:
                subnets['subnets'].append(self._convert(subnet))
        subnets.update(vim_dict)
        return subnets
