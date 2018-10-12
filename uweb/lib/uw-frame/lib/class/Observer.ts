/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

export default class Observer {
  observers = new WeakSet();
  observerHandler;
  queuedHanlder = new Set();
  setTimer;

  create = (obj) => {
    if (!obj) return obj;
    const proxy = new Proxy(obj, { get: this.get, set: this.set });
    this.observers.add(proxy);
    return proxy;
  }

  bind = (fn) => {
    this.observerHandler = fn;
  }

  get = (target, key, receiver) => {
    const result = Reflect.get(target, key, receiver);
    if (needProxy(key, result, this.observers)) {
      const observerResult = this.create(result);
      Reflect.set(target, key, observerResult, receiver);
      return observerResult;
    }
    return result;
  }

  set = (target, key, value, receiver) => {
    // 修改对象属性，即对象属性值发生变更时，将会触发 handler
    this.queuedHanlder.add(this.observerHandler);
    // 需要保证多个属性发生改变时只触发一次 hanlder
    clearTimeout(this.setTimer);
    this.setTimer = setTimeout(() => {
      this.excuteHanlder(target[key], value);
    });

    // set 方法默认行为
    return Reflect.set(target, key, value, receiver);
  }

  excuteHanlder = (oldvalue, value) => {
    try {
      this.queuedHanlder.forEach((hanlder) => {
        hanlder(oldvalue, value);
      });
    } finally {
      this.queuedHanlder.clear();
    }
  }
}

function needProxy(key, result, observers) {
  // 需要判断是否已经是proxy了，以及排除 react 的属性
  // 将不会对数组子元素进行 proxy 代理
  const reactProps = ['_store', '_owner', 'props'];
  return typeof result === 'object' && !Array.isArray(result) && !observers.has(result) && reactProps.indexOf(key) === -1;
}
