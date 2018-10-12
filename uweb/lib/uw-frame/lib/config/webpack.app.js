/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = function ({ envConfig, appConfig }) {
  const { libPath, distPath, appPath, version } = envConfig;
  const { entries, target, publicPath = '/' } = appConfig;
  const sourceArr = Object.values(entries);

  const tsLoader = {
    loader: 'awesome-typescript-loader',
    options: {
      configFileName: `${path.join(libPath, 'config/tsconfig.json')}`,
    },
  };

  const babelLoader = {
    loader: 'babel-loader',
    options: {
      presets: ['env', 'react', 'stage-0'],
      plugins: ['transform-runtime', 'add-module-exports', 'syntax-dynamic-import'],
    }
  };

  return {
    mode: 'production',
    entry: entries,
    output: {
      filename: (file) => {
        const { name } = file.chunk;
        if (name === 'source') return '[name].js';
        return `[name].${version}.js`;
      },
      path: distPath,
      library: "_loaded_file",
      publicPath: `${publicPath}/`,
      libraryTarget: "window",
    },
    target, // 支持 electron-renderer 等 https://webpack.js.org/configuration/target/
    resolve: {
      extensions: ['.ts', '.tsx', '.js', '.json'],
    },
    externals: ['react', 'react-dom', 'lodash', 'moment', 'echarts', '@tencent/uw2', '@tencent/uw-plugins', '@tencent/uw-api'],
    module: {
      rules: [
        { test: /\.(tsx?)$/, use: [tsLoader], include: [libPath, appPath] },
        { test: /\.(jsx?)$/, use: [babelLoader], include: [libPath, appPath] },
        { test: /\.uw$/, use: [babelLoader, path.join(libPath, 'utils', 'uw-loader.js')] },
        { test: /\.less$/, use: ['style-loader', 'css-loader', 'less-loader'] },
        { test: /\.css$/, use: ['style-loader', 'css-loader'] },
        { test: /\.(png|jpg|gif|svg)$/, use: [{ loader: 'file-loader', options: { name: '[name].[ext]', outputPath: 'assets/' } }] },
        // 解析作为页面的 UWX
        {
          test: (pathname) => pathname.indexOf('.uwx') !== -1 && sourceArr.indexOf(pathname) !== -1,
          use: [babelLoader, { loader: path.resolve(libPath, 'utils', 'uwx-loader.js'), options: { isPage: true } }],
        },
        // 解析作为组件的 UWX
        {
          test: (pathname) =>  pathname.indexOf('.uwx') !== -1 && sourceArr.indexOf(pathname) == -1,
          use: [babelLoader, { loader: path.resolve(libPath, 'utils', 'uwx-loader.js'), options: { isPage: false } }],
        },
      ],
    },
    plugins: [
      new CleanWebpackPlugin([distPath], {
        root: process.cwd()
      }),
    ],
  }
}