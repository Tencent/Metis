/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

import React from 'react';
const { Line } = require('../../../lib/uw-chart');
const { Icon } = require('../../../lib/uw2');
import './Chart.less';

interface ChartProps {
  loading: boolean;
  option: any;
  height: number | string;
  width: number | string;
}

export default class Chart extends React.Component<ChartProps, any> {
  render() {
    const { height = 300, width = '100%', loading = false, option } = this.props;
    return (
      <div style={{ height, width }}>
        {loading && <div className="uw-chart-loading"><Icon type="loading"/></div>}
        <Line {...option} height={height} width={width}/>
      </div>
    );
  }
}