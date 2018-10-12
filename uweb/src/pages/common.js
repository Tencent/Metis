/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

import numeral from 'numeral';

export function getDefaultChartOption() {
  return {
    title: {},
    grid: {
      left: 35,
      right: 20,
      bottom: 25,
      top: 10,
      containLabel: true,
    },
    dataZoom: [
      { start: 0 },
      { type: 'inside'},
    ],
    tooltip: {
      show: true,
      trigger: 'axis',
      formatter: (params) => {
        if (!params || params.length == 0) {
          return;
        }
        let content = `${params[0].axisValueLabel}<br />`;
        params.forEach((item) => {
          content = `${content}<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:${
            item.color}"></span>${item.seriesName}: ${item.value || '--'}<br />`;
        });
        return content;
      },
    },
    legend: {
      data: ['数据A', '数据B', '数据C'],
      right: 10,
    },
    xAxis: {
      data: [],
    },
    yAxis: {
      axisLabel: {
        formatter: (value) => {
          return numeral(value).format('0.[00]a');
        },
      },
    },
    color: ['#006eff', '#29cc85', '#ffbb00'],
    series: [
      {
        name: '数据A',
        type: 'line',
        showSymbol: false,
        data: [],
        z: 3,
        lineStyle: {
          normal: {
            width: 1,
            color: '#006eff',
          },
        },
      },
      {
        name: '数据B',
        type: 'line',
        showSymbol: false,
        data: [],
        z: 2,
        lineStyle: {
          normal: {
            width: 1,
            color: '#29cc85',
          },
        },
      },
      {
        name: '数据C',
        type: 'line',
        showSymbol: false,
        data: [],
        z: 1,
        lineStyle: {
          normal: {
            width: 1,
            color: '#ffbb00',
          },
        },
      },
    ]
  };
}

export function getTableCell(text) {
  return (text !== '' && text !== null && text !== undefined) ? text : '-';
}