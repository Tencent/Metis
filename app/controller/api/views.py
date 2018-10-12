# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render
from django.http import FileResponse
from common.render import render_json
from app.service.time_series_detector.anomaly_service import *
from app.service.time_series_detector.sample_service import *
from app.service.time_series_detector.task_service import *
from app.service.time_series_detector.detect_service import *
from app.config.errorcode import *
from app.utils.utils import *


def search_anomaly(request):
    if request.method == "POST":
        try:
            anomaly_service = AnomalyService()
            return_dict = anomaly_service.query_anomaly(request.body)
        except Exception, ex:
            return_dict = build_ret_data(THROW_EXP, str(ex))
            return render_json(return_dict)
    else:
        return_dict = build_ret_data(NOT_POST)
    return render_json(return_dict)


def import_sample(request):
    if request.method == "POST":
        try:
            sample_service = SampleService()
            return_dict = sample_service.import_file(request.FILES)
        except Exception, ex:
            return_dict = build_ret_data(THROW_EXP, str(ex))
            return render_json(return_dict)
    else:
        return_dict = build_ret_data(NOT_POST)
    return render_json(return_dict)


def update_sample(request):
    if request.method == "POST":
        try:
            sample_service = SampleService()
            return_dict = sample_service.update_sample(request.body)
        except Exception, ex:
            return_dict = build_ret_data(THROW_EXP, str(ex))
            return render_json(return_dict)
    else:
        return_dict = build_ret_data(NOT_POST)
    return render_json(return_dict)


def query_sample(request):
    if request.method == "POST":
        try:
            sample_service = SampleService()
            return_dict = sample_service.query_sample(request.body)
        except Exception, ex:
            return_dict = build_ret_data(THROW_EXP, str(ex))
            return render_json(return_dict)
    else:
        return_dict = build_ret_data(NOT_POST)
    return render_json(return_dict)


def update_anomaly(request):
    if request.method == "POST":
        try:
            sample_service = AnomalyService()
            return_dict = sample_service.update_anomaly(request.body)
        except Exception, ex:
            return_dict = build_ret_data(THROW_EXP, str(ex))
            return render_json(return_dict)
    else:
        return_dict = build_ret_data(NOT_POST)
    return render_json(return_dict)


def train(request):
    if request.method == "POST":
        try:
            detect_service = DetectService()
            return_dict = detect_service.process_train(json.loads(request.body))
        except Exception, ex:
            return_dict = build_ret_data(THROW_EXP, str(ex))
            return render_json(return_dict)
    else:
        return_dict = build_ret_data(NOT_POST)
    return render_json(return_dict)


def download_sample(request):
    if request.method == "GET":
        try:
            sample_service = SampleService()
            file_name = sample_service.sample_download(request.GET['id'])
            files = open(file_name, 'rb')
            response = FileResponse(files)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename = "SampleExport.csv"'
            return response
        except Exception, ex:
            return_dict = build_ret_data(THROW_EXP, str(ex))
            return render_json(return_dict)
    else:
        return_dict = build_ret_data(NOT_GET)
    return render_json(return_dict)


def predict_rate(request):
    if request.method == "POST":
        try:
            detect_service = DetectService()
            return_dict = detect_service.rate_predict(json.loads(request.body))
        except Exception, ex:
            return_dict = build_ret_data(THROW_EXP, str(ex))
            return render_json(return_dict)
    else:
        return_dict = build_ret_data(NOT_POST)
    return render_json(return_dict)


def predict_value(request):
    if request.method == "POST":
        try:
            detect_service = DetectService()
            return_dict = detect_service.value_predict(json.loads(request.body))
        except Exception, ex:
            return_dict = build_ret_data(THROW_EXP, str(ex))
            return render_json(return_dict)
    else:
        return_dict = build_ret_data(NOT_POST)
    return render_json(return_dict)


def query_train_task(request):
    if request.method == "POST":
        try:
            train_service = TrainService()
            return_dict = train_service.query_train(request.body)
        except Exception, ex:
            return_dict = build_ret_data(THROW_EXP, str(ex))
            return render_json(return_dict)
    else:
        return_dict = build_ret_data(NOT_POST)
    return render_json(return_dict)


def query_train_source(request):
    if request.method == "POST":
        try:
            sample_service = SampleService()
            return_dict = sample_service.query_sample_source()
        except Exception, ex:
            return_dict = build_ret_data(THROW_EXP, str(ex))
            return render_json(return_dict)
    else:
        return_dict = build_ret_data(NOT_POST)
    return render_json(return_dict)


def delete_train_task(request):
    if request.method == "POST":
        try:
            train_service = TrainService()
            return_dict = train_service.delete_train(request.body)
        except Exception, ex:
            return_dict = build_ret_data(THROW_EXP, str(ex))
            return render_json(return_dict)
    else:
        return_dict = build_ret_data(NOT_POST)
    return render_json(return_dict)


def delete_sample(request):
    if request.method == "POST":
        try:
            sample_service = SampleService()
            return_dict = sample_service.delete_sample(request.body)
        except Exception, ex:
            return_dict = build_ret_data(THROW_EXP, str(ex))
            return render_json(return_dict)
    else:
        return_dict = build_ret_data(NOT_POST)
    return render_json(return_dict)


def count_sample(request):
    if request.method == "POST":
        try:
            sample_service = SampleService()
            return_dict = sample_service.count_sample(request.body)
        except Exception, ex:
            return_dict = build_ret_data(THROW_EXP, str(ex))
            return render_json(return_dict)
    else:
        return_dict = build_ret_data(NOT_POST)
    return render_json(return_dict)
