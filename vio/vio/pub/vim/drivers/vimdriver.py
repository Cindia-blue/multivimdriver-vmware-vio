# Copyright (c) 2017 VMware, Inc.
#
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


from vio.pub.vim.drivers.openstacksdk import image_v2
from vio.pub.vim.drivers.openstacksdk import keystone_v3
from vio.pub.vim.drivers.openstacksdk import cinder_v2
from vio.pub.vim.drivers.openstacksdk import compute


class VimDriver(object):
    '''Generic driver class'''

    def __init__(self):
        self.identity = keystone_v3.KeystoneClient
        self.glance = image_v2.GlanceClient
        self.cinder = cinder_v2.CinderClient
        self.compute = compute.ComputeClient
