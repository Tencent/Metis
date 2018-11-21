#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import numpy as np
import tsfresh.feature_extraction.feature_calculators as ts_feature_calculators
from time_series_detector.common.tsd_common import DEFAULT_WINDOW, split_time_series
from statistical_features import time_series_mean, time_series_variance, time_series_standard_deviation, time_series_median


def time_series_autocorrelation(x):
    """
    Calculates the autocorrelation of the specified lag, according to the formula [1]

    .. math::

        \\frac{1}{(n-l)\sigma^{2}} \\sum_{t=1}^{n-l}(X_{t}-\\mu )(X_{t+l}-\\mu)

    where :math:`n` is the length of the time series :math:`X_i`, :math:`\sigma^2` its variance and :math:`\mu` its
    mean. `l` denotes the lag.

    .. rubric:: References

    [1] https://en.wikipedia.org/wiki/Autocorrelation#Estimation

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :param lag: the lag
    :type lag: int
    :return: the value of this feature
    :return type: float
    """
    lag = int((len(x) - 3) / 5)
    if np.sqrt(np.var(x)) < 1e-10:
        return 0
    return ts_feature_calculators.autocorrelation(x, lag)


def time_series_coefficient_of_variation(x):
    """
    Calculates the coefficient of variation, mean value / square root of variation

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    if np.sqrt(np.var(x)) < 1e-10:
        return 0
    return np.mean(x) / np.sqrt(np.var(x))


def time_series_binned_entropy(x):
    """
    First bins the values of x into max_bins equidistant bins.
    Then calculates the value of

    .. math::

        - \\sum_{k=0}^{min(max\\_bins, len(x))} p_k log(p_k) \\cdot \\mathbf{1}_{(p_k > 0)}

    where :math:`p_k` is the percentage of samples in bin :math:`k`.

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :param max_bins: the maximal number of bins
    :type max_bins: int
    :return: the value of this feature
    :return type: float
    """
    max_bins = [2, 4, 6, 8, 10, 20]
    result = []
    for value in max_bins:
        result.append(ts_feature_calculators.binned_entropy(x, value))
    return result


def time_series_value_distribution(x):
    """
    Given buckets, calculate the percentage of elements in the whole time series
    in different buckets

    :param x: normalized time series
    :type x: pandas.Series
    :return: the values of this feature
    :return type: list
    """
    thresholds = [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99, 1.0, 1.0]
    return list(np.histogram(x, bins=thresholds)[0] / float(len(x)))


def time_series_daily_parts_value_distribution(x):
    """
    Given buckets, calculate the percentage of elements in three subsequences
    of the whole time series in different buckets

    :param x: normalized time series
    :type x: pandas.Series
    :return: the values of this feature
    :return type: list
    """
    thresholds = [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99, 1.0, 1.0]
    split_value_list = split_time_series(x, DEFAULT_WINDOW)
    data_c = split_value_list[0] + split_value_list[1][1:]
    data_b = split_value_list[2] + split_value_list[3][1:]
    data_a = split_value_list[4]
    count_c = list(np.histogram(data_c, bins=thresholds)[0])
    count_b = list(np.histogram(data_b, bins=thresholds)[0])
    count_a = list(np.histogram(data_a, bins=thresholds)[0])
    return list(np.array(count_c) / float(len(data_c))) + list(np.array(count_b) / float(len(data_b))) + list(np.array(count_a) / float(len(data_a)))


def time_series_daily_parts_value_distribution_with_threshold(x):
    """
    Split the whole time series into three parts: c, b, a.
    Given a threshold = 0.01, return the percentage of elements of time series
    which are less than threshold

    :param x: normalized time series
    :type x: pandas.Series
    :return: 6 values of this feature
    :return type: list
    """
    threshold = 0.01
    split_value_list = split_time_series(x, DEFAULT_WINDOW)
    data_c = split_value_list[0] + split_value_list[1][1:]
    data_b = split_value_list[2] + split_value_list[3][1:]
    data_a = split_value_list[4]

    # the number of elements in time series which is less than threshold:
    nparray_data_c_threshold = np.array(data_c)
    nparray_data_c_threshold[nparray_data_c_threshold < threshold] = -1
    nparray_data_b_threshold = np.array(data_b)
    nparray_data_b_threshold[nparray_data_b_threshold < threshold] = -1
    nparray_data_a_threshold = np.array(data_a)
    nparray_data_a_threshold[nparray_data_a_threshold < threshold] = -1

    # the total number of elements in time series which is less than threshold:
    nparray_threshold_count = (nparray_data_c_threshold == -1).sum() + (nparray_data_b_threshold == -1).sum() + (nparray_data_a_threshold == -1).sum()

    if nparray_threshold_count == 0:
        features = [0, 0, 0]
    else:
        features = [
            (nparray_data_c_threshold == -1).sum() / float(nparray_threshold_count),
            (nparray_data_b_threshold == -1).sum() / float(nparray_threshold_count),
            (nparray_data_a_threshold == -1).sum() / float(nparray_threshold_count)
        ]

    features.extend([
                    (nparray_data_c_threshold == -1).sum() / float(len(data_c)),
                    (nparray_data_b_threshold == -1).sum() / float(len(data_b)),
                    (nparray_data_a_threshold == -1).sum() / float(len(data_a))
                    ])
    return features


def time_series_window_parts_value_distribution_with_threshold(x):
    """
    Split the whole time series into five parts.
    Given a threshold = 0.01, return the percentage of elements of time series
    which are less than threshold

    :param x: normalized time series
    :type x: pandas.Series
    :return: 5 values of this feature
    :return type: list
    """
    threshold = 0.01
    split_value_list = split_time_series(x, DEFAULT_WINDOW)

    count_list = []
    for value_list in split_value_list:
        nparray_threshold = np.array(value_list)
        nparray_threshold[nparray_threshold < threshold] = -1
        count_list.append((nparray_threshold == -1).sum())

    if sum(count_list) == 0:
        features = [0, 0, 0, 0, 0]
    else:
        features = list(np.array(count_list) / float((DEFAULT_WINDOW + 1)))

    return features


# add yourself classification features here...


def get_classification_features(x):
    classification_features = [
        time_series_mean(x),
        time_series_variance(x),
        time_series_standard_deviation(x),
        time_series_median(x),
        time_series_autocorrelation(x),
        time_series_coefficient_of_variation(x)
    ]
    classification_features.extend(time_series_value_distribution(x))
    classification_features.extend(time_series_daily_parts_value_distribution(x))
    classification_features.extend(time_series_daily_parts_value_distribution_with_threshold(x))
    classification_features.extend(time_series_window_parts_value_distribution_with_threshold(x))
    classification_features.extend(time_series_binned_entropy(x))
    # add yourself classification features here...

    return classification_features
