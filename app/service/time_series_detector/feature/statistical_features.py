#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import tsfresh.feature_extraction.feature_calculators as ts_feature_calculators


def time_series_maximum(x):
    """
    Calculates the highest value of the time series x.

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.maximum(x)


def time_series_minimum(x):
    """
    Calculates the lowest value of the time series x.

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.minimum(x)


def time_series_mean(x):
    """
    Returns the mean of x

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.mean(x)


def time_series_variance(x):
    """
    Returns the variance of x

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.variance(x)


def time_series_standard_deviation(x):
    """
    Returns the standard deviation of x

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.standard_deviation(x)


def time_series_skewness(x):
    """
    Returns the sample skewness of x (calculated with the adjusted Fisher-Pearson standardized
    moment coefficient G1).

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.skewness(x)


def time_series_kurtosis(x):
    """
    Returns the kurtosis of x (calculated with the adjusted Fisher-Pearson standardized
    moment coefficient G2).

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.kurtosis(x)


def time_series_median(x):
    """
    Returns the median of x

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.median(x)


def time_series_abs_energy(x):
    """
    Returns the absolute energy of the time series which is the sum over the squared values

    .. math::

        E = \\sum_{i=1,\ldots, n} x_i^2

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.abs_energy(x)


def time_series_absolute_sum_of_changes(x):
    """
    Returns the sum over the absolute value of consecutive changes in the series x

    .. math::

        \\sum_{i=1, \ldots, n-1} \\mid x_{i+1}- x_i \\mid

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.absolute_sum_of_changes(x)


def time_series_variance_larger_than_std(x):
    """
    Boolean variable denoting if the variance of x is greater than its standard deviation. Is equal to variance of x
    being larger than 1

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: int
    """
    return int(ts_feature_calculators.variance_larger_than_standard_deviation(x))


def time_series_count_above_mean(x):
    """
    Returns the number of values in x that are higher than the mean of x

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.count_above_mean(x)


def time_series_count_below_mean(x):
    """
    Returns the number of values in x that are lower than the mean of x

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.count_below_mean(x)


def time_series_first_location_of_maximum(x):
    """
    Returns the first location of the maximum value of x.
    The position is calculated relatively to the length of x.

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.first_location_of_maximum(x)


def time_series_first_location_of_minimum(x):
    """
    Returns the first location of the minimal value of x.
    The position is calculated relatively to the length of x.

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.first_location_of_minimum(x)


def time_series_last_location_of_maximum(x):
    """
    Returns the relative last location of the maximum value of x.
    The position is calculated relatively to the length of x.

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.last_location_of_maximum(x)


def time_series_last_location_of_minimum(x):
    """
    Returns the last location of the minimal value of x.
    The position is calculated relatively to the length of x.

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.last_location_of_minimum(x)


def time_series_has_duplicate(x):
    """
    Checks if any value in x occurs more than once

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: bool
    """
    return ts_feature_calculators.has_duplicate(x)


def time_series_has_duplicate_max(x):
    """
    Checks if the maximum value of x is observed more than once

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: bool
    """
    return ts_feature_calculators.has_duplicate_max(x)


def time_series_has_duplicate_min(x):
    """
    Checks if the minimal value of x is observed more than once

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: bool
    """
    return ts_feature_calculators.has_duplicate_min(x)


def time_series_longest_strike_above_mean(x):
    """
    Returns the length of the longest consecutive subsequence in x that is bigger than the mean of x

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.longest_strike_above_mean(x)


def time_series_longest_strike_below_mean(x):
    """
    Returns the length of the longest consecutive subsequence in x that is smaller than the mean of x

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.longest_strike_below_mean(x)


def time_series_mean_abs_change(x):
    """
    Returns the mean over the absolute differences between subsequent time series values which is

    .. math::

        \\frac{1}{n} \\sum_{i=1,\ldots, n-1} | x_{i+1} - x_{i}|


    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.mean_abs_change(x)


def time_series_mean_change(x):
    """
    Returns the mean over the absolute differences between subsequent time series values which is

    .. math::

        \\frac{1}{n} \\sum_{i=1,\ldots, n-1}  x_{i+1} - x_{i}

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.mean_change(x)


def time_series_percentage_of_reoccurring_datapoints_to_all_datapoints(x):
    """
    Returns the percentage of unique values, that are present in the time series
    more than once.

        len(different values occurring more than once) / len(different values)

    This means the percentage is normalized to the number of unique values,
    in contrast to the percentage_of_reoccurring_values_to_all_values.

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.percentage_of_reoccurring_datapoints_to_all_datapoints(x)


def time_series_ratio_value_number_to_time_series_length(x):
    """
    Returns a factor which is 1 if all values in the time series occur only once,
    and below one if this is not the case.
    In principle, it just returns

        # unique values / # values

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.ratio_value_number_to_time_series_length(x)


def time_series_sum_of_reoccurring_data_points(x):
    """
    Returns the sum of all data points, that are present in the time series
    more than once.

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.sum_of_reoccurring_data_points(x)


def time_series_sum_of_reoccurring_values(x):
    """
    Returns the sum of all values, that are present in the time series
    more than once.

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return ts_feature_calculators.sum_of_reoccurring_values(x)


def time_series_sum_values(x):
    """
    Calculates the sum over the time series values

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: bool
    """
    return ts_feature_calculators.sum_values(x)


def time_series_range(x):
    """
    Calculates the range value of the time series x.

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    return time_series_maximum(x) - time_series_minimum(x)

# add yourself statistical features here...


def get_statistical_features(x):
    statistical_features = [
        time_series_maximum(x),
        time_series_minimum(x),
        time_series_mean(x),
        time_series_variance(x),
        time_series_standard_deviation(x),
        time_series_skewness(x),
        time_series_kurtosis(x),
        time_series_median(x),
        time_series_abs_energy(x),
        time_series_absolute_sum_of_changes(x),
        time_series_variance_larger_than_std(x),
        time_series_count_above_mean(x),
        time_series_count_below_mean(x),
        time_series_first_location_of_maximum(x),
        time_series_first_location_of_minimum(x),
        time_series_last_location_of_maximum(x),
        time_series_last_location_of_minimum(x),
        int(time_series_has_duplicate(x)),
        int(time_series_has_duplicate_max(x)),
        int(time_series_has_duplicate_min(x)),
        time_series_longest_strike_above_mean(x),
        time_series_longest_strike_below_mean(x),
        time_series_mean_abs_change(x),
        time_series_mean_change(x),
        time_series_percentage_of_reoccurring_datapoints_to_all_datapoints(x),
        time_series_ratio_value_number_to_time_series_length(x),
        time_series_sum_of_reoccurring_data_points(x),
        time_series_sum_of_reoccurring_values(x),
        time_series_sum_values(x),
        time_series_range(x)
    ]
    # append yourself statistical features here...

    return statistical_features
