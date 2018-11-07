#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import traceback
from functools import wraps
from errorcode import *

DEFAULT_WINDOW = 180
INPUT_LEN_ENG_MAX = 32
INPUT_LEN_CH_MAX = 64
INPUT_ITEM_PER_PAGE_MAX = 100
INPUT_LIST_LEN_MAX = 5
VALUE_LEN_MAX = 50000
UPLOAD_FILE = '/tmp/tmpfile_%s.csv'
MARK_POSITIVE = 1
MARK_NEGATIVE = 2


def build_ret_data(ret_code, data=""):
    return {"code": ret_code, "msg": ERR_CODE[ret_code], "data": data}


def exce_service(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            ret_code, ret_data = func(*args, **kwargs)
            return_dict = build_ret_data(ret_code, ret_data)
        except Exception as ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict
    return wrapper
