# Copyright 2016 ZTE Corporation.
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


from vio.pub.msapi import extsys

logger = logging.getLogger(__name__)


class OperatorImage(object):
    def __init__(self, data):
        self.ns_model_data = data["ns_model_data"]
        self.fp_inst_id = data["fpinstid"]
        self.flow_classifiers_model = get_fp_model_by_fp_inst_id(data["ns_model_data"], self.fp_inst_id)["properties"][
            "policy"]
        self.sdnControllerId = ""
        self.url = ""
        self.dscp = ""
        self.ip_proto = ""
        self.source_port_range = ""
        self.dest_port_range = ""
        self.source_ip_range = ""
        self.dest_ip_range = ""
        self.flow_classfier_id = ""


    def create_image(self, data):
        pass

    def list_images(self, data):
        pass

    def delete_image(self, data):
        pass

    def get_image(self, data):
        pass

