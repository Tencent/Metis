#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import time
import os
from multiprocessing import Process
from app.dao.time_series_detector import anomaly_op
from app.dao.time_series_detector import sample_op
from app.dao.time_series_detector import train_op
from app.utils.utils import *
from app.service.time_series_detector.algorithm import isolation_forest, ewma, polynomial_interpolation, statistic, xgboosting
from app.config.errorcode import *
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../model/time_series_detector/')


class DetectService(object):

    def __init__(self):
        self.sample_op_obj = sample_op.SampleOperation()
        self.anomaly_op_obj = anomaly_op.AbnormalOperation()
        self.iforest_obj = isolation_forest.IForest()
        self.ewma_obj = ewma.Ewma()
        self.polynomial_obj = polynomial_interpolation.PolynomialInterpolation()
        self.statistic_obj = statistic.Statistic()
        self.supervised_obj = xgboosting.XGBoosting()

    def __generate_model(self, data, task_id):
        """
        Start train a model

        :param data: Training dataset.
        :param task_id: The id of the training task.
        """
        xgb_obj = xgboosting.XGBoosting()
        # pylint: disable=unused-variable
        ret_code, ret_data = xgb_obj.xgb_train(data, task_id)
        current_timestamp = int(time.time())
        train_op_obj = train_op.TrainOperation()
        if ret_code == 0:
            train_status = "complete"
            params = {
                "task_id": task_id,
                "end_time": current_timestamp,
                "status": train_status,
                "model_name": task_id + "_model"
            }
        else:
            train_status = "failed"
            params = {
                "task_id": task_id,
                "end_time": current_timestamp,
                "status": train_status,
                "model_name": ""
            }
        train_op_obj.update_model_info(params)

    def process_train(self, data):
        """
        Start a process to train model
        :param data: Training dataset.
        """
        sample_params = {
            "trainOrTest": data["trainOrTest"],
            "positiveOrNegative": data["positiveOrNegative"],
            "source": data["source"],
            "beginTime": data["beginTime"],
            "endTime": data["endTime"]
        }
        samples = self.sample_op_obj.sample_query_all(sample_params)
        train_op_obj = train_op.TrainOperation()
        samples_list = []
        positive_count = 0
        negative_count = 0
        for index in samples:
            samples_list.append({"flag": index["flag"], "data": map(int, index["data"].split(','))})
            if index["flag"] == 1:
                positive_count = positive_count + 1
            else:
                negative_count = negative_count + 1
        task_id = str(int(round(time.time() * 1000)))
        train_params = {
            "begin_time": int(time.time()),
            "end_time": int(time.time()),
            "task_id": task_id,
            "status": "running",
            "source": data["source"],
            "sample_num": len(samples_list),
            "postive_sample_num": positive_count,
            "negative_sample_num": negative_count
        }
        if positive_count == 0 or negative_count == 0:
            return build_ret_data(LACK_SAMPLE, "")
        train_op_obj.insert_train_info(train_params)
        try:
            process = Process(target=self.__generate_model, args=(samples_list, task_id, ))
            process.start()
        except Exception:
            train_status = "failed"
            params = {
                "task_id": task_id,
                "end_time": int(time.time()),
                "status": train_status,
                "model_name": ""
            }
            train_op_obj.update_model_info(params)
        return build_ret_data(OP_SUCCESS, "")

    def __list_is_digit(self, data):
        for index in data:
            try:
                float(index)
            except ValueError:
                return False
        return True

    def __check_param(self, data):
        if ("viewName" not in data.keys()) or ("attrId" not in data.keys()) or ("attrName" not in data.keys()) or ("time" not in data.keys()) or ("dataC" not in data.keys()) or ("dataB" not in data.keys()) or ("dataA" not in data.keys()):
            return CHECK_PARAM_FAILED, "missing parameter"
        if not data['dataA']:
            return CHECK_PARAM_FAILED, "dataA can not be empty"
        if not data['dataB']:
            return CHECK_PARAM_FAILED, "dataB can not be empty"
        if not data['dataC']:
            return CHECK_PARAM_FAILED, "dataC can not be empty"
        if not self.__list_is_digit(data['dataA'].split(',')):
            return CHECK_PARAM_FAILED, "dataA contains illegal numbers"
        if not self.__list_is_digit(data['dataB'].split(',')):
            return CHECK_PARAM_FAILED, "dataB contains illegal numbers"
        if not self.__list_is_digit(data['dataC'].split(',')):
            return CHECK_PARAM_FAILED, "dataC contains illegal numbers"
        if "window" in data:
            window = data["window"]
        else:
            window = 180
        if len(data['dataC'].split(',')) != (2 * window + 1):
            return CHECK_PARAM_FAILED, "dataC is not long enough"
        if len(data['dataB'].split(',')) != (2 * window + 1):
            return CHECK_PARAM_FAILED, "dataB is not long enough"
        if len(data['dataA'].split(',')) != (window + 1):
            return CHECK_PARAM_FAILED, "dataA is not long enough"
        return OP_SUCCESS, ""

    def value_predict(self, data):
        """
        Predict the data

        :param data: the time series to detect of
        """
        ret_code, ret_data = self.__check_param(data)
        if ret_code != OP_SUCCESS:
            return build_ret_data(ret_code, ret_data)
        if "taskId" in data and data["taskId"]:
            model_name = MODEL_PATH + data["taskId"] + "_model"
        else:
            model_name = MODEL_PATH + "xgb_default_model"
        combined_data = data["dataC"] + "," + data["dataB"] + "," + data["dataA"]
        time_series = map(int, combined_data.split(','))
        if "window" in data:
            window = data["window"]
        else:
            window = 180
        statistic_result = self.statistic_obj.predict(time_series)
        ewma_result = self.ewma_obj.predict(time_series)
        polynomial_result = self.polynomial_obj.predict(time_series, window)
        iforest_result = self.iforest_obj.predict(time_series, window)
        if statistic_result == 0 or ewma_result == 0 or polynomial_result == 0 or iforest_result == 0:
            xgb_result = self.supervised_obj.predict(time_series, window, model_name)
            res_value = xgb_result[0]
            prob = xgb_result[1]
        else:
            res_value = 1
            prob = 1
        ret_data = {"ret": res_value, "p": str(prob)}
        if ret_data["ret"] == 0:
            anomaly_params = {
                "view_id": data["viewId"],
                "view_name": data["viewName"],
                "attr_id": data["attrId"],
                "attr_name": data["attrName"],
                "time": data["time"],
                "data_c": data["dataC"],
                "data_b": data["dataB"],
                "data_a": data["dataA"]
            }
            self.anomaly_op_obj.insert_anomaly(anomaly_params)
        return build_ret_data(OP_SUCCESS, ret_data)

    def rate_predict(self, data):
        ret_code, ret_data = check_value(data)
        if ret_code != OP_SUCCESS:
            return build_ret_data(ret_code, ret_data)
        combined_data = data["dataC"] + "," + data["dataB"] + "," + data["dataA"]
        time_series = map(float, combined_data.split(','))
        statistic_result = self.statistic_obj.predict(time_series)
        if statistic_result == 0:
            prob = 0
        else:
            prob = 1
        ret_data = {"ret": statistic_result, "p": str(prob)}
        if ret_data["ret"] == 0:
            anomaly_params = {
                "view_id": data["viewId"],
                "view_name": data["viewName"],
                "attr_id": data["attrId"],
                "attr_name": data["attrName"],
                "time": data["time"],
                "data_c": data["dataC"],
                "data_b": data["dataB"],
                "data_a": data["dataA"]
            }
            self.anomaly_op_obj.insert_anomaly(anomaly_params)
        return build_ret_data(OP_SUCCESS, ret_data)
