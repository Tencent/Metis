#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

TSD_OP_SUCCESS = 0
TSD_THROW_EXP = 1000
TSD_CHECK_PARAM_FAILED = 1002
TSD_FILE_FORMAT_ERR = 1003
TSD_CAL_FEATURE_ERR = 2001
TSD_READ_FEATURE_FAILED = 2002
TSD_TRAIN_ERR = 2003
TSD_LACK_SAMPLE = 2004

ERR_CODE = {
    TSD_OP_SUCCESS: "操作成功",
    TSD_THROW_EXP: "抛出异常",
    TSD_CHECK_PARAM_FAILED: "参数检查失败",
    TSD_FILE_FORMAT_ERR: "文件格式有误",
    TSD_CAL_FEATURE_ERR: "特征计算出错",
    TSD_READ_FEATURE_FAILED: "读取特征数据失败",
    TSD_TRAIN_ERR: "训练出错",
    TSD_LACK_SAMPLE: "缺少正样本或负样本"
}