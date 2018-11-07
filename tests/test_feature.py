#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

from tests.fixtures import DataTestCase
from time_series_detector.feature.statistical_features import *

class FeatureTestCase(DataTestCase):

    def test_features(self):
        testdata_a = self.create_test_data_a()
        self.assertTrue(time_series_maximum(testdata_a) == 1020900)
        self.assertTrue(time_series_minimum(testdata_a) == 824757)
        self.assertTrue((time_series_mean(testdata_a) - 919324.34) < 1e-2)

    def test_two(self):
        x = "hello"
        assert 'hello' in x


if __name__ == '__main__':
    a = FeatureTestCase()
    a.test_features()
