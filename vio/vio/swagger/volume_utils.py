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


def VolumeFormatter(volume):

    attachments = []
    for attach in volume.attachments:
        vim_attach = {
            'device' : attach['device'],
            'volumeId' : attach['volume_id'],
            'hostName' : attach['host_name'],
            'Id' : attach['attachment_id'],
            'serverId' : attach['server_id']
        }
        attachments.append(vim_attach)

    return {
        'id' : volume.id,
        'name' : volume.name,
        'createTime' : volume.created_at,
        'status' : volume.status,
        'type' : volume.volume_type,
        'size' : volume.size,
        'availabilityZone' : volume.availability_zone,
        'attachments' : attachments
    }
