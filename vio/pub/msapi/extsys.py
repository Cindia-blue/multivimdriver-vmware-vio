# Copyright 2017 VMware Corporation.
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

import json
import logging

from vio.pub.exceptions import VimDriverVioException
from vio.pub.utils.restcall import req_by_msb

logger = logging.getLogger(__name__)


def get_vims():
    ret = req_by_msb("/openoapi/extsys/v1/vims", "GET")
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise VimDriverVioException("Failed to query vims from extsys.")
    return json.JSONDecoder().decode(ret[1])


def get_vim_by_id(vim_id):
    ret = req_by_msb("/openoapi/extsys/v1/vims/%s" % vim_id, "GET")
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise VimDriverVioException("Failed to query vim(%s) from extsys." % vim_id)
    return json.JSONDecoder().decode(ret[1])


