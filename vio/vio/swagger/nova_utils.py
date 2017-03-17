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

import six


def server_formatter(server, interfaces=[]):
    r = {
        "id": server.id,
        "name": server.name,
        "tenantId": server.project_id,
        "availabilityZone": server.availability_zone,
        "flavorId": server.flavor_id or server.flavor['id'],
        "volumeArray": [],
        "metadata": [],
        "securityGroups": [],
        # TODO finish following attributes
        "serverGroup": "",
        "contextArray": [],
        "userdata": server.user_data,
        "nicArray": [],
        "status": server.status
    }
    if interfaces:
        r['nicArray'] = [{'portId': i.port_id} for i in interfaces]
    elif server.networks:
        r['nicArray'] = [{'portId': n['port']} for n in server.networks]
    # TODO: wait sdk fix block_device_mapping
    try:
        if server.attached_volumes:
            r["volumeArray"] = [{'volumeId': v['id']} for v in server.attached_volumes]
        elif server.block_device_mapping:
            r["volumeArray"] = [{'volumeId': v['uuid']} for v in server.block_device_mapping]
    except ValueError as e:
        r['volumeArray'] = [{'volumeId':""}]
    if server.image_id or server.image:
        r['boot'] = {
            'type': 2,
            'imageId': server.image_id or server.image['id']
        }
    else:
        r['boot'] = {
            'type': 1,
            'volumeId': r['volumeArray'][0]['volumeId']
        }
    if server.metadata:
        r["metadata"] = [{'keyName': k, 'value': v}
                         for k, v in six.iteritems(server.metadata)]
    if server.security_groups:
        r["securityGroups"] = [i['name'] for i in server.security_groups]
    return r


def flavor_formatter(flavor, extra_specs):
    r = {
        "id": flavor.id,
        "name": flavor.name,
        "vcpu": flavor.vcpus,
        "memory": flavor.ram,
        "disk": flavor.disk,
        "ephemeral": flavor.ephemeral,
        "swap": flavor.swap,
        "isPublic": flavor.is_public}
    if extra_specs:
        r["extraSpecs"] = extra_specs_formatter(extra_specs)
    return r


def extra_specs_formatter(extra_specs):
    return [{"keyName": k, "value": v}
            for k, v in six.iteritems(extra_specs.extra_specs)]


def server_limits_formatter(limits):
    return {
        # nova
        'maxPersonality': limits.absolute.personality,
        'maxPersonalitySize': limits.absolute.personality_size,
        'maxServerGroupMembers': limits.absolute.server_group_members,
        'maxServerGroups': limits.absolute.server_groups,
        'maxImageMeta': limits.absolute.image_meta,
        'maxTotalCores': limits.absolute.total_cores,
        'maxTotalInstances': limits.absolute.instances,
        'maxTotalKeypairs': limits.absolute.keypairs,
        'maxTotalRAMSize': limits.absolute.total_ram,
        'security_group_rules': limits.absolute.security_group_rules,
        'security_group': limits.absolute.security_groups,

        # cinder
        # neutron
    }


def service_formatter(service):
    return {
        'service': service.binary,
        'name': service.host,
        'zone': service.zone,
    }


def hypervisor_formatter(hypervisor):
    return {
        'name': hypervisor.name,
        'cpu': hypervisor.vcpus,
        'disk_gb': hypervisor.local_disk_size,
        'memory_mb': hypervisor.memory_size,
    }
