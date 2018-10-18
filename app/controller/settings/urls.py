"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from api import views as api_views

urlpatterns = [
    url(r'^SearchAnomaly$', api_views.search_anomaly, name='search_anomaly'),
    url(r'^ImportSample$', api_views.import_sample, name='import_sample'),
    url(r'^UpdateSample$', api_views.update_sample, name='update_sample'),
    url(r'^QuerySample$', api_views.query_sample, name='query_sample'),
    url(r'^DeleteSample$', api_views.delete_sample, name='delete_sample'),
    url(r'^CountSample$', api_views.count_sample, name='count_sample'),
    url(r'^UpdateAnomaly$', api_views.update_anomaly, name='update_anomaly'),
    url(r'^DownloadSample/', api_views.download_sample, name='download_sample'),
    url(r'^QueryTrain$', api_views.query_train_task, name='query_train_task'),
    url(r'^QueryTrainSource$', api_views.query_train_source, name='query_train_source'),
    url(r'^DeleteTrain$', api_views.delete_train_task, name='delete_train_task'),
    url(r'^Train$', api_views.train, name='train'),
    url(r'^PredictRate$', api_views.predict_rate, name='predict_rate'),
    url(r'^PredictValue$', api_views.predict_value, name='predict_value'),
]
