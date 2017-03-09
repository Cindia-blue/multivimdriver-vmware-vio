# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from vio.pub.vim.drivers import base
from vio.pub.vim.drivers.openstacksdk import sdk


class NeutronClient(base.DriverBase):
    '''Neutron V2.0 driver.'''

    def __init__(self, params):
        super(NeutronClient, self).__init__(params)
        self.conn = sdk.create_connection(params)

    @sdk.translate_exception
    def subnet_create(self, **args):
        network = self.conn.network.create_subnet(**args)
        return network
    
    @sdk.translate_exception
    def network_create(self, **args):
        network = self.conn.network.create_network(**args)
        return network

    @sdk.translate_exception
    def network_get(self, name_or_id):
        network = self.conn.network.find_network(name_or_id)
        return network

    @sdk.translate_exception
    def network_delete(self, name_or_id):
        res = self.conn.network.delete_network(name_or_id)
        return res

    @sdk.translate_exception
    def networks_get(self, **kwargs):
        network = self.conn.network.networks(**kwargs)
        return network

    @sdk.translate_exception
    def subnets_get(self, **kwargs):
        subnets = self.conn.network.subnets(**kwargs)
        return subnets

    @sdk.translate_exception
    def subnet_delete(self, name_or_id):
        res = self.conn.network.delete_subnet(name_or_id)
        return res

    @sdk.translate_exception
    def port_find(self, name_or_id, ignore_missing=False):
        port = self.conn.network.find_port(name_or_id, ignore_missing)
        return port

    @sdk.translate_exception
    def subnet_get(self, name_or_id, ignore_missing=False):
        subnet = self.conn.network.find_subnet(name_or_id, ignore_missing)
        return subnet

    @sdk.translate_exception
    def port_create(self, **attr):
        res = self.conn.network.create_port(**attr)
        return res

    @sdk.translate_exception
    def port_delete(self, port, ignore_missing=True):
        res = self.conn.network.delete_port(
            port=port, ignore_missing=ignore_missing)
        return res

    @sdk.translate_exception
    def ports_get(self, **kwargs):
        ports = self.conn.network.ports(**kwargs)
        return ports

    