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
import xgboost as xgb
from time_series_detector.feature import feature_service
from time_series_detector.common.tsd_errorcode import *
from time_series_detector.common.tsd_common import *
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../model/')
DEFAULT_MODEL = MODEL_PATH + "xgb_default_model"


class XGBoosting(object):
    """
    XGBoost is an optimized distributed gradient boosting library designed to be highly efficient,
    flexible and portable. It implements machine learning algorithms under the Gradient Boosting framework.
    XGBoost provides a parallel tree boosting (also known as GBDT, GBM) that solve many data science problems
    in a fast and accurate way. The same code runs on major distributed environment (Hadoop, SGE, MPI)
    and can solve problems beyond billions of examples.

    https://github.com/dmlc/xgboost
    """

    def __init__(self,
                 threshold=0.15,
                 max_depth=10,
                 eta=0.05,
                 gamma=0.1,
                 silent=1,
                 min_child_weight=1,
                 subsample=0.8,
                 colsample_bytree=1,
                 booster='gbtree',
                 objective='binary:logistic',
                 eval_metric='auc'):
        """
        :param threshold: The critical point of normal.
        :param max_depth: Maximum tree depth for base learners.
        :param eta: Value means model more robust to overfitting but slower to compute.
        :param gamma: Minimum loss reduction required to make a further partition on a leaf node of the tree.
        :param silent: If 1, it will print information about performance. If 2, some additional information will be printed out.
        :param min_child_weight: Minimum sum of instance weight(hessian) needed in a child.
        :param subsample: Subsample ratio of the training instance.
        :param colsample_bytree: Subsample ratio of columns when constructing each tree.
        :param booster: Specify which booster to use: gbtree, gblinear or dart.
        :param objective: Specify the learning task and the corresponding learning objective or a custom objective function to be used (see note below).
        :param eval_metric: If a str, should be a built-in evaluation metric to use. See doc/parameter.md. If callable, a custom evaluation metric.
        """
        self.threshold = threshold
        self.max_depth = max_depth
        self.eta = eta
        self.gamma = gamma
        self.silent = silent
        self.min_child_weight = min_child_weight
        self.subsample = subsample
        self.colsample_bytree = colsample_bytree
        self.booster = booster
        self.objective = objective
        self.eval_metric = eval_metric

    def __save_libsvm_format(self, data, feature_file_name):
        """
        Save the time features to libsvm format.

        :param data: feature values
        :param file_name: file saves the time features and label
        """
        try:
            f = open(feature_file_name, "w")
        except Exception as ex:
            return TSD_CAL_FEATURE_ERR, str(ex)
        times = 0
        for temp in data:
            if times > 0:
                f.write("\n")
            result = ['{0}:{1}'.format(int(index) + 1, value) for index, value in enumerate(temp[0])]
            f.write(str(temp[1]))
            for x in result:
                f.write(' ' + x)
            times = times + 1
        return TSD_OP_SUCCESS, ""

    def __calculate_features(self, data, feature_file_name, window=DEFAULT_WINDOW):
        """
        Caculate time features and save as libsvm format.

        :param data: the time series to detect of
        :param feature_file_name: the file to use
        :param window: the length of window
        """
        features = []
        for index in data:
            if is_standard_time_series(index["data"], window):
                temp = []
                temp.append(feature_service.extract_features(index["data"], window))
                temp.append(index["flag"])
                features.append(temp)
        try:
            ret_code, ret_data = self.__save_libsvm_format(features, feature_file_name)
        except Exception as ex:
            ret_code = TSD_CAL_FEATURE_ERR
            ret_data = str(ex)
        return ret_code, ret_data

    def xgb_train(self, data, task_id, num_round=300):
        """
        Train an xgboost model.

        :param data: Training dataset.
        :param task_id: The id of the training task.
        :param num_round: Max number of boosting iterations.
        """
        model_name = MODEL_PATH + task_id + "_model"
        feature_file_name = MODEL_PATH + task_id + "_features"
        ret_code, ret_data = self.__calculate_features(data, feature_file_name)
        if ret_code != TSD_OP_SUCCESS:
            return ret_code, ret_data
        try:
            dtrain = xgb.DMatrix(feature_file_name)
        except Exception as ex:
            return TSD_READ_FEATURE_FAILED, str(ex)
        params = {
            'max_depth': self.max_depth,
            'eta': self.eta,
            'gamma': self.gamma,
            'silent': self.silent,
            'min_child_weight': self.min_child_weight,
            'subsample': self.subsample,
            'colsample_bytree': self.colsample_bytree,
            'booster': self.booster,
            'objective': self.objective,
            'eval_metric': self.eval_metric,
        }
        try:
            bst = xgb.train(params, dtrain, num_round)
            bst.save_model(model_name)
        except Exception as ex:
            return TSD_TRAIN_ERR, str(ex)
        return TSD_OP_SUCCESS, ""

    def predict(self, X, window=DEFAULT_WINDOW, model_name=DEFAULT_MODEL):
        """
        :param X: the time series to detect of
        :type X: pandas.Series
        :param window: the length of window
        :param model_name: Use a xgboost model to predict a particular sample is an outlier or not.
        :return 1 denotes normal, 0 denotes abnormal.
        """
        if is_standard_time_series(X, window):
            ts_features = []
            features = [10]
            features.extend(feature_service.extract_features(X, window))
            ts_features.append(features)
            res_pred = xgb.DMatrix(np.array(ts_features))
            bst = xgb.Booster({'nthread': 4})
            bst.load_model(model_name)
            xgb_ret = bst.predict(res_pred)
            if xgb_ret[0] < self.threshold:
                value = 0
            else:
                value = 1
            return [value, xgb_ret[0]]
        else:
            return [0, 0]
