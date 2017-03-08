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


def image_formatter(image):

    return {
        'id' : image.id,
        'name' : image.name,
        'imageType' : image.disk_format,
        'status' : image.status,
        'size' : image.size,
        'containerFormat' : image.container_format,
        'visibility' : image.visibility
    }


def vim_formatter(vim_info, tenantid):
    rsp = {}
    rsp['vimid'] = vim_info.get('vimId')
    rsp['vimName'] = vim_info.get('name')
    rsp['tenantid'] = tenantid
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