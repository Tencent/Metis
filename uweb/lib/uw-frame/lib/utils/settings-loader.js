/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

const fs = require('fs');
const path = require('path');
const context = require('../context');
const winPath = require('../utils/winPath');

module.exports = function () {
  if (this.cacheable) {
    this.cacheable();
  }
  const callback = this.async();
  const { appConfig, envConfig } = context;
  const { pages = {}, modules = [], request, homePage, sourceTree, language, loginType = true, navigation = true, globalConfig = {}, logoUrl } = appConfig;
  const { appPath, env } = envConfig;
  const pagesWithAbsoluteUrl = {};

  Object.keys(pages).forEach((key) => {
    if (!pages[key].file) return;
    pagesWithAbsoluteUrl[key] = {
      view: winPath(path.join(appPath, `${pages[key].file}.uwx`)),
      distName: key.replace(/(:|~)/g, '').replace(/\//g, '.'),
    };
  });

  callback(null, `
  module.exports = {
    pages: ${JSON.stringify(pages)},
    modules: ${JSON.stringify(modules)},
    request: ${JSON.stringify(request)},
    sourceTree: ${JSON.stringify(sourceTree)},
    appPath: '${winPath(envConfig.appPath)}',
    env: '${env}',
    loginType: ${loginType},
    ${homePage ? `homePage: '${homePage}',` : ''}
    ${language ? `language: ${JSON.stringify(language)},` : ''}
    navigation: ${navigation},
    logoUrl: '${logoUrl}',
    globalConfig: ${JSON.stringify(globalConfig)}
  };
`)
};