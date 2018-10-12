/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

const nunjucks = require('nunjucks');
const fs = require('fs');
const path = require('path');
const winPath = require('./winPath');
const _ = require('lodash');

class Template {
  constructor(appPath, libPath) {
    this.appPath = appPath;
    this.libPath = libPath;
  }

  entryStringify(dependencies) {
    const pluginPath = winPath(path.join(this.appPath, 'plugins'));
    const stylePath = winPath(path.join(this.appPath, 'app.less'));
    const modelPath = winPath(path.join(this.appPath, 'app.uw'));
    const entryTemplate = fs.readFileSync(path.join(this.libPath, 'template/entry.njk')).toString();
    return nunjucks.renderString(entryTemplate, {
      defaultPlugins: findDefaultPlugins(dependencies),
      plugins: fileExist(pluginPath) ? pluginPath : false,
      style: fileExist(stylePath) ? stylePath : false,
      model: fileExist(modelPath) ? modelPath : false,
    });
  }
}

module.exports = Template;

function fileExist(path) {
  try {
    return !!fs.statSync(path);
  } catch (e) {
    return false;
  }
}

function findDefaultPlugins(dependencies) {
  // 默认自动加载 uw-plugins 及 uw-plugins-xxx
  const defaultPlugins = [];
  _.forEach(dependencies, (value, key) => {
    if (key.indexOf('@tencent/uw-plugins-') !== -1) {
      defaultPlugins.push({
        name: _.capitalize(key.replace('@tencent/uw-plugins-', '')),
        path: key,
      });
    }
  });
  return defaultPlugins;
}