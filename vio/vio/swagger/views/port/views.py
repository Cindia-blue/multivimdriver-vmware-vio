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

import logging
import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from vio.pub.utils import syscomm
from vio.pub.vim.vimapi.network import OperatePort

logger = logging.getLogger(__name__)


class CreatePortView(APIView):
    def post(self, request, vimid, tenantid):
        logger.info("Enter %s, method is %s, vim_id is %s",
                    syscomm.fun_name(), request.method, vimid)
        port = OperatePort.OperatePort()
        try:
            body = json.loads(request.body)
        except Exception as e:
            return Response(data={'error': 'Fail to decode request body.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            port_name = body.get('name')
            port_id = body.get('id', None)
            target = port_id or port_name
            resp = port.list_port(vimid, tenantid, target, ignore_missing=True)
            if resp:
                resp['returnCode'] = 0
                return Response(data=resp, status=status.HTTP_200_OK)
            else:
                resp = port.create_port(vimid, tenantid, body)
                resp['returnCode'] = 1
                return Response(data=resp, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, vimid, tenantid):
        logger.info("Enter %s, method is %s, vim_id is %s",
                    syscomm.fun_name(), request.method, vimid)
        query = dict(request.query_params)
        port = OperatePort.OperatePort()
        try:
            resp = port.list_ports(vimid, tenantid, **query)
            return Response(data=resp, status=status.HTTP_200_OK)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeletePortView(APIView):

    def get(self, request, vimid, tenantid, portid):
        logger.info("Enter %s, method is %s, vim_id is %s",
                    syscomm.fun_name(), request.method, vimid)
        port = OperatePort.OperatePort()
        try:
            resp = port.list_port(vimid, tenantid, portid)
            return Response(data=resp, status=status.HTTP_200_OK)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, vimid, tenantid, portid):
        logger.info("Enter %s, method is %s, vim_id is %s",
                    syscomm.fun_name(), request.method, vimid)
        port = OperatePort.OperatePort()
        try:
            resp = port.delete_port(vimid, tenantid, portid)
            return Response(data=resp, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)



