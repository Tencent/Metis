#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import statistical_features
import classification_features
import fitting_features
from app.utils import utils


def extract_features(time_series, window):
    """
    Extracts three types of features from the time series.

    :param time_series: the time series to extract the feature of
    :type time_series: pandas.Series
    :param window: the length of window
    :type window: int
    :return: the value of features
    :return type: list with float
    """
    if not utils.is_standard_time_series(time_series, window):
        # add your report of this error here...

        return []

    # spilt time_series
    split_time_series = utils.split_time_series(time_series, window)
    # nomalize time_series
    normalized_split_time_series = utils.normalize_time_series(split_time_series)
    s_features = statistical_features.get_statistical_features(normalized_split_time_series[4])
    f_features = fitting_features.get_fitting_features(normalized_split_time_series)
    c_features = classification_features.get_classification_features(normalized_split_time_series[0] + normalized_split_time_series[1][1:] + normalized_split_time_series[2] + normalized_split_time_series[3][1:] + normalized_split_time_series[4])
    # combine features with types
    features = s_features + f_features + c_features
    return features
