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
from vio.pub.vim.vimapi.network import OperateSubnet

logger = logging.getLogger(__name__)


class CreateSubnetView(APIView):
    def post(self, request, vimid, tenantid):
        logger.info("Enter %s, method is %s, vim_id is %s",
                    syscomm.fun_name(), request.method, vimid)
        subnet = OperateSubnet.OperateSubnet()
        try:
            body = json.loads(request.body)
        except Exception as e:
            return Response(data={'error': 'Fail to decode request body.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            subnet_name = body.get('name')
            subnet_id = body.get('id', None)
            target = subnet_id or subnet_name
            resp = subnet.list_subnet(vimid, tenantid, target, ignore_missing=True)
            if resp:
                resp['returnCode'] = 0
            else:
                resp = subnet.create_subnet(vimid, tenantid, body)
                resp['returnCode'] = 1
            return Response(data=resp, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, vimid, tenantid):
        logger.info("Enter %s, method is %s, vim_id is %s",
                    syscomm.fun_name(), request.method, vimid)
        query = dict(request.query_params)
        subnet =  OperateSubnet.OperateSubnet()
        try:
            resp = subnet.list_subnets(vimid, tenantid, **query)
            return Response(data=resp, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteSubnetView(APIView):

    def get(self, request, vimid, tenantid, subnetid):
        logger.info("Enter %s, method is %s, vim_id is %s",
                    syscomm.fun_name(), request.method, vimid)
        subnet =  OperateSubnet.OperateSubnet()
        try:
            resp = subnet.list_subnet(vimid, tenantid, subnetid)
            return Response(data=resp, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, vimid, tenantid, subnetid):
        logger.info("Enter %s, method is %s, vim_id is %s",
                    syscomm.fun_name(), request.method, vimid)
        subnet =  OperateSubnet.OperateSubnet()
        try:
            resp = subnet.delete_subnet(vimid, tenantid, subnetid)
            return Response(data=resp, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



