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


def volume_formatter(volume):

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


def vim_formatter(vim_info, tenantid):

    rsp = {}
    rsp['vimId'] = vim_info.get('vimId')
    rsp['vimName'] = vim_info.get('name')
    rsp['tenantId'] = tenantid
    return rsp


def sdk_param_formatter(data):

    param = {}
    param['username'] = data.get('userName')
    param['password'] = data.get('password')
    param['auth_url'] = data.get('url')
    param['project_name'] = data.get('tenant')
    param['user_domain_name'] = 'default'
    param['project_domain_name'] = 'default'
    return param


def req_body_formatter(body):

    param = {}
    param['name'] = body.get('name')
    param['size'] = body.get('volumeSize')

    if body.get('volumeType'):
        param['volume_type'] = body.get('volumeType')
    if body.get('availabilityZone'):
        param['availability_zone'] = body.get('availabilityZone')
    if body.get('imageId'):
        param['image_id'] = body.get('imageId')
    return param
