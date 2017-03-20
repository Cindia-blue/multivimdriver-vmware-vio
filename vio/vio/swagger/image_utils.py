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


def image_formatter(image):

    image = image.to_dict()
    properties = {}
    if image.get("vmware_adaptertype"):
        properties['vmware_adaptertype'] = image.get("vmware_adaptertype")
    if image.get("vmware_ostype"):
        properties['vmware_ostype'] = image.get("vmware_ostype")

    return {
        'id' : image.get("id"),
        'name' : image.get("name"),
        'imageType' : image.get("disk_format"),
        'status' : image.get("status"),
        'size' : image.get("size"),
        'containerFormat' : image.get("container_format"),
        'visibility' : image.get("visibility"),
        'properties' : properties
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
    param['project_id'] = data.get('tenant')
    param['user_domain_name'] = 'default'
    param['project_domain_name'] = 'default'
    return param

def req_body_formatter(body):

    param = {}
    param['name'] = body.get('name')
    param['disk_format'] = body.get('imageType')
    param['container_format'] = body.get('containerFormat')
    param['visibility'] = body.get('visibility')
    properties = body.get('properties', {})
    param.update(properties)
    return param
