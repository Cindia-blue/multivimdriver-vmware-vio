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


def server_formatter(server):
    # TODO: finish all attributes
    return {
        "id": server.id,
        "name": server.name
    }


def flavor_formatter(flavor, extra_specs):
    # TODO: finish all attributes
    return {
        "id": flavor.id,
        "name": flavor.name,
        "vcpu": flavor.vcpus,
        "memory": flavor.ram,
        "disk": flavor.disk,
        "ephemeral": flavor['OS-FLV-EXT-DATA:ephemeral'],
        "swap": flavor.swap,
        "isPublic": flavor['os-flavor-access:is_public'],
        "extraSpecs": extra_specs_formatter(extra_specs)
    }


def extra_specs_formatter(extra_specs):
    return {

    }