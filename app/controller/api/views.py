# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from functools import wraps
from django.shortcuts import render
from django.http import FileResponse
from render import render_json
from app.service.time_series_detector.anomaly_service import *
from app.service.time_series_detector.sample_service import *
from app.service.time_series_detector.task_service import *
from app.service.time_series_detector.detect_service import *
from app.common.errorcode import *
from app.common.common import *


def check_post(func):
    @wraps(func)
    def f(request):
        if request.method == "POST":
            return_dict = func(request)
        else:
            return_dict = build_ret_data(NOT_POST)
        return render_json(return_dict)
    return f


@check_post
def search_anomaly(request):
    anomaly_service = AnomalyService()
    return anomaly_service.query_anomaly(request.body)


@check_post
def import_sample(request):
    sample_service = SampleService()
    return sample_service.import_file(request.FILES)


@check_post
def update_sample(request):
    sample_service = SampleService()
    return sample_service.update_sample(request.body)


@check_post
def query_sample(request):
    sample_service = SampleService()
    return sample_service.query_sample(request.body)


@check_post
def update_anomaly(request):
    sample_service = AnomalyService()
    return sample_service.update_anomaly(request.body)


@check_post
def train(request):
    detect_service = DetectService()
    return detect_service.process_train(json.loads(request.body))


def download_sample(request):
    if request.method == "GET":
        try:
            sample_service = SampleService()
            ret_code, file_name = sample_service.sample_download(request.GET['id'])
            files = open(file_name, 'rb')
            response = FileResponse(files)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename = "SampleExport.csv"'
            return response
        except Exception as ex:
            return_dict = build_ret_data(THROW_EXP, str(ex))
            return render_json(return_dict)
    else:
        return_dict = build_ret_data(NOT_GET)
    return render_json(return_dict)


@check_post
def predict_rate(request):
    detect_service = DetectService()
    return detect_service.rate_predict(json.loads(request.body))


@check_post
def predict_value(request):
    detect_service = DetectService()
    return detect_service.value_predict(json.loads(request.body))


@check_post
def query_train_task(request):
    train_service = TrainService()
    return train_service.query_train(request.body)


@check_post
def query_train_source(request):
    sample_service = SampleService()
    return sample_service.query_sample_source(request.body)


@check_post
def delete_train_task(request):
    train_service = TrainService()
    return train_service.delete_train(request.body)


@check_post
def delete_sample(request):
    sample_service = SampleService()
    return sample_service.delete_sample(request.body)


@check_post
def count_sample(request):
    sample_service = SampleService()
    return sample_service.count_sample(request.body)
