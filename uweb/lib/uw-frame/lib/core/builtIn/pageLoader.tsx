/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

import React from 'react';
import ReactDOM from 'react-dom';
import loadSource from './loadSource';

declare global {
  interface Window {
    $routes: object;
    _loaded_file: object;
    uw: any;
  }
}

export default function pageLoader() {
  window.$routes = {}; // 全局缓存的页面

  window.uw.event.on('@@page_start_download', (e) => {
    const { detail = {} } = e;
    const { filePath, pathname, props } = detail;

    if (!filePath || !pathname) return;

    if (window.$routes[pathname]) {
      loadPage(window.$routes[pathname], props);
    } else {
      loadSource(filePath).then(() => {
        const mod = window._loaded_file;
        if (mod) {
          loadPage(mod, props);
          window.$routes[pathname] = mod;
        }
      });
    }
  });

  function loadPage(Cmp, props) {
    const elem = document.getElementById('uw_child_page');
    if (elem) {
      if (elem.firstChild) {
        ReactDOM.unmountComponentAtNode((elem.firstChild as any));
        elem.removeChild(elem.firstChild);
      }
      const newDom = document.createElement('div');
      elem.appendChild(newDom);
      ReactDOM.render(<Cmp {...props} />, newDom);
    }
  }
}
