#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import json
import traceback
from app.dao.time_series_detector.train_op import *
from app.config.errorcode import *
from app.utils.utils import *


class TrainService(object):

    def __init__(self):
        self.__train_op = TrainOperation()

    def query_train(self, body):
        try:
            form = json.loads(body)
            ret_code, ret_data = check_value(form)
            if OP_SUCCESS == ret_code:
                ret_code, ret_data = self.__train_op.query_train(form)
            return_dict = build_ret_data(ret_code, ret_data)
        except Exception, ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict

    def query_train_source(self):
        try:
            ret_code, ret_data = self.__train_op.query_train_source()
            return_dict = build_ret_data(ret_code, ret_data)
        except Exception, ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict

    def delete_train(self, body):
        try:
            form = json.loads(body)
            ret_code, ret_data = check_value(form)
            if OP_SUCCESS == ret_code:
                ret_code, ret_data = self.__train_op.delete_train(form)
            return_dict = build_ret_data(ret_code, ret_data)
        except Exception, ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict
