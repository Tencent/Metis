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
import pickle
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.externals import joblib
from time_series_detector.feature import feature_service
from time_series_detector.common.tsd_common import *
from time_series_detector.common.tsd_errorcode import *


MODEL_PATH = os.path.join(os.path.dirname(__file__), '../model/')
DEFAULT_MODEL = MODEL_PATH + "gbdt_default_model"


class Gbdt(object):
    """
    Gradient boosting is a machine learning technique for regression and classification problems,
    which produces a prediction model in the form of an ensemble of weak prediction models,
    typically decision trees. It builds the model in a stage-wise fashion like other boosting methods do,
    and it generalizes them by allowing optimization of an arbitrary differentiable loss function.

    WIKIPEDIA: https://en.wikipedia.org/wiki/Gradient_boosting
    """

    def __init__(self, threshold=0.15, n_estimators=300, max_depth=10, learning_rate=0.05):
        """
        :param threshold: The critical point of normal.
        :param n_estimators: The number of boosting stages to perform. Gradient boosting is fairly robust to over-fitting so a large number usually results in better performance.
        :param max_depth: Maximum depth of the individual regression estimators. The maximum depth limits the number of nodes in the tree.
        :param learning_rate: Learning rate shrinks the contribution of each tree by `learning_rate`. There is a trade-off between learning_rate and n_estimators.
        """
        self.threshold = threshold
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate

    def __calculate_features(self, data, window=DEFAULT_WINDOW):
        """
        Caculate time features.

        :param data: the time series to detect of
        :param window: the length of window
        """
        features = []
        for index in data:
            if is_standard_time_series(index["data"], window):
                temp = []
                temp.append(feature_service.extract_features(index["data"], window))
                temp.append(index["flag"])
                features.append(temp)
        return features

    def gbdt_train(self, data, task_id, window=DEFAULT_WINDOW):
        """
        Train a gbdt model.

        :param data: Training dataset.
        :param task_id: The id of the training task.
        :param window: the length of window
        """
        X_train = []
        y_train = []
        features = self.__calculate_features(data, window)
        if features:
            return TSD_LACK_SAMPLE
        for index in features:
            X_train.append(index[0])
            y_train.append(index[1])
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        try:
            grd = GradientBoostingClassifier(n_estimators=self.n_estimators, max_depth=self.max_depth, learning_rate=self.learning_rate)
            grd.fit(X_train, y_train)
            model_name = MODEL_PATH + task_id + "_model"
            joblib.dump(grd, model_name)
        except Exception as ex:
            return TSD_TRAIN_ERR, str(ex)
        return TSD_OP_SUCCESS, ""

    def predict(self, X, window=DEFAULT_WINDOW, model_name=DEFAULT_MODEL):
        """
        Predict if a particular sample is an outlier or not.

        :param X: the time series to detect of
        :param type X: pandas.Series
        :param window: the length of window
        :param type window: int
        :param model_name: the model to use
        :param type model_name: string
        :return 1 denotes normal, 0 denotes abnormal
        """
        if is_standard_time_series(X):
            ts_features = feature_service.extract_features(X, window)
            ts_features = np.array([ts_features])
            load_model = pickle.load(open(model_name, "rb"))
            gbdt_ret = load_model.predict_proba(ts_features)[:, 1]
            if gbdt_ret[0] < self.threshold:
                value = 0
            else:
                value = 1
            return [value, gbdt_ret[0]]
        else:
            return [0, 0]
