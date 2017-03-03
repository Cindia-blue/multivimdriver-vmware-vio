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

import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import volume_utils

from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.keystone import OperateTenant
from vio.pub.vim.vimapi.glance import OperateImage
from vio.pub.vim.vimapi.cinder import OperateVolume

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


class CreateListImagesView(APIView):
    def get(self, request, vimid, tenantid):
        vim_info = extsys.get_vim_by_id(vimid)

        data = {}
        data['vimid'] = vim_info['vimId']
        data['vimName'] = vim_info['name']
        data['username'] = vim_info['userName']
        data['password'] = vim_info['password']
        data['url'] = vim_info['url']
        data['project_name'] = vim_info['tenant']
        data['tenantid'] = tenantid

        image_instance = OperateImage.OperateImage()
        images = image_instance.get_vim_images(data)

        rsp = {}
        rsp['vimid'] = vim_info['vimId']
        rsp['vimName'] = vim_info['name']
        rsp['teanantid'] = tenantid
        rsp['images'] = []

        for image in images:
            vim_image = {}
            vim_image['id'] = image['id']
            vim_image['name'] = image['name']
            vim_image['size'] = image['size']/1024
            vim_image['status'] = image['status']
            vim_image['imageType'] = image['disk_format']
            vim_image['containerFormat'] = image['container_format']
            vim_image['visibility'] = image['visibility']
            rsp['images'].append(vim_image)

        return Response(data=rsp, status=status.HTTP_200_OK)

    def post(self, request, vimid, tenantid):
        vim_info = extsys.get_vim_by_id(vimid)

        data = {}
        data['vimid'] = vim_info['vimId']
        data['vimName'] = vim_info['name']
        data['username'] = vim_info['userName']
        data['password'] = vim_info['password']
        data['url'] = vim_info['url']
        data['project_name'] = vim_info['tenant']

        image_instance = OperateImage.OperateImage()
        image = image_instance.create_vim_image(data)

        rsp = {}
        rsp['vimid'] = vim_info['vimId']
        rsp['vimName'] = vim_info['name']
        rsp['image'] = []

        return Response(data=rsp, status=status.HTTP_200_OK)



class ListTenantsView(APIView):
    def get(self, request, vimid):
        vim_info = extsys.get_vim_by_id(vimid)

        data = {}
        data['vimid'] = vim_info['vimId']
        data['vimName'] = vim_info['name']
        data['username'] = vim_info['userName']
        data['password'] = vim_info['password']
        data['url'] = vim_info['url']
        data['project_name'] = vim_info['tenant']

        tenant_instance = OperateTenant.OperateTenant()
        projects = tenant_instance.get_projects(data)

        rsp = {}
        rsp['vimid'] = vim_info['vimId']
        rsp['vimName'] = vim_info['name']
        rsp['tenants'] = []

        for project in projects:
            tenant = {}
            logger.debug("testproject is : ", project)
            tenant['id'] = project['id']
            tenant['name'] = project['name']
            rsp['tenants'].append(tenant)
        return Response(data=rsp, status=status.HTTP_200_OK)


class ListServersView(APIView):

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


class SwaggerJsonView(APIView):
    def get(self, request):
        json_file = os.path.join(os.path.dirname(__file__), 'multivim.flavor.swagger.json')
        f = open(json_file)
        json_data = json.JSONDecoder().decode(f.read())
        f.close()
        json_file = os.path.join(os.path.dirname(__file__), 'multivim.image.swagger.json')
        f = open(json_file)
        json_data_temp = json.JSONDecoder().decode(f.read())
        f.close()
        json_data["paths"].update(json_data_temp["paths"])
        json_data["definitions"].update(json_data_temp["definitions"])
        json_file = os.path.join(os.path.dirname(__file__), 'multivim.network.swagger.json')
        f = open(json_file)
        json_data_temp = json.JSONDecoder().decode(f.read())
        f.close()
        json_data["paths"].update(json_data_temp["paths"])
        json_data["definitions"].update(json_data_temp["definitions"])
        json_file = os.path.join(os.path.dirname(__file__), 'multivim.subnet.swagger.json')
        f = open(json_file)
        json_data_temp = json.JSONDecoder().decode(f.read())
        f.close()
        json_data["paths"].update(json_data_temp["paths"])
        json_data["definitions"].update(json_data_temp["definitions"])
        json_file = os.path.join(os.path.dirname(__file__), 'multivim.server.swagger.json')
        f = open(json_file)
        json_data_temp = json.JSONDecoder().decode(f.read())
        f.close()
        json_data["paths"].update(json_data_temp["paths"])
        json_data["definitions"].update(json_data_temp["definitions"])
        json_file = os.path.join(os.path.dirname(__file__), 'multivim.volume.swagger.json')
        f = open(json_file)
        json_data_temp = json.JSONDecoder().decode(f.read())
        f.close()
        json_data["paths"].update(json_data_temp["paths"])
        json_data["definitions"].update(json_data_temp["definitions"])
        json_file = os.path.join(os.path.dirname(__file__), 'multivim.vport.swagger.json')
        f = open(json_file)
        json_data_temp = json.JSONDecoder().decode(f.read())
        f.close()
        json_data["paths"].update(json_data_temp["paths"])
        json_data["definitions"].update(json_data_temp["definitions"])
        json_file = os.path.join(os.path.dirname(__file__), 'multivim.tenant.swagger.json')
        f = open(json_file)
        json_data_temp = json.JSONDecoder().decode(f.read())
        f.close()
        json_data["paths"].update(json_data_temp["paths"])
        json_data["definitions"].update(json_data_temp["definitions"])
        json_file = os.path.join(os.path.dirname(__file__), 'multivim.host.swagger.json')
        f = open(json_file)
        json_data_temp = json.JSONDecoder().decode(f.read())
        f.close()
        json_data["paths"].update(json_data_temp["paths"])
        json_data["definitions"].update(json_data_temp["definitions"])
        json_file = os.path.join(os.path.dirname(__file__), 'multivim.limit.swagger.json')
        f = open(json_file)
        json_data_temp = json.JSONDecoder().decode(f.read())
        f.close()
        json_data["paths"].update(json_data_temp["paths"])
        json_data["definitions"].update(json_data_temp["definitions"])
        json_data["basePath"] = "/openoapi/multivim-vio/v1/"
        json_data["info"]["title"] = "MultiVIM driver of OpenStack VIO Service NBI"
        return Response(json_data)

