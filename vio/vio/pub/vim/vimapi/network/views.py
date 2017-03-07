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

import logging
import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from vio.pub.utils import syscomm
from vio.pub.vim.vimapi.network import networking

logger = logging.getLogger(__name__)


@api_view(http_method_names=['POST','GET'])
def create_list_network(request, vimid, tenantid):
    if request.method == "GET":
        return list_networks(request, vimid, tenantid)
    elif request.method == "POST":
        return create_network(request, vimid, tenantid)


@api_view(http_method_names=['DELETE','GET'])
def delete_list_network(request, vimid, tenantid, networkid):
    if request.method == "DELETE":
        return delete_network(request, vimid, tenantid, networkid)
    elif request.method == "GET":
        return list_network(request, vimid, tenantid, networkid)


def create_network(request, vimid, tenantid):
    logger.info("Enter %s, method is %s, vim_id is %s",
                syscomm.fun_name(), request.method, vimid)
    net = networking.Network()
    body = json.loads(request.body)
    try:
        resp = net.create_network(vimid, tenantid, body)
        return Response(data=resp, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response(data={'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def list_network(request, vimid, tenantid, networkid):
    logger.info("Enter %s, method is %s, vim_id is %s",
                syscomm.fun_name(), request.method, vimid)
    net = networking.Network()
    try:
        resp = net.list_network(vimid, tenantid, networkid)
        return Response(data=resp, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response(data={'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def delete_network(request, vimid, tenantid, networkid):
    logger.info("Enter %s, method is %s, vim_id is %s",
                syscomm.fun_name(), request.method, vimid)
    net = networking.Network()
    try:
        resp = net.delete_network(vimid, tenantid, networkid)
        return Response(data=resp, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response(data={'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def list_networks(request, vimid, tenantid):
    logger.info("Enter %s, method is %s, vim_id is %s",
                syscomm.fun_name(), request.method, vimid)
    net = networking.Network()
    try:
        resp = net.list_networks(vimid, tenantid)
        return Response(data=resp, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response(data={'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
