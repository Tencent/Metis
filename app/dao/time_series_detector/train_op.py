#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making Metis available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import MySQLdb
from app.dao.db_common import database
from app.common.common import *
from app.common.errorcode import *


class TrainOperation(object):

    def __init__(self):
        self.__conn = MySQLdb.connect(host=database.HOST, port=database.PORT, user=database.USER, passwd=database.PASSWD, db=database.DB)
        self.__cur = self.__conn.cursor()
        self.__cur.execute("SET NAMES UTF8")

    def __del__(self):
        self.__conn.close()

    def query_train(self, data):
        request_page = data['requestPage']
        item_per_page = data['itemPerPage']
        begin_time = data['beginTime']
        end_time = data['endTime']
        task_id = data['taskId']
        task_status = data['taskStatus']
        beg_limit = (item_per_page * (request_page - 1))
        source = data['source']
        limit = item_per_page
        params = []
        query_str = ""

        if task_id != "":
            params.append(("%" + task_id + "%").encode('utf8'))
            params.append(("%" + task_id + "%").encode('utf8'))
            query_str += " and (task_id like %s or model_name like %s) "
        if source != "":
            params.append("%" + source + "%")
            query_str += " and (source like %s) "
        if begin_time != "" and end_time != "":
            params.append(begin_time)
            params.append(end_time)
            query_str += " and start_time > from_unixtime(%s) and end_time < from_unixtime(%s) "
        if task_status != "":
            params.append(task_status)
            query_str += " and status = %s "

        params.append(beg_limit)
        params.append(limit)
        command = 'SELECT task_id, sample_num, postive_sample_num, negative_sample_num, window, model_name, source, UNIX_TIMESTAMP(start_time), UNIX_TIMESTAMP(end_time), status FROM train_task where 1 = 1 ' + query_str + ' order by start_time desc LIMIT %s,%s;'
        command_count = 'SELECT count(*) FROM train_task where 1 = 1' + query_str
        length = self.__cur.execute(command, params)
        task_list = []
        query_res = self.__cur.fetchmany(length)
        for row in query_res:
            task_list.append({
                "id": row[0],
                "sampleNum": row[1],
                "positiveSampleNum": row[2],
                "negativeSampleNum": row[3],
                "window": row[4],
                "modelName": row[5],
                "source": row[6],
                "startTime": row[7],
                "endTime": row[8],
                "status": row[9]
            })

        self.__cur.execute(command_count, params[:-2])
        total_count = int(self.__cur.fetchone()[0])
        total_page = int(total_count) / item_per_page
        current_page = min(request_page, total_page)

        return OP_SUCCESS, {
            "taskList": task_list,
            "currentPage": current_page,
            "totalCount": total_count
        }

    def query_train_source(self):
        command = "select distinct source from train_task"
        num = self.__cur.execute(command)
        source_list = []
        query_res = self.__cur.fetchmany(num)
        for row in query_res:
            source_list.append(row[0])
        return OP_SUCCESS, {
            "source": source_list
        }

    def insert_train_info(self, data):
        command = "insert into train_task(task_id, sample_num, postive_sample_num, negative_sample_num, window, model_name, source, start_time, end_time, status) values(%s, %s, %s, %s, %s, %s, %s, from_unixtime(%s), from_unixtime(%s), %s)"

        num = self.__cur.execute(command, [data['task_id'], data['sample_num'], data['postive_sample_num'], data['negative_sample_num'], DEFAULT_WINDOW, "", ','.join(data['source']), data['begin_time'], data['end_time'], data['status']])
        self.__conn.commit()
        return num

    def delete_train(self, data):
        task_id = data['taskId']
        command = "delete from train_task where task_id = %s "
        num = self.__cur.execute(command, [task_id])
        self.__conn.commit()
        return OP_SUCCESS, num

    def update_model_info(self, data):
        command = "UPDATE train_task SET end_time = from_unixtime(%s), status = (%s), model_name = %s where task_id = %s"
        num = self.__cur.execute(command, [data['end_time'], data['status'], data['model_name'], data['task_id']])
        self.__conn.commit()
        return num

    def update_sample_info(self, data):
        command = "UPDATE train_task SET end_time = from_unixtime(%s), status = %s, sample_num = %s, postive_sample_num = %s, negative_sample_num =%s where task_id = %s"
        num = self.__cur.execute(command, [data['end_time'], data['status'], data['sample_num'], data['postive_sample_num'], data['negative_sample_num'], data['task_id']])
        self.__conn.commit()
        return num
