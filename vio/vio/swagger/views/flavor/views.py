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

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.nova import OperateFlavors
from vio.swagger import nova_utils


class FlavorsView(APIView):

    def post(self, request, vimid, tenantid):
        create_req = json.loads(request.body)

        vim_info = extsys.get_vim_by_id(vimid)
        data = {'vimid': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url'],
                'project_name': vim_info['tenant']}

        flavors_op = OperateFlavors.OperateFlavors()
        flavor, extra_specs = flavors_op.create_flavor(data, tenantid, create_req)
        flavor_dict = nova_utils.flavor_formatter(flavor, extra_specs)

        rsp = {'vimid': vim_info['vimId'],
               'vimName': vim_info['name'],
               'tenantId': tenantid,
               'returnCode': 1}
        rsp.update(flavor_dict)
        return Response(data=rsp, status=status.HTTP_200_OK)

    def get(self, request, vimid, tenantid):
        vim_info = extsys.get_vim_by_id(vimid)
        data = {'vimid': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url'],
                'project_name': vim_info['tenant']}

        flavors_op = OperateFlavors.OperateFlavors()
        flavors_result = flavors_op.list_flavors(data, tenantid)
        flavors_dict = [nova_utils.flavor_formatter(flavor, extra)
                        for flavor, extra in flavors_result]

        rsp = {'vimid': vim_info['vimId'],
               'vimName': vim_info['name'],
               'flavors': flavors_dict}

        return Response(data=rsp, status=status.HTTP_200_OK)


class FlavorView(APIView):

    def get(self, request, vimid, tenantid, flavorid):
        vim_info = extsys.get_vim_by_id(vimid)
        data = {'vimid': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url'],
                'project_name': vim_info['tenant']}

        flavors_op = OperateFlavors.OperateFlavors()
        flavor, extra_specs = flavors_op.get_flavor(data, tenantid, flavorid)
        flavor_dict = nova_utils.flavor_formatter(flavor, extra_specs)

        rsp = {'vimid': vim_info['vimId'],
               'vimName': vim_info['name'],
               'tenantId': tenantid}
        rsp.update(flavor_dict)
        return Response(data=rsp, status=status.HTTP_200_OK)

    def delete(self, request, vimid, tenantid, flavorid):
        vim_info = extsys.get_vim_by_id(vimid)
        data = {'vimid': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url'],
                'project_name': vim_info['tenant']}
        flavors_op = OperateFlavors.OperateFlavors()
        flavors_op.delete_flavor(data, tenantid, flavorid)
        return Response(status=status.HTTP_204_NO_CONTENT)
