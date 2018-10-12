/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

import React from 'react';
import { forEach, findIndex, cloneDeep } from 'lodash';
const { Table, Icon } = require('../../../lib/uw2');
import './DetailList.less';

export interface DetailListProps {
  info: string | React.ReactNode;
  columns?: any[];
  dataSource?: any[];
  loading?: boolean;
  emptyText?: string;
}

export default class DetailList extends React.Component<DetailListProps, any> {
  state = {
    expand: false,
  };

  onShowDetailClick() {
    this.setState({ expand: !this.state.expand });
  };

  getDataSource() {
    const dataSource = cloneDeep(this.props.dataSource || []);
    let newDataSource: any[] = [];
    forEach(dataSource, (item, index) => {
      if (!('index' in item)) {
        item.index = index + 1;
      }
      newDataSource.push(item);
    });
    return newDataSource;
  };

  render() {
    const { info, columns: originColumns = [], loading = false, emptyText = '列表为空' } = this.props;
    const columns = cloneDeep(originColumns);
    const dataSource = this.getDataSource();
    if (findIndex(columns, ['key', 'index']) === -1) {
      columns.unshift({
        key: 'index',
        dataIndex: 'index',
        title: '序号',
        width: 65,
      });
    }
   
    return (
      <div className="uw-detail-list">
        <div>
          <div className="uw-detail-info">
            {info}
            {
              dataSource.length > 0 && (
                <span onClick={this.onShowDetailClick.bind(this)}>
                  <a>查看详情 {this.state.expand ? <Icon type="arrow-up" /> : <Icon type="arrow-down" />}</a>
                </span>
              )
            }
          </div>
          {
            this.state.expand && (
              <Table
                loading={loading}
                size="middle"
                columns={columns}
                dataSource={dataSource}
                rowKey="index"
                pagination={false}
                scroll={{ y: 200 }}
                placeholder={ (!loading && dataSource.length === 0) && emptyText  }
              />
            )
          }
        </div>
      </div>
    )
  }
}
