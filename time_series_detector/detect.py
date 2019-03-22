#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import os
from time_series_detector.algorithm import isolation_forest, ewma, polynomial_interpolation, statistic, xgboosting
from time_series_detector.common.tsd_errorcode import *
from time_series_detector.common.tsd_common import *
MODEL_PATH = os.path.join(os.path.dirname(__file__), './model/')


class Detect(object):

    def __init__(self):
        self.iforest_obj = isolation_forest.IForest()
        self.ewma_obj = ewma.Ewma()
        self.polynomial_obj = polynomial_interpolation.PolynomialInterpolation()
        self.statistic_obj = statistic.Statistic()
        self.supervised_obj = xgboosting.XGBoosting()

    def __list_is_digit(self, data):
        for index in data:
            try:
                float(index)
            except ValueError:
                return False
        return True

    def __check_param(self, data):
        if ("dataC" not in data.keys()) or ("dataB" not in data.keys()) or ("dataA" not in data.keys()):
            return TSD_CHECK_PARAM_FAILED, "missing parameter"
        if not data['dataA']:
            return TSD_CHECK_PARAM_FAILED, "dataA can not be empty"
        if not data['dataB']:
            return TSD_CHECK_PARAM_FAILED, "dataB can not be empty"
        if not data['dataC']:
            return TSD_CHECK_PARAM_FAILED, "dataC can not be empty"
        if not self.__list_is_digit(data['dataA'].split(',')):
            return TSD_CHECK_PARAM_FAILED, "dataA contains illegal numbers"
        if not self.__list_is_digit(data['dataB'].split(',')):
            return TSD_CHECK_PARAM_FAILED, "dataB contains illegal numbers"
        if not self.__list_is_digit(data['dataC'].split(',')):
            return TSD_CHECK_PARAM_FAILED, "dataC contains illegal numbers"
        if "window" in data:
            window = data["window"]
        else:
            window = DEFAULT_WINDOW
        if len(data['dataC'].split(',')) != (2 * window + 1):
            return TSD_CHECK_PARAM_FAILED, "dataC length does not match"
        if len(data['dataB'].split(',')) != (2 * window + 1):
            return TSD_CHECK_PARAM_FAILED, "dataB length does not match"
        if len(data['dataA'].split(',')) != (window + 1):
            return TSD_CHECK_PARAM_FAILED, "dataA length does not match"
        return TSD_OP_SUCCESS, ""

    def value_predict(self, data):
        """
        Predict if the latest value is an outlier or not.

        :param data: The attributes are:
                    'window', the length of window,
                    'taskId', the id of detect model,
                    'dataC', a piece of data to learn,
                    'dataB', a piece of data to learn,
                    'dataA', a piece of data to learn and the latest value to be detected.
        :type data: Dictionary-like object
        :return: The attributes are:
                    'p', the class probability,
                    'ret', the result of detect(1 denotes normal, 0 denotes abnormal).
        """
        ret_code, ret_data = self.__check_param(data)
        if ret_code != TSD_OP_SUCCESS:
            return ret_code, ret_data
        if "taskId" in data and data["taskId"]:
            model_name = MODEL_PATH + data["taskId"] + "_model"
        else:
            model_name = MODEL_PATH + "xgb_default_model"
        combined_data = data["dataC"] + "," + data["dataB"] + "," + data["dataA"]
        time_series = map(int, combined_data.split(','))
        if "window" in data:
            window = data["window"]
        else:
            window = DEFAULT_WINDOW
        statistic_result = self.statistic_obj.predict(time_series)
        ewma_result = self.ewma_obj.predict(time_series)
        polynomial_result = self.polynomial_obj.predict(time_series, window)
        if statistic_result == 0 or ewma_result == 0 or polynomial_result == 0 :
            xgb_result = self.supervised_obj.predict(time_series, window, model_name)
            res_value = xgb_result[0]
            prob = xgb_result[1]
        else:
            res_value = 1
            prob = 1
        ret_data = {"ret": res_value, "p": str(prob)}
        return TSD_OP_SUCCESS, ret_data

    def rate_predict(self, data):
        """
        Predict if the latest value is an outlier or not.

        :param data: The attributes are:
                    'dataC', a piece of data to learn,
                    'dataB', a piece of data to learn,
                    'dataA', a piece of data to learn and the latest value to be detected.
        :type data: Dictionary-like object
        :return: The attributes are:
                    'p', the class probability,
                    'ret', the result of detect(1 denotes normal, 0 denotes abnormal).
        """
        combined_data = data["dataC"] + "," + data["dataB"] + "," + data["dataA"]
        time_series = map(float, combined_data.split(','))
        statistic_result = self.statistic_obj.predict(time_series)
        if statistic_result == 0:
            prob = 0
        else:
            prob = 1
        ret_data = {"ret": statistic_result, "p": str(prob)}
        return TSD_OP_SUCCESS, ret_data
