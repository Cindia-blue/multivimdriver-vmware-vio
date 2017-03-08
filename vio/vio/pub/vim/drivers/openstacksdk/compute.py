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
import base64
import logging

from vio.pub.vim.drivers import base
from vio.pub.vim.drivers.openstacksdk import sdk

LOG = logging.getLogger(__name__)


class ComputeClient(base.DriverBase):
    """Compute driver."""

    def __init__(self, params):
        super(ComputeClient, self).__init__(params)
        self.conn = sdk.create_connection(params)
        self.session = self.conn.session

    @sdk.translate_exception
    def create_server(self, **kwargs):
        flavor_name = kwargs.pop('flavor_name', None)
        if flavor_name:
            kwargs['flavor_id'] = self.conn.compute.find_flavor(flavor_name)

        if kwargs.get('volume_id') or kwargs.get('volume_name'):
            pass
        else:
            image_name = kwargs.pop('image_name', None)
            if image_name:
                kwargs['image_id'] = self.conn.compute.find_image(image_name)

        networks = kwargs.get('networks')
        network_ids = []
        for network in networks:
            net_name = network.get('name')
            net_id = network.get('id')
            if net_name:
                net_id = self.conn.network.find_network(net_name).id
            network_ids.append({"uuid": net_id})
        kwargs['networks'] = network_ids
        kwargs.pop('project_id', None)

        userdata = kwargs.get('user_data')
        if userdata:
            kwargs['user_data'] = base64.encodestring(userdata)

        import pdb;pdb.set_trace()
        server = self.conn.compute.create_server(**kwargs)
        return server

    @sdk.translate_exception
    def list_servers(self):
        servers = self.conn.compute.servers()
        return servers

    @sdk.translate_exception
    def get_server(self, server_id, **query):
        server = self.conn.compute.get_server(server=server_id)
        return server

    @sdk.translate_exception
    def delete_server(self, server_id, **query):
        self.conn.compute.delete_server(server=server_id)

    @sdk.translate_exception
    def list_flavors(self, **query):
        flavors = self.conn.compute.flavors()
        return flavors

    @sdk.translate_exception
    def create_flavor(self, **kwargs):
        return self.conn.compute.create_flavor(**kwargs)

    @sdk.translate_exception
    def get_flavor(self, flavor_id, **query):
        return self.conn.compute.get_flavor(flavor=flavor_id)

    @sdk.translate_exception
    def delete_flavor(self, flavor_id, **query):
        self.conn.compute.delete_flavor(flavor=flavor_id)

    @sdk.translate_exception
    def get_flavor_extra_specs(self, flavor_id, **query):
        return None

    @sdk.translate_exception
    def get_limits(self, **kwargs):
        return self.conn.compute.get_limits()

    @sdk.translate_exception
    def list_services(self, **kwargs):
        return self.conn.compute.services()

    @sdk.translate_exception
    def get_hypervisor(self, hypervisor, **kwargs):
        return self.conn.compute.get_hypervisor(hypervisor=hypervisor)
