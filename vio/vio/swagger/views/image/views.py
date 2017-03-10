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
from vio.pub.vim.vimapi.glance import OperateImage
from vio.swagger import image_utils


class GetDeleteImageView(APIView):

    def get(self, request, vimid, tenantid, imageid):

        vim_info = extsys.get_vim_by_id(vimid)
        image_op = OperateImage.OperateImage(vim_info)
        image = image_op.get_vim_image(imageid)

        vim_rsp = image_utils.vim_formatter(vim_info, tenantid)
        rsp = image_utils.image_formatter(image)
        rsp.update(vim_rsp)

        return Response(data=rsp, status=status.HTTP_200_OK)

    def delete(self, request, vimid, tenantid, imageid):

        vim_info = extsys.get_vim_by_id(vimid)
        image_op = OperateImage.OperateImage(vim_info)
        image_op.delete_vim_image(imageid)

        return Response(status="204")

class CreateListImagesView(APIView):

    def get(self, request, vimid, tenantid):

        vim_info = extsys.get_vim_by_id(vimid)
        query_data = dict(request.query_params)
        image_instance = OperateImage.OperateImage(vim_info)
        images = image_instance.get_vim_images(**query_data)

        rsp = {}
        rsp['images'] = []
        vim_rsp = image_utils.vim_formatter(vim_info, tenantid)
        for image in images:
            rsp['images'].append(image_utils.image_formatter(image))
        rsp.update(vim_rsp)

        return Response(data=rsp, status=status.HTTP_200_OK)

    def post(self, request, vimid, tenantid):
        vim_info = extsys.get_vim_by_id(vimid)

        req_body = json.loads(request.body)
        vim_rsp = image_utils.vim_formatter(vim_info, tenantid)
        image_instance = OperateImage.OperateImage(vim_info)

        images = image_instance.get_vim_images()
        for image in images:
            if image.name == req_body.get('name'):
                image_info = image_instance.get_vim_image(image.id)
                rsp = image_utils.image_formatter(image_info)
                rsp['returnCode'] = '0'
                rsp.update(vim_rsp)
                return Response(data=rsp, status=status.HTTP_200_OK)

        param = image_utils.req_body_formatter(req_body)
        image = image_instance.create_vim_image(vimid, tenantid, **param)

        rsp = image_utils.image_formatter(image)
        rsp.update(vim_rsp)
        rsp['returnCode'] = '1'

        return Response(data=rsp, status=status.HTTP_200_OK)