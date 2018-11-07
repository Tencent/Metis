#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import json
from app.dao.time_series_detector.anomaly_op import *


class AnomalyService(object):

    def __init__(self):
        self.__anomaly = AbnormalOperation()

    @exce_service
    def query_anomaly(self, body):
        return self.__anomaly.get_anomaly(json.loads(body))

    @exce_service
    def update_anomaly(self, body):
        return self.__anomaly.update_anomaly(json.loads(body))
