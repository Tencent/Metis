/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

import React from 'react';
import _ from 'lodash';
import './login.less';

const { View, Panel, Form, Input, Icon, Button, Dropdown } = require('../../../../uw2/index');
const FormItem = Form.Item;

declare global {
  interface Window {
    uw: any;
  }
}

export default class Login extends React.Component<any, any> {

  state = {
    errorMsg: null,
    validate: { name: '', password: '' },
    name: '',
    password: '',
    ownerList: [],
    selectedOwner: '',
    loading: false,
  };

  login = () => {
    const isValidated = this.validate();
    if (!isValidated) return;
    this.setState({ loading: true });
    const { name, password } = this.state;
    window.uw.request({
      url: '/unified/login/byAccount',
      method: 'POST',
      data: { account: name.trim(), pwd: password },
      success: ({ code, msg }) => {
        if (code === '0') {
          this.getLoginUserInfo();
        } else {
          this.setState({ errorMsg: msg, loading: false });
        }
      },
    });
  }

  getLoginUserInfo = () => {
    window.uw.request({
      url: '/unified/userInfo/getLoginUserOwnerInfo',
      success: ({ code, data, msg }) => {
        if (code === '0') {
          const { ownerType } = data;
          if (ownerType === 1) {
            const { returnurl } = window.uw.qs.parse(this.props.location.search.slice(1));
            window.location.href = returnurl || this.props.settings.homePage;
          } else if (ownerType === 2) {
            this.getOwnerList();
          }
        } else {
          this.setState({ errorMsg: msg, loading: false });
        }
      },
    });
  }

  getOwnerList = () => {
    window.uw.request({
      url: '/unified/userInfo/getCurrentUserOwnerList',
      success: ({ code, data = [], msg }) => {
        if (code === '0') {
          const selectedOwner = _.get(data, '0.ownerId', '');
          const ownerList = data.map((o: any) => ({ label: o.ownerName, value: o.ownerId }));
          this.setState({ ownerList, selectedOwner, loading: false });
        } else {
          this.setState({ errorMsg: msg, loading: false });
        }
      },
    });
  }

  selectOwner = () => {
    const { selectedOwner } = this.state;
    this.setState({ loading: true });
    window.uw.request({
      url: '/unified/userInfo/selectOwnerInfo',
      method: 'POST',
      data: { ownerId: selectedOwner },
      success: ({ code, msg }) => {
        if (code === '0') {
          const { returnurl } = window.uw.qs.parse(this.props.location.search.slice(1));
          window.location.href = returnurl || this.props.settings.homePage;
        } else {
          this.setState({ errorMsg: msg, loading: false });
        }
      },
    });
  }

  onFieldChange = (field) => {
    return (value) => {
      this.setState({
        [field]: value,
        validate: { ...this.state.validate, [field]: '' },
        errorMsg: '',
      });
    };
  }

  validate = () => {
    const { name, password } = this.state;
    const rules = {
      name: [
        ['required', '用户名不能为空'],
      ],
      password: [
        ['required', '密码不能为空'],
      ],
    };
    const result = window.uw.validate({ name, password }, rules);
    if (!result.isValidated) {
      this.setState({ validate: { ...this.state.validate, ...result.errors } });
    }

    return result.isValidated;
  }

  render() {
    return (
      <div className={`uw-login ${this.state.errorMsg ? 'error' : ''}`}>
        <View title="登录">
          {_.isEmpty(this.state.ownerList) ? (
            <Panel>
              <h1 className="login-title">用户登录</h1>
              <Form>
                <FormItem
                  help={this.state.validate.name}
                  hasError={this.state.validate.name}
                >
                  <Input placeholder="用户名" value={this.state.name} size="large" onPressEnter={this.login} onChange={this.onFieldChange('name')} />
                </FormItem>
                <FormItem
                  help={this.state.validate.password}
                  hasError={this.state.validate.password}
                >
                  <Input placeholder="密码" value={this.state.password} onPressEnter={this.login} size="large" type="password" onChange={this.onFieldChange('password')} />
                </FormItem>
              </Form>
              {this.state.errorMsg && <p className="error-msg"><Icon type="error-small" /> {this.state.errorMsg}</p>}
              <div className="uw-login-button">
                <Button type="primary" onClick={this.login} disabled={this.state.loading}>{this.state.loading ? <Icon type="loading" /> : '登录'}</Button>
              </div>
            </Panel>
          ) : (
              <Panel>
                <h1 className="login-title">选择租户</h1>
                <Form>
                  <FormItem label="">
                    <Dropdown size="large" options={this.state.ownerList} value={this.state.selectedOwner} onChange={this.onFieldChange('selectedOwner')} />
                  </FormItem>
                </Form>
                {this.state.errorMsg && <p className="error-msg"><Icon type="error-small" /> {this.state.errorMsg}</p>}
                <div className="uw-login-button">
                  <Button type="primary" onClick={this.selectOwner} disabled={this.state.loading}>{this.state.loading ? <Icon type="loading" /> : '选择'}</Button>
                </div>
              </Panel>
            )}
        </View>
      </div>
    );
  }
}
