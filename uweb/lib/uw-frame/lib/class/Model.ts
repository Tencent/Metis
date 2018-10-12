/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

import _ from 'lodash';
import Observer from './Observer';

export default class Model {
  context; // 组件的实例

  constructor(context) {
    this.context = context;
  }

  Page = (model) => {
    if (!model.data) throw Error('必须包含 "data" 属性');

    const observer = new Observer();
    const proxy = observer.create(model.data);
    observer.bind(() => {
      if (!this.context._isUnmounted) {
        // 未来可以在这里进行比对以提高性能
        this.context.forceUpdate();
      }
    });

    Object.assign(this.context, { data: proxy });

    _.map(model, (value, key) => {
      if (_.isFunction(value)) {
        this.context[key] = value.bind(this.context);
      }
    });

    this.context.componentDidMount = () => {
      if (this.context.onLoad) this.context.onLoad();
    };

    this.context.componentWillReceiveProps = (props) => {
      if (this.context.onPropsChange) this.context.onPropsChange(props);
    };

    this.context.componentWillUnmount = () => {
      if (this.context._unload) {
        this.context._unload();
      }
      if (this.context.onUnload) this.context.onUnload();
    };
  }

  Model = (name, model) => {
    if (!model.data) throw Error('必须包含 "data" 属性');
    const observer = new Observer();
    const proxy = observer.create(model.data);

    observer.bind(() => {
      if (!this.context._isUnmounted) {
        // 未来可以在这里进行比对以提高性能
        this.context.forceUpdate();
      }
    });

    model.data = proxy;
    this.context.$model[name] = model;
  }

  Controller = (name, ctrlMethods) => {
    const onLoads: Array<() => void> = [];
    const onPropsChanges: Array<(props) => void> = [];
    const onUnloads: Array<() => void> = [];
    const ctx = { ...this.context, ...ctrlMethods };
    _.forEach(ctrlMethods, (fn, key) => {
      if (typeof fn === 'function') {
        ctrlMethods[key] = fn.bind(ctx);
        switch (key) {
          case 'onLoad':
            onLoads.push(ctrlMethods[key]);
            break;
          case 'onUnload':
            onUnloads.push(ctrlMethods[key]);
            break;
          case 'onPropsChange':
            onPropsChanges.push(ctrlMethods[key]);
            break;
        }
      }
    });

    this.context.$controller[name] = ctrlMethods;

    this.context.componentDidMount = () => {
      onLoads.forEach((fn) => fn());
    };

    this.context.componentWillReceiveProps = (props) => {
      onPropsChanges.forEach((fn) => fn(props));
    };

    this.context.componentWillUnmount = () => {
      if (this.context._unload) {
        this.context._unload();
      }
      onUnloads.forEach((fn) => fn());
    };
  }
}
