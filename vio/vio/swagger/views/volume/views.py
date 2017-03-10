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
from vio.pub.vim.vimapi.cinder import OperateVolume

from vio.swagger import volume_utils

logger = logging.getLogger(__name__)


class GetDeleteVolumeView(APIView):

    def get(self, request, vimid, tenantid, volumeid):
        vim_info = extsys.get_vim_by_id(vimid)
        volume_op = OperateVolume.OperateVolume(vim_info)

        try:
            volume = volume_op.get_vim_volume(volumeid)
            vim_rsp = volume_utils.vim_formatter(vim_info, tenantid)
            rsp  = volume_utils.volume_formatter(volume)
            rsp.update(vim_rsp)
            return Response(data=rsp, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, vimid, tenantid, volumeid):
        vim_info = extsys.get_vim_by_id(vimid)
        volume_op = OperateVolume.OperateVolume(vim_info)

        try:
            volume_op.delete_vim_volume(volumeid)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateListVolumeView(APIView):

    def get(self, request, vimid, tenantid):
        vim_info = extsys.get_vim_by_id(vimid)
        query_data = dict(request.query_params)
        volume_op = OperateVolume.OperateVolume(vim_info)

        try:
            volumes = volume_op.get_vim_volumes(**query_data)
            rsp = {}
            rsp['volumes'] = []

            vim_rsp = volume_utils.vim_formatter(vim_info, tenantid)
            for volume in volumes:
                volume_info = volume_op.get_vim_volume(volume.id)
                rsp['volumes'].append(volume_utils.volume_formatter(volume_info))

            rsp.update(vim_rsp)
            return Response(data=rsp, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request, vimid, tenantid):
        vim_info = extsys.get_vim_by_id(vimid)
        volume_op = OperateVolume.OperateVolume(vim_info)

        try:
            volumes_detail = volume_op.get_vim_volumes()
            json_body = json.loads(request.body)

            vim_rsp = volume_utils.vim_formatter(vim_info, tenantid)
            for volume in volumes_detail:
                if volume.name == json_body.get('name'):
                    volume_info = volume_op.get_vim_volume(volume.id)
                    rsp  = volume_utils.volume_formatter(volume_info)
                    rsp['returnCode'] = 0
                    rsp.update(vim_rsp)
                    return Response(data=rsp, status=status.HTTP_200_OK)

            param = volume_utils.req_body_formatter(json_body)
            volume_info = volume_op.create_vim_volume(**param)
            rsp  = volume_utils.volume_formatter(volume_info)
            rsp['returnCode'] = 1
            rsp.update(vim_rsp)
            return Response(data=rsp, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)