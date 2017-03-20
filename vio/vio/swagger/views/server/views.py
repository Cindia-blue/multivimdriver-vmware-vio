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
import json
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.nova import OperateServers
from vio.swagger import nova_utils
from vio.pub.exceptions import VimDriverVioException

logger = logging.getLogger(__name__)


class ListServersView(APIView):

    def post(self, request, vimid, tenantid):
        try:
            create_req = json.loads(request.body)
        except Exception as e:
            return Response(data={'error': 'Fail to decode request body.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            vim_info = extsys.get_vim_by_id(vimid)
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        data = {'vimid': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url'],
                'project_name': vim_info['tenant']}
        rsp = {'vimId': vim_info['vimId'],
               'vimName': vim_info['name'],
               'tenantId': tenantid}
        servers_op = OperateServers.OperateServers()
        server_name = create_req.get('name', None)
        server_id = create_req.get('id', None)
        try:
            target = server_id or server_name
            server = servers_op.find_server(data, tenantid, target)
            # Find server only returns id and name, fetch all attributes again
            if server:
                server = servers_op.get_server(data, tenantid, server.id)
                rsp['returnCode'] = 0
            else:
                rsp['returnCode'] = 1
                server = servers_op.create_server(data, tenantid, create_req)
        except Exception as e:
            if e.http_status:
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        server_dict = nova_utils.server_formatter(server)
        rsp.update(server_dict)
        return Response(data=rsp, status=status.HTTP_202_ACCEPTED)

    def get(self, request, vimid, tenantid):
        try:
            vim_info = extsys.get_vim_by_id(vimid)
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        data = {'vimid': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url'],
                'project_name': vim_info['tenant']}
        query = dict(request.query_params)
        servers_op = OperateServers.OperateServers()
        try:
            servers = servers_op.list_servers(data, tenantid, **query)
        except Exception as e:
            if e.http_status:
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        servers_resp = []
        for server in servers:
            intfs = servers_op.list_server_interfaces(data, tenantid, server)
            servers_resp.append(nova_utils.server_formatter(
                server, interfaces=intfs))

        rsp = {'vimId': vim_info['vimId'],
               'vimName': vim_info['name'],
               'servers': servers_resp}

        return Response(data=rsp, status=status.HTTP_200_OK)


class GetServerView(APIView):

    def get(self, request, vimid, tenantid, serverid):
        try:
            vim_info = extsys.get_vim_by_id(vimid)
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        data = {'vimid': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url'],
                'project_name': vim_info['tenant']}

        servers_op = OperateServers.OperateServers()
        try:
            server = servers_op.get_server(data, tenantid, serverid)
            intfs = servers_op.list_server_interfaces(data, tenantid, server)
            server_dict = nova_utils.server_formatter(server, interfaces=intfs)
        except Exception as e:
            if e.http_status:
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        rsp = {'vimId': vim_info['vimId'],
               'vimName': vim_info['name'],
               'tenantId': tenantid}
        rsp.update(server_dict)

        return Response(data=rsp, status=status.HTTP_200_OK)

    def delete(self, request, vimid, tenantid, serverid):
        servers_op = OperateServers.OperateServers()
        try:
            vim_info = extsys.get_vim_by_id(vimid)
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        data = {'vimid': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url'],
                'project_name': vim_info['tenant']}
        try:
            servers_op.delete_server(data, tenantid, serverid)
        except Exception as e:
            if e.http_status:
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)
