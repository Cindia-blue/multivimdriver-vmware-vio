# Copyright 2017 VMware, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging
import threading
import urllib2


from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.baseclient import baseclient
from vio.swagger import image_utils

logger = logging.getLogger(__name__)


running_threads = {}
running_thread_lock = threading.Lock()

class imageThread(threading.Thread):
    def __init__(self, vimid, tenantid, image, imagefd):

        threading.Thread.__init__(self)
        self.imageid = image.id
        self.imagefd = imagefd
        self.vimid = vimid
        self.tenantid = tenantid
        self.image = image


    def run(self):

        logger.debug("start imagethread")
        self.transfer_image(self.vimid, self.tenantid, self.image, self.imagefd)
        running_thread_lock.acquire()
        running_threads.pop(self.imageid)
        running_thread_lock.release()


    def transfer_image(self, vimid, tenantid, image, imagefd):

        logger.debug("Image----transfer_image")
        vim_info = extsys.get_vim_by_id(vimid)

        param = image_utils.sdk_param_formatter(vim_info)
        data = imagefd.read()
        client = baseclient()
        client.glance(param).upload_image(data, image)


class OperateImage(baseclient):

    def __init__(self, params):

        super(OperateImage, self).__init__()
        self.param = image_utils.sdk_param_formatter(params)

    def get_vim_images(self, **query):

        images = self.glance(self.param).list_images(**query)
        return images

    def get_vim_image(self, imageid):

        image = self.glance(self.param).get_image(imageid)
        return image

    def delete_vim_image(self, imageid):

        image = self.glance(self.param).delete_image(imageid)
        return image

    def create_vim_image(self, vimid, tenantid,  **req_body):

        imageurl = req_body.pop('imagePath', None)
        imagefd = urllib2.urlopen(imageurl)

        image = self.glance(self.param).create_image(**req_body)

        upload_image_thread = imageThread(vimid, tenantid, image, imagefd)
        logger.debug("launch thread to upload image: %s" % image.id)
        running_thread_lock.acquire()
        running_threads[image.id] = image.id
        running_thread_lock.release()
        try:
            upload_image_thread.start()
        except Exception as ex:
            pass
        return image