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


class CreateListVolumeView(APIView):

    def get(self, request, vimid, tenantid):
        vim_info = extsys.get_vim_by_id(vimid)

        data = {
            'vimid' : vim_info['vimId'],
            'vimName' : vim_info['name'],
            'username' : vim_info['userName'],
            'password' : vim_info['password'],
            'url' : vim_info['url'],
            'project_name' : vim_info['tenant']
        }

        volume_op = OperateVolume.OperateVolume()
        volumes = volume_op.get_vim_volumes(data, tenantid)

        volume_resp = []

        for volume in volumes:
            volume_id = volume.id
            volume_info = volume_op.get_vim_volume(data, tenantid, volume_id)
            volume_resp.append(volume_utils.VolumeFormatter(volume_info))

        rsp = {
            'vimid' : vim_info['vimId'],
            'vimName' : vim_info['name'],
            'volumes' : volume_resp
        }
        return Response(data=rsp, status=status.HTTP_200_OK)

    def post(self, request, vimid, tenantid):
        vim_info = extsys.get_vim_by_id(vimid)

        data = {
            'vimid' : vim_info['vimId'],
            'vimName' : vim_info['name'],
            'username' : vim_info['userName'],
            'password' : vim_info['password'],
            'url' : vim_info['url'],
            'project_name' : vim_info['tenant']
        }

        logger.debug(request.body)
        json_body = json.loads(request.body)
        param = {
            'name' : json_body['name'],
            'size' : json_body['volumeSize'],
            'availability_zone' : json_body['availabilityZone'],
            'imageRef' : json_body['imageName'],
            'volume_type' : json_body['volumeType']
        }

        logger.debug(param)
        body = {}
        body["volume"] = param
        logger.debug(body)

        volume_op = OperateVolume.OperateVolume()
        volume = volume_op.create_vim_volume(data, tenantid, body)

        rsp = {
            'vimid' : vim_info['vimId'],
            'vimName' : vim_info['name'],
            'volumes' : volume
        }
        return Response(data=rsp, status=status.HTTP_200_OK)


class GetDeleteVolumeView(APIView):

    def get(self, request, vimid, tenantid, volumeid):
        vim_info = extsys.get_vim_by_id(vimid)

        data = {
            'vimid' : vim_info['vimId'],
            'vimName' : vim_info['name'],
            'username' : vim_info['userName'],
            'password' : vim_info['password'],
            'url' : vim_info['url'],
            'project_name' : vim_info['tenant']
        }

        volume_op = OperateVolume.OperateVolume()
        volume = volume_op.get_vim_volume(data, tenantid, volumeid)

        vim_volume  = volume_utils.VolumeFormatter(volume)

        rsp = {
            'vimid' : vim_info['vimId'],
            'vimName' : vim_info['name'],
            'volumes' : vim_volume
        }
        return Response(data=rsp, status=status.HTTP_200_OK)

    def post(self, request, vimid, tenantid, volumeid):
        vim_info = extsys.get_vim_by_id(vimid)

        data = {
            'vimid' : vim_info['vimId'],
            'vimName' : vim_info['name'],
            'username' : vim_info['userName'],
            'password' : vim_info['password'],
            'url' : vim_info['url'],
            'project_name' : vim_info['tenant']
        }

        volume_op = OperateVolume.OperateVolume()
        volume = volume_op.delete_vim_volume(data, tenantid, volumeid)
