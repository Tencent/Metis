# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

OP_SUCCESS = 0
THROW_EXP = 1000
OP_DB_FAILED = 1001
CHECK_PARAM_FAILED = 1002
FILE_FORMAT_ERR = 1003
NOT_POST = 1004
NOT_GET = 1005
CAL_FEATURE_ERR = 2001
READ_FEATURE_FAILED = 2002
TRAIN_ERR = 2003
LACK_SAMPLE = 2004

ERR_CODE = {
    0: "操作成功",
    1000: "抛出异常",
    1001: "数据库操作失败",
    1002: "参数检查失败",
    1003: "文件格式有误",
    1004: "非post请求",
    1005: "非get请求",
    2001: "特征计算出错",
    2002: "读取特征数据失败",
    2003: "训练出错",
    2004: "缺少正样本或负样本"
}