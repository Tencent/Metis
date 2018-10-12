/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

const path = require('path');
const fs = require('fs');
const webpack = require('webpack');
const appConfig = require(path.join(process.cwd(), 'src', 'app.json'));
const packageConfig = require(path.join(process.cwd(), 'package.json'));
const ctx = require('../context');
const Template = require('../utils/templateStringify');

const APP_PATH = path.resolve(process.cwd(), 'src'); // 应用目录
const LIB_PATH = path.join(__dirname, '..'); // uw-frame 框架目录
const DIST_PATH = path.resolve(process.cwd(), 'dist'); // 打包目录

module.exports = function (env) {
  // 构建入口文件
  const template = new Template(APP_PATH, LIB_PATH);
  const entryString = template.entryStringify(packageConfig.dependencies);
  fs.writeFileSync(path.join(LIB_PATH, 'entry.js'), entryString);

  // 生成资源文件和资源树
  const { entries, sourceTree } = generatePageEntry(appConfig.pages, APP_PATH);
  
  // 写入上下文
  const context = {
    appConfig: { ...appConfig, sourceTree, entries },
    envConfig: { appPath: APP_PATH, libPath: LIB_PATH, distPath: DIST_PATH, env }
  };
  ctx.initialize(context);

  const webpackConfig = require('../config/webpack.common')(context);

  // 返回 Webpack Compiler 对象
  return webpack(webpackConfig);
}

function generatePageEntry(pages, appPath, publicPath = '/') {
  const entries = {}; // webpack entry
  const sourceTree = {}; // URL对应资源Map树
  Object.keys(pages).forEach((pagePath) => {
    const fileKey = pagePath.replace(/\//g, '_').replace(':', ''); // 文件路径字符转义后成为文件名
    const filePath = pages[pagePath].file;
    if (filePath) {
      entries[fileKey] = path.resolve(appPath, `${filePath}.uwx`);
      sourceTree[pagePath] = `${publicPath}${fileKey}.js`;
    }
  });

  return { entries, sourceTree };
}