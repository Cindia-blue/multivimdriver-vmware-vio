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
import json
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.nova import OperateServers
from vio.swagger import nova_utils

logger = logging.getLogger(__name__)


class ListServersView(APIView):

    def post(self, request, vimid, tenantid):
        create_req = json.loads(request.body)

        vim_info = extsys.get_vim_by_id(vimid)
        data = {'vimid': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url'],
                'project_name': vim_info['tenant']}

        servers_op = OperateServers.OperateServers()
        server = servers_op.create_server(data, tenantid, create_req)
        server_dict = nova_utils.server_formatter(server)

        rsp = {'vimid': vim_info['vimId'],
               'vimName': vim_info['name'],
               'server': server_dict}
        return Response(data=rsp, status=status.HTTP_200_OK)

    def get(self, request, vimid, tenantid):
        vim_info = extsys.get_vim_by_id(vimid)
        data = {'vimid': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url'],
                'project_name': vim_info['tenant']}

        servers_op = OperateServers.OperateServers()
        servers = servers_op.list_servers(data, tenantid)

        servers_resp = []
        for server in servers:
            servers_resp.append(nova_utils.server_formatter(server))

        rsp = {'vimid': vim_info['vimId'],
               'vimName': vim_info['name'],
               'servers': servers_resp}

        return Response(data=rsp, status=status.HTTP_200_OK)


class GetServerView(APIView):

    def get(self, request, vimid, tenantid, serverid):
        vim_info = extsys.get_vim_by_id(vimid)
        data = {'vimid': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url'],
                'project_name': vim_info['tenant']}

        servers_op = OperateServers.OperateServers()
        server = servers_op.get_server(data, tenantid, serverid)
        server_dict = nova_utils.server_formatter(server)

        rsp = {'vimid': vim_info['vimId'],
               'vimName': vim_info['name'],
               'server': server_dict}

        return Response(data=rsp, status=status.HTTP_200_OK)

    def delete(self, request, vimid, tenantid, serverid):
        servers_op = OperateServers.OperateServers()
        vim_info = extsys.get_vim_by_id(vimid)
        data = {'vimid': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url'],
                'project_name': vim_info['tenant']}
        servers_op.delete_server(data, tenantid, serverid)
        return Response(status=status.HTTP_204_NO_CONTENT)
