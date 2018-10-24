#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

from unittest import TestCase
import random


class DataTestCase(TestCase):
    def create_test_data_a(self):
        return [850600,889768,883237,896313,870407,868385,865300,889802,894983,836835,937571,904475,892846,878769,886624,892638,894804,889133,908860,
                904439,896944,910079,932156,927790,936513,944358,922693,905639,929855,824757,1020900,918838,966000,936090,921495,988048,963848,959618,
                948817,963953,955761,964989,980420,927674,962113,956436,967907,975038,946675,875024]

    def generate_random_str(self, randomlength=16):
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        for i in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str
