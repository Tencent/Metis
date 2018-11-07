#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import MySQLdb
from app.dao.db_common import database
from app.dao.time_series_detector.sample_op import *
from app.common.common import *
from app.common.errorcode import *


class AbnormalOperation(object):

    def __init__(self):
        self.__conn = MySQLdb.connect(host=database.HOST, port=database.PORT, user=database.USER, passwd=database.PASSWD, db=database.DB)
        self.__cur = self.__conn.cursor()
        self.__cur.execute("SET NAMES UTF8")
        self.__sample = SampleOperation()

    def __del__(self):
        self.__conn.close()

    def get_anomaly(self, form):
        request_page = form['requestPage']
        item_per_page = form['itemPerPage']
        attr_id = form['attrId']
        view_id = form['viewId']
        beg_limit = (form['itemPerPage'] * (form['requestPage'] - 1))
        limit = form['itemPerPage']
        params = []
        query_str = ""
        params.append(form['beginTime'])
        params.append(form['endTime'])
        if attr_id != "":
            params.append(attr_id.encode('utf8'))
            params.append(("%" + attr_id + "%").encode('utf8'))
            query_str += " and (attr_id = %s or attr_name like %s) "
        if view_id != "":
            params.append(view_id.encode('utf8'))
            params.append(("%" + view_id + "%").encode('utf8'))
            query_str += "and (view_id = %s or view_name like %s) "

        params.append(beg_limit)
        params.append(limit)
        command = 'SELECT id, view_id, view_name, attr_id, attr_name, UNIX_TIMESTAMP(time), data_c, data_b, data_a, mark_flag FROM anomaly WHERE time > from_unixtime(%s) and time < from_unixtime(%s) ' + query_str + 'LIMIT %s, %s;'
        command_count = 'SELECT count(*) FROM anomaly  WHERE time > from_unixtime(%s) and time < from_unixtime(%s) ' + query_str
        length = self.__cur.execute(command, params)
        abnormal_list = []
        query_res = self.__cur.fetchmany(length)
        for row in query_res:
            abnormal_list.append({
                "id": row[0],
                "viewId": row[1],
                "viewName": row[2],
                "attrId": row[3],
                "attrName": row[4],
                "time": row[5],
                "dataC": row[6].split(','),
                "dataB": row[7].split(','),
                "dataA": row[8].split(','),
                "markFlag": row[9]
            })
        self.__cur.execute(command_count, params[:-2])
        total_count = int(self.__cur.fetchone()[0])
        total_page = int(total_count) / item_per_page
        current_page = min(request_page, total_page)

        return OP_SUCCESS, {
            "anomalyList": abnormal_list,
            "currentPage": current_page,
            "totalCount": total_count
        }

    def update_anomaly(self, data):
        update_str = "UPDATE anomaly set mark_flag = %s where id = %s"
        params = [data['markFlag'], data['id']]
        self.__cur.execute(update_str, params)
        self.__conn.commit()

        if MARK_NEGATIVE == data['markFlag'] or MARK_POSITIVE == data['markFlag']:
            select_str = 'SELECT  view_name, view_id, attr_name, attr_id, UNIX_TIMESTAMP(time), data_c, data_b, data_a, mark_flag, id FROM anomaly where id = %s'
            self.__cur.execute(select_str, [data['id']])
            row = self.__cur.fetchone()
            insert_data = []
            window = row[7].count(',')
            one_item = {
                "viewName": row[0],
                "viewId": row[1],
                "attrName": row[2],
                "attrId": row[3],
                "source": "unknown",
                "trainOrTest": "train",
                "positiveOrNegative": "positive" if MARK_POSITIVE == data['markFlag'] else "negative",
                "window": window,
                "dataC": row[5],
                "dataB": row[6],
                "dataA": row[7],
                "dataTime": row[4],
                "anomalyId": row[9],
            }
            insert_data.append(one_item)
            ret_code, ret_data = self.__sample.import_sample(insert_data)
        else:
            ret_code, ret_data = self.__sample.delete_sample_by_anomaly_id(data)
        record_num = ret_data
        return ret_code, record_num

    def insert_anomaly(self, data):
        insert_str = "INSERT INTO anomaly(view_id, view_name, attr_name, attr_id, time, data_c, data_b, data_a) values(%s, %s, %s, %s, %s, %s, %s, %s);"
        params = [data['view_id'], data['view_name'].encode('utf8'), data['attr_name'].encode('utf8'), data['attr_id'], data['time'], data['data_c'], data['data_b'], data['data_a']]
        record_num = self.__cur.execute(insert_str, params)
        self.__conn.commit()
        return OP_SUCCESS, record_num
