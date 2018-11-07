#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

from sklearn.ensemble import IsolationForest
from time_series_detector.common.tsd_common import *


class IForest(object):
    """
    The IsolationForest 'isolates' observations by randomly selecting a feature and then
    randomly selecting a split value between the maximum and minimum values of the selected feature.

    https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf
    """

    def __init__(self,
                 n_estimators=3,
                 max_samples="auto",
                 contamination=0.15,
                 max_feature=1.,
                 bootstrap=False,
                 n_jobs=1,
                 random_state=None,
                 verbose=0):
        """
        :param n_estimators: The number of base estimators in the ensemble.
        :param max_samples: The number of samples to draw from X to train each base estimator.
        :param coefficient: The amount of contamination of the data set, i.e. the proportion of outliers in the data set. Used when fitting to define the threshold on the decision function.
        :param max_features: The number of features to draw from X to train each base estimator.
        :param bootstrap: If True, individual trees are fit on random subsets of the training data sampled with replacement. If False, sampling without replacement is performed.
        :param random_state: If int, random_state is the seed used by the random number generator;
                              If RandomState instance, random_state is the random number generator;
                              If None, the random number generator is the RandomState instance used  by `np.random`.
        :param verbose: Controls the verbosity of the tree building process.
        """
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.contamination = contamination
        self.max_feature = max_feature
        self.bootstrap = bootstrap
        self.n_jobs = n_jobs
        self.random_state = random_state
        self.verbose = verbose

    def predict(self, X, window=DEFAULT_WINDOW):
        """
        Predict if a particular sample is an outlier or not.

        :param X: the time series to detect of
        :param type X: pandas.Series
        :param window: the length of window
        :param type window: int
        :return: 1 denotes normal, 0 denotes abnormal.
        """
        x_train = list(range(0, 2 * window + 1)) + list(range(0, 2 * window + 1)) + list(range(0, window + 1))
        sample_features = zip(x_train, X)
        clf = IsolationForest(self.n_estimators, self.max_samples, self.contamination, self.max_feature, self.bootstrap, self.n_jobs, self.random_state, self.verbose)
        clf.fit(sample_features)
        predict_res = clf.predict(sample_features)
        if predict_res[-1] == -1:
            return 0
        return 1
