#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import numpy as np
from app.config.errorcode import *
from app.config.common import *


def is_standard_time_series(time_series, window=180):
    """
    Check the length of time_series. If window = 180, then the length of time_series should be 903.
    The mean value of last window should be larger than 0.

    :param time_series: the time series to check, like [data_c, data_b, data_a]
    :type time_series: pandas.Series
    :param window: the length of window
    :return: True or False
    :return type: boolean
    """
    if len(time_series) == 5 * window + 3 and np.mean(time_series[(4 * window + 2):]) > 0:
        return True
    else:
        return False


def split_time_series(time_series, window=180):
    """
    Spilt the time_series into five parts. Each has a length of window + 1

    :param time_series: [data_c, data_b, data_a]
    :param window: the length of window
    :return: spilt list [[data_c_left], [data_c_right], [data_b_left], [data_b_right], [data_a]]
    """
    data_c_left = time_series[0:(window + 1)]
    data_c_right = time_series[window:(2 * window + 1)]
    data_b_left = time_series[(2 * window + 1):(3 * window + 2)]
    data_b_right = time_series[(3 * window + 1):(4 * window + 2)]
    data_a = time_series[(4 * window + 2):]
    split_time_series = []
    split_time_series.append(data_c_left)
    split_time_series.append(data_c_right)
    split_time_series.append(data_b_left)
    split_time_series.append(data_b_right)
    split_time_series.append(data_a)
    return split_time_series


def normalize_time_series(split_time_series):
    """
    Normalize the split_time_series.

    :param split_time_series: [[data_c_left], [data_c_right], [data_b_left], [data_b_right], [data_a]]
    :return: all list / mean(split_time_series)
    """
    value = np.mean(split_time_series[4])
    if value > 1:
        normalized_data_c_left = list(split_time_series[0] / value)
        normalized_data_c_right = list(split_time_series[1] / value)
        normalized_data_b_left = list(split_time_series[2] / value)
        normalized_data_b_right = list(split_time_series[3] / value)
        normalized_data_a = list(split_time_series[4] / value)
    else:
        normalized_data_c_left = split_time_series[0]
        normalized_data_c_right = split_time_series[1]
        normalized_data_b_left = split_time_series[2]
        normalized_data_b_right = split_time_series[3]
        normalized_data_a = split_time_series[4]
    normalized_split_time_series = []
    normalized_split_time_series.append(normalized_data_c_left)
    normalized_split_time_series.append(normalized_data_c_right)
    normalized_split_time_series.append(normalized_data_b_left)
    normalized_split_time_series.append(normalized_data_b_right)
    normalized_split_time_series.append(normalized_data_a)
    return normalized_split_time_series


def build_ret_data(ret_code, data=""):
    return {"code": ret_code, "msg": ERR_CODE[ret_code], "data": data}


def validate_value(data):
    if isinstance(data, unicode):
        if len(data) > INPUT_LEN_ENG_MAX:
            return CHECK_PARAM_FAILED
    elif isinstance(data, str):
        if len(data) > INPUT_LEN_ENG_MAX:
            return CHECK_PARAM_FAILED
    elif isinstance(data, list):
        if len(data) > INPUT_LIST_LEN_MAX:
            return CHECK_PARAM_FAILED
        for item in data:
            ret_code = validate_value(item)
            if ret_code != 0:
                return ret_code
    return 0


def check_value(data):
    if 'attrId' in data:
        ret_code = validate_value(data['attrId'])
        if ret_code != 0:
            return CHECK_PARAM_FAILED, "attrId too long"
    if 'attrName' in data:
        ret_code = validate_value(data['attrName'])
        if ret_code != 0:
            return CHECK_PARAM_FAILED, "attrName too long"
    if 'viewId' in data:
        ret_code = validate_value(data['viewId'])
        if ret_code != 0:
            return CHECK_PARAM_FAILED, "viewId too long"
    if 'viewName' in data:
        ret_code = validate_value(data['viewName'])
        if ret_code != 0:
            return CHECK_PARAM_FAILED, "viewName too long"
    if 'itemPerPage' in data:
        if data['itemPerPage'] > INPUT_ITEM_PER_PAGE_MAX:
            return CHECK_PARAM_FAILED, "itemPerPage too big"
    if 'beginTime' in data:
        if len(str(data['beginTime'])) > INPUT_LEN_ENG_MAX:
            return CHECK_PARAM_FAILED, "beginTime too long"
    if 'endTime' in data:
        if len(str(data['endTime'])) > INPUT_LEN_ENG_MAX:
            return CHECK_PARAM_FAILED, "endTime too long"
    if 'updateTime' in data:
        if len(str(data['updateTime'])) > INPUT_LEN_ENG_MAX:
            return CHECK_PARAM_FAILED, "updateTime too long"
    if 'source' in data:
        ret_code = validate_value(data['source'])
        if ret_code != 0:
            return CHECK_PARAM_FAILED, "source too long"
    if 'trainOrTest' in data:
        ret_code = validate_value(data['source'])
        if ret_code != 0:
            return CHECK_PARAM_FAILED, "trainOrTest too long"
    if 'positiveOrNegative' in data:
        ret_code = validate_value(data['positiveOrNegative'])
        if ret_code != 0:
            return CHECK_PARAM_FAILED, "positiveOrNegative too long"
    if 'window' in data:
        if len(str(data['window'])) > INPUT_LEN_ENG_MAX:
            return CHECK_PARAM_FAILED, "window"
    if 'dataTime' in data:
        if len(str(data['dataTime'])) > INPUT_LEN_ENG_MAX:
            return CHECK_PARAM_FAILED, "dataTime too long"
    if 'dataC' in data:
        if len(str(data['dataC'])) > VALUE_LEN_MAX:
            return CHECK_PARAM_FAILED, "dataC too long"
    if 'dataB' in data:
        if len(str(data['dataB'])) > VALUE_LEN_MAX:
            return CHECK_PARAM_FAILED, "dataB too long"
    if 'dataA' in data:
        if len(str(data['dataA'])) > VALUE_LEN_MAX:
            return CHECK_PARAM_FAILED, "dataA too long"
    return 0, ""
