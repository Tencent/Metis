#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import datetime
import uuid
import csv
import codecs
import MySQLdb
from app.dao.db_common import database
from app.common.common import *
from app.common.errorcode import *


class SampleOperation(object):

    def __init__(self):
        self.__conn = MySQLdb.connect(host=database.HOST, port=database.PORT, user=database.USER, passwd=database.PASSWD, db=database.DB)
        self.__cur = self.__conn.cursor()
        self.__cur.execute("SET NAMES UTF8")

    def __del__(self):
        self.__conn.close()

    def import_sample(self, data):
        params = []
        insert_str = "INSERT INTO sample_dataset(view_id, view_name, attr_name, attr_id, source, train_or_test, positive_or_negative, window, data_time, data_c, data_b, data_a, anomaly_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        for row in data:
            params.append([row['viewId'], row['viewName'], row['attrName'], row['attrId'], row['source'], row['trainOrTest'], row['positiveOrNegative'], row['window'], row['dataTime'], row['dataC'], row['dataB'], row['dataA'], row['anomalyId']])
        num = self.__cur.executemany(insert_str, params)
        self.__conn.commit()
        return OP_SUCCESS, num

    def update_sample(self, data):
        params = []
        update_str = ""
        update_data = data['data']
        if update_data['updateTime'] != "":
            update_time_str = datetime.datetime.fromtimestamp(update_data['updateTime']).strftime("%Y-%m-%d %H:%M:%S")
            params.append(update_time_str)
            update_str += "update_time = %s, "
        if update_data['viewId'] != "":
            params.append(update_data['viewId'])
            update_str += "view_id = %s, "
        if update_data['viewName'] != "":
            params.append(update_data['viewName'].encode('utf8'))
            update_str += "view_name = %s, "
        if update_data['attrName'] != "":
            params.append(update_data['attrName'].encode('utf8'))
            update_str += "attr_name = %s, "
        if update_data['attrId'] != "":
            params.append(update_data['attrId'])
            update_str += "attr_id = %s, "
        if update_data['source'] != "":
            params.append(update_data['source'])
            update_str += "source = %s, "
        if update_data['trainOrTest'] != "":
            params.append(update_data['trainOrTest'])
            update_str += "train_or_test = %s, "
        if update_data['positiveOrNegative'] != "":
            params.append(update_data['positiveOrNegative'])
            update_str += "positive_or_negative = %s, "
        if update_data['window'] != "":
            params.append(update_data['window'])
            update_str += "window = %s, "
        if update_data['dataTime'] != "":
            params.append(update_data['dataTime'])
            update_str += "data_time = %s, "

        if update_str == "":
            return CHECK_PARAM_FAILED, ""

        command = "UPDATE sample_dataset set " + update_str[:-2] + " where id = %s "
        all_params = []

        for id_num in data['idList']:
            all_params.append(tuple(params + [id_num]))
        num = self.__cur.executemany(command, all_params)
        self.__conn.commit()
        return OP_SUCCESS, num

    def sample_query_all(self, data):
        params = []
        query_str = ""
        params.append(DEFAULT_WINDOW)
        params.append(data['beginTime'])
        params.append(data['endTime'])

        if data['trainOrTest'] != "":
            train_str = ""
            for one_source in data['trainOrTest']:
                params.append(one_source)
                train_str += 'train_or_test = %s or '
            query_str += ' and (' + train_str[:-4] + ') '
        if data['positiveOrNegative'] != "":
            params.append(data['positiveOrNegative'])
            query_str += " and positive_or_negative = %s "
        if data['source'] != "":
            source_str = ""
            for one_source in data['source']:
                params.append(one_source)
                source_str += 'source = %s or '
            query_str += ' and (' + source_str[:-4] + ') '

        command = 'SELECT data_c, data_b, data_a, positive_or_negative FROM sample_dataset WHERE window = %s and data_time > %s and data_time < %s ' + query_str
        length = self.__cur.execute(command, params)
        sample_list = []
        query_res = self.__cur.fetchmany(length)
        for row in query_res:
            sample_list.append({
                "data": row[0] + ',' + row[1] + ',' + row[2],
                "flag": 1 if row[3] == 'positive' else 0
            })
        return sample_list

    def sample_count(self, data):
        params = []
        query_str = ""
        params.append(DEFAULT_WINDOW)
        params.append(data['beginTime'])
        params.append(data['endTime'])

        if data['trainOrTest'] != "":
            train_str = ""
            for one_source in data['trainOrTest']:
                params.append(one_source)
                train_str += "train_or_test = %s or "
            query_str += " and (" + train_str[:-4] + ") "
        if data['positiveOrNegative'] != "":
            params.append(data['positiveOrNegative'])
            query_str += " and positive_or_negative = %s "
        if data['source'] != "":
            source_str = ""
            for one_source in data['source']:
                params.append(one_source)
                source_str += 'source = %s or '
            query_str += " and (" + source_str[:-4] + ") "

        command = 'SELECT count(*), count(if(positive_or_negative = "positive", 1, NULL)), count(if(positive_or_negative = "negative", 1, NULL))  FROM sample_dataset WHERE  window = %s and data_time > %s and data_time < %s ' + query_str
        length = self.__cur.execute(command, params)

        sample_list = []
        query_res = self.__cur.fetchmany(length)
        for row in query_res:
            sample_list.append({
                "total_count": int(row[0]),
                "positive_count": int(row[1]),
                "negative_count": int(row[2])
            })

        return OP_SUCCESS, {"count": sample_list}

    def download_sample(self, data):
        sample_list = []
        id_list = data.split(',')
        format_strings = ','.join(['%s'] * len(id_list))
        command = 'SELECT view_name, view_id, attr_name, attr_id, source, train_or_test, positive_or_negative, window, data_c, data_b, data_a, data_time FROM sample_dataset WHERE id in (%s) ' % format_strings
        length = self.__cur.execute(command, id_list)
        query_res = self.__cur.fetchmany(length)
        for row in query_res:
            sample_list.append([
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
                row[9],
                row[10],
                row[11]
            ])
        head = ['指标集名称', '指标集id', '指标名称', '指标id', '样本来源', '训练集_测试集', '正样本_负样本', '样本窗口', 'dataC', 'dataB', 'dataA', '数据时间戳']
        uuid_str = uuid.uuid4().hex[:8]
        download_file_path = UPLOAD_FILE % uuid_str
        with open(download_file_path, 'w') as pfile:
            pfile.write(codecs.BOM_UTF8)
            writer = csv.writer(pfile)
            writer.writerow(head)
            writer.writerows(sample_list)
        return 0, download_file_path

    def query_sample(self, data):
        item_per_page = data['itemPerPage']
        request_page = data['requestPage']
        beg_limit = (item_per_page * (request_page - 1))
        limit = item_per_page
        params = []
        query_str = ""

        if data['beginTime'] != "" and data['endTime'] != "":
            params.append(data['beginTime'])
            params.append(data['endTime'])
            query_str += " and data_time > %s and data_time < %s "
        if data['attrId'] != "":
            params.append(data['attrId'].encode('utf8'))
            params.append(("%" + data['attrId'] + "%").encode('utf8'))
            query_str += " and (attr_id = %s or attr_name like %s)  "
        if data['viewId'] != "":
            params.append(data['viewId'].encode('utf8'))
            params.append(("%" + data['viewId'] + "%").encode('utf8'))
            query_str += " and (view_id = %s or view_name like %s) "
        if data['positiveOrNegative'] != "":
            params.append(data['positiveOrNegative'])
            query_str += " and positive_or_negative = %s "
        if data['source'] != "":
            params.append(data['source'])
            query_str += " and source = %s "
        if data['trainOrTest'] != "":
            params.append(data['trainOrTest'])
            query_str += " and train_or_test = %s "
        if data['window'] != "":
            params.append(data['window'])
            query_str += " and window = %s "
        if query_str != "":
            query_str = " WHERE " + query_str[5:]

        params.append(beg_limit)
        params.append(limit)
        command = 'SELECT id, view_id, view_name, attr_id, attr_name, data_time, data_c, data_b, data_a, positive_or_negative, source, train_or_test, window FROM sample_dataset  ' + query_str + ' LIMIT %s, %s;'
        command_count = 'SELECT count(*) FROM sample_dataset  ' + query_str
        length = self.__cur.execute(command, params)

        sample_list = []
        query_res = self.__cur.fetchmany(length)
        for row in query_res:
            sample_list.append({
                "id": row[0],
                "viewId": row[1],
                "viewName": row[2],
                "attrId": row[3],
                "attrName": row[4],
                "time": row[5],
                "dataC": row[6],
                "dataB": row[7],
                "dataA": row[8],
                "positiveOrNegative": row[9],
                "source": row[10],
                "trainOrTest": row[11],
                "window": row[12]
            })
        self.__cur.execute(command_count, params[:-2])
        total_count = int(self.__cur.fetchone()[0])
        total_page = total_count / item_per_page
        current_page = min(request_page, total_page)
        return 0, {
            "sampleList": sample_list,
            "currentPage": current_page,
            "totalTotal": total_count
        }

    def delete_sample(self, data):
        id_num = data['id']
        command = "delete from sample_dataset where id = %s "
        num = self.__cur.execute(command, id_num)
        self.__conn.commit()
        return OP_SUCCESS, {"count": num}

    def delete_sample_by_anomaly_id(self, data):
        id_num = data['id']
        command = "delete from sample_dataset where anomaly_id = %s "
        num = self.__cur.execute(command, [id_num])
        self.__conn.commit()
        return OP_SUCCESS, num

    def query_sample_source(self):
        command = "select distinct source from sample_dataset"
        num = self.__cur.execute(command)
        source_list = []
        query_res = self.__cur.fetchmany(num)
        for row in query_res:
            source_list.append(row[0])
        return OP_SUCCESS, {
            "source": source_list
        }
