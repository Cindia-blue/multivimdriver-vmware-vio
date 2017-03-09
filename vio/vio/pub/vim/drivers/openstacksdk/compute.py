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
    def list_server_interfaces(self, server_id):
        ifaces = self.conn.compute.server_interfaces(server_id)
        return list(ifaces)

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
    def find_flavor(self, flavor_id):
        return self.conn.compute.find_flavor(flavor_id, ignore_missing=False)

    @sdk.translate_exception
    def delete_flavor(self, flavor_id, **query):
        self.conn.compute.delete_flavor(flavor=flavor_id)

    @sdk.translate_exception
    def get_flavor_extra_specs(self, flavor_id, **query):
        return None

    @sdk.translate_exception
    def find_image(self, image_id, ignore_missing=False):
        return self.conn.compute.find_image(
            image_id, ignore_missing=ignore_missing)

    @sdk.translate_exception
    def get_limits(self, **kwargs):
        return self.conn.compute.get_limits()

    @sdk.translate_exception
    def list_services(self, **kwargs):
        return self.conn.compute.services()

    @sdk.translate_exception
    def get_hypervisor(self, hypervisor, **kwargs):
        return self.conn.compute.get_hypervisor(hypervisor=hypervisor)
