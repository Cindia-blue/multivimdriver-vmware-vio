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

from openstack import resource2 as resource
from openstack.compute import compute_service

from vio.pub.vim.drivers import base
from vio.pub.vim.drivers.vimsdk import sdk

LOG = logging.getLogger(__name__)


class FlavorExtraSpecs(resource.Resource):
    resources_key = 'os-extra_specs'
    base_path = '/flavors/%(flavor_id)s/os-extra_specs'
    service = compute_service.ComputeService()

    #: The ID for the flavor.
    flavor_id = resource.URI('flavor_id')

    # capabilities
    allow_create = True
    allow_get = True
    allow_delete = True
    allow_list = True

    extra_specs = resource.Body('extra_specs')


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
    def find_server(self, server_id, ignore_missing=False):
        server = self.conn.compute.find_server(
            server_id, ignore_missing=ignore_missing)
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
    def find_flavor(self, flavor_id, ignore_missing=False):
        return self.conn.compute.find_flavor(
            flavor_id, ignore_missing=ignore_missing)

    @sdk.translate_exception
    def delete_flavor(self, flavor_id, **query):
        self.conn.compute.delete_flavor(flavor=flavor_id)

    @sdk.translate_exception
    def get_flavor_extra_specs(self, flavor_id, **query):
        return self.conn.compute._get(FlavorExtraSpecs, flavor_id=flavor_id,
                                      requires_id=False)

    @sdk.translate_exception
    def create_flavor_extra_specs(self, flavor_id, extra_specs, **query):
        return self.conn.compute._create(FlavorExtraSpecs,
                                         flavor_id=flavor_id,
                                         extra_specs=extra_specs)

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
