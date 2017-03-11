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


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.nova import OperateLimits
from vio.swagger import nova_utils


class LimitsView(APIView):

    def get(self, request, vimid, tenantid):
        vim_info = extsys.get_vim_by_id(vimid)
        data = {'vimid': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url'],
                'project_name': vim_info['tenant']}

        servers_op = OperateLimits.OperateLimits()
        try:
            server_limits = servers_op.get_limits(data, tenantid)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        rsp = {'vimid': vim_info['vimId'],
               'vimName': vim_info['name'],
               'tenantId': tenantid}
        rsp.update(nova_utils.server_limits_formatter(server_limits))

        return Response(data=rsp, status=status.HTTP_200_OK)
