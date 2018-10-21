#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""
from __future__ import print_function

import json
import traceback
from app.dao.time_series_detector.anomaly_op import *
from app.utils.utils import *


class AnomalyService(object):

    def __init__(self):
        self.__anomaly = AbnormalOperation()

    def query_anomaly(self, body):
        try:
            form = json.loads(body)
            ret_code, ret_data = check_value(form)
            if OP_SUCCESS == ret_code:
                ret_code, ret_data = self.__anomaly.get_anomaly(form)
            return_dict = build_ret_data(ret_code, ret_data)
        except Exception as ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict

    def update_anomaly(self, body):
        try:
            form = json.loads(body)
            ret_code, ret_data = check_value(form)
            if OP_SUCCESS == ret_code:
                print(form)
                ret_code, ret_data = self.__anomaly.update_anomaly(form)
            return_dict = build_ret_data(ret_code, ret_data)

        except Exception as ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict
