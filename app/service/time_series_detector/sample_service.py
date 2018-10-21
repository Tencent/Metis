#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import json
import traceback
import csv
from app.dao.time_series_detector.sample_op import *
from app.config.errorcode import *
from app.utils.utils import *
from app.config.common import *


class SampleService(object):

    def __init__(self):
        self.__sample = SampleOperation()
        uuid_str = uuid.uuid4().hex[:8]
        self.__upload_file_path = UPLOAD_PATH % uuid_str

    def import_sample(self, data):
        try:
            ret_code, ret_data = self.__sample.import_sample(data)
            return_dict = build_ret_data(ret_code, {"count": ret_data})
        except Exception as ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict

    def import_file(self, file_data):
        try:
            pfile = file_data['sample_file']
            with open(self.__upload_file_path, 'wb+') as destination:
                for chunk in pfile.chunks():
                    destination.write(chunk.replace('\x00', ''))
            data = []
            csv_reader = csv.reader(open(self.__upload_file_path))
            next(csv_reader)
            count = 0
            positive_count = 0
            negative_count = 0
            for row in csv_reader:
                one_item = {"viewName": row[0],
                            "viewId": row[1],
                            "attrName": row[2],
                            "attrId": row[3],
                            "source": row[4],
                            "trainOrTest": row[5],
                            "positiveOrNegative": row[6],
                            "window": row[7],
                            "dataC": row[8],
                            "dataB": row[9],
                            "dataA": row[10],
                            "dataTime": int(row[11]),
                            "updateTime": int(row[11]),
                            "time": int(row[11]),
                            "anomalyId": "0"}
                check_code, check_msg = check_value(one_item)
                if OP_SUCCESS != check_code:
                    return build_ret_data(check_code, check_msg)
                data.append(one_item)
                if row[6] == "positive":
                    positive_count = positive_count + 1
                elif row[6] == "negative":
                    negative_count = negative_count + 1
                count = count + 1
        except Exception as ex:
            traceback.print_exc()
            return_dict = build_ret_data(FILE_FORMAT_ERR, str(ex))
            return return_dict

        import_ret = self.import_sample(data)
        if OP_SUCCESS == import_ret['code']:
            ret_data = {"positiveCount": positive_count, "negativeCount": negative_count, "totalCount": count}
            import_ret["data"] = ret_data
        return import_ret

    def update_sample(self, body):
        try:
            form = json.loads(body)
            ret_code, ret_data = check_value(form)
            if OP_SUCCESS == ret_code:
                ret_code, ret_data = self.__sample.update_sample(form)
            return_dict = build_ret_data(ret_code, {"count": ret_data})
        except Exception as ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict

    def query_sample(self, body):
        try:
            form = json.loads(body)
            ret_code, ret_data = check_value(form)
            if OP_SUCCESS == ret_code:
                ret_code, ret_data = self.__sample.query_sample(form)
            return_dict = build_ret_data(ret_code, ret_data)
        except Exception as ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict

    def sample_download(self, body):
        ret_data = ""
        try:
            if len(body) > VALUE_LEN_MAX:
                return ""
            ret_data = self.__sample.download_sample(body)
        except Exception as ex:
            traceback.print_exc()
            ret_data = build_ret_data(THROW_EXP, str(ex))
        return ret_data

    def delete_sample(self, body):
        try:
            form = json.loads(body)
            ret_code, ret_data = check_value(form)
            if OP_SUCCESS == ret_code:
                ret_code, ret_data = self.__sample.delete_sample(form)
            return_dict = build_ret_data(ret_code, {"count": ret_data})
        except Exception as ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict

    def count_sample(self, body):
        form = json.loads(body)
        try:
            ret_code, ret_data = check_value(form)
            if OP_SUCCESS == ret_code:
                ret_code, ret_data = self.__sample.sample_count(form)
            return_dict = build_ret_data(ret_code, {"count": ret_data})
        except Exception as ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict

    def query_sample_source(self):
        try:
            ret_code, ret_data = self.__sample.query_sample_source()
            return_dict = build_ret_data(ret_code, ret_data)
        except Exception as ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict
