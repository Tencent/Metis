#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

from time_series_detector.algorithm import ewma
from time_series_detector.algorithm import polynomial_interpolation
from time_series_detector.common.tsd_common import *


class EwmaAndPolynomialInterpolation(object):

    def __init__(self, alpha=0.3, coefficient=3, threshold=0.15, degree=4):
        """
        :param alpha: Discount rate of ewma, usually in (0.2, 0.3).
        :param coefficient: Coefficient is the width of the control limits, usually in (2.7, 3.0).
        :param threshold: The critical point of normal.
        :param degree: Depth of iteration.
        """
        self.alpha = alpha
        self.coefficient = coefficient
        self.degree = degree
        self.threshold = threshold

    def predict(self, X, window=DEFAULT_WINDOW):
        """
        Predict if a particular sample is an outlier or not.

        :param X: the time series to detect of
        :param type X: pandas.Series
        :param: window: the length of window
        :param type window: int
        :return: 1 denotes normal, 0 denotes abnormal
        """
        ewma_obj = ewma.Ewma(self.alpha, self.coefficient)
        ewma_ret = ewma_obj.predict(X)
        if ewma_ret == 1:
            result = 1
        else:
            polynomial_obj = polynomial_interpolation.PolynomialInterpolation(self.threshold, self.degree)
            polynomial_ret = polynomial_obj.predict(X, window)
            result = polynomial_ret
        return result
