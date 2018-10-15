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
from app.service.time_series_detector.feature.statistical_features import *
from app.config.common import *
from app.utils.utils import *

class CommonTestCase(DataTestCase):

    def test_check_value(self):
        str_param = self.generate_random_str(INPUT_LEN_ENG_MAX+1)
        self.assertTrue(validate_value(str_param) != 0 )
        list_param = []
        for i in range(0,INPUT_LIST_LEN_MAX):
            list_param.append(self.generate_random_str(INPUT_LEN_ENG_MAX))
        self.assertTrue(validate_value(list_param) == 0 )
        list_param.append(self.generate_random_str(INPUT_LEN_ENG_MAX))
        self.assertFalse(validate_value(list_param) == 0 )
