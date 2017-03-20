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

from rest_framework import status

from vio.pub.msapi.extsys import get_vim_by_id
from vio.pub.vim.drivers.vimsdk import neutron_v2_0
from vio.pub.exceptions import VimDriverVioException

logger = logging.getLogger(__name__)


def translate(mapping, data, revert=True):
    if revert:
        for key in mapping:
            if key in data:
                data[mapping[key]] = data.pop(key)
    else:
        for key in mapping:
            if mapping[key] in data:
                data[key] = data.pop(mapping[key])
    return data


class BaseNet(object):
    def get_vim_info(self, vimid):
        try:
            vim_info = get_vim_by_id(vimid)
        except VimDriverVioException as e:
            raise VimDriverVioException("Failed to query VIM with id (%s) from extsys." % vimid,
                                        status.HTTP_404_NOT_FOUND)
        return vim_info

    def auth(self, vim_info, tenant_id):
        param = {}
        param['username'] = vim_info['userName']
        param['user_domain_name'] = 'default'
        param['project_domain_name'] = 'default'
        param['password'] = vim_info['password']
        param['auth_url'] = vim_info['url']
        param['project_id'] = tenant_id
        return neutron_v2_0.NeutronClient(param)


class OperateNetwork(BaseNet):
    service = {'service_type': 'network',
               'interface': 'public',
               'region_name': 'RegionOne'}
    keys_mapping = {"segmentationId": "provider:segmentation_id",
                    "physicalNetwork": "provider:physical_network",
                    "routerExternal": "router:external",
                    "networkType": "provider:network_type",
                    "vlanTransparent": "vlan_transparent",
                    "tenantId": "project_id"
                    }

    def ___init__(self, params):
        super(OperateNetwork, self).__init__(params)

    def _convert(self, network):
        result = {}
        result['status'] = network.status
        result['id'] = network.id
        result['name'] = network.name
        result['tenantId'] = network.project_id
        result['segmentationId'] = network.provider_segmentation_id
        result['networkType'] = network.provider_network_type
        result['physicalNetwork'] = network.provider_physical_network
        result['vlanTransparent'] = True
        result['shared'] = network.is_shared
        result['routerExternal'] = network.is_router_external
        return result

    def create_network(self, vimid, tenantid, body):
        vim_info = self.get_vim_info(vimid)
        network = self.auth(vim_info, tenantid)
        body = translate(self.keys_mapping, body)
        net = network.network_create(**body)
        vim_dict = {"vimName": vim_info['name'], "vimId": vim_info['vimId']}
        resp = self._convert(net)
        resp.update(vim_dict)
        return resp

    def list_network(self, vimid, tenantid, networkid):
        vim_info = self.get_vim_info(vimid)
        network = self.auth(vim_info, tenantid)
        net = network.network_get(networkid)
        if net is None:
            return net
        vim_dict = {"vimName": vim_info['name'], "vimId": vim_info['vimId']}
        resp = self._convert(net)
        resp.update(vim_dict)
        return resp

    def delete_network(self, vimid, tenantid, networkid):
        vim_info = self.get_vim_info(vimid)
        network = self.auth(vim_info, tenantid)
        return network.network_delete(networkid)

    def list_networks(self, vimid, tenantid, **query):
        vim_info = self.get_vim_info(vimid)
        network = self.auth(vim_info, tenantid)
        resp = network.networks_get(**query)
        vim_dict = {"vimName": vim_info['name'], "vimId": vim_info['vimId']}
        networks = {'networks': []}
        if resp:
            for net in resp:
                networks['networks'].append(self._convert(net))
        networks.update(vim_dict)
        return networks
