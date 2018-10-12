/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

const path = require('path');
const fs = require('fs');
const nunjucks = require('nunjucks');
const { getOptions } = require('loader-utils');
const { envConfig: { appPath, libPath }, appConfig: { language = [] }} = require('../context');
const winPath = require('../utils/winPath');

const pageNunjucks = fs.readFileSync(path.join(__dirname, '../template/page.njk')).toString();
nunjucks.configure('views', {
  autoescape: false,
});

module.exports = function uwxLoader(source, ...extra) {
  if (this.cacheable) {
    this.cacheable();
  }

  const { isPage } = getOptions(this) || {};

  const { imports, replacedSource, models, styles } = getImports(source);

  const className = firstUpperCase(path.basename(this.resourcePath, '.uwx'));
  const uwxString = nunjucks.renderString(pageNunjucks, {
    className, imports, models, styles, isPage, language,
    uwx: replacedSource,
    libPath: winPath(libPath),
    appPath: winPath(appPath),
  });
  this.callback(null, uwxString, ...extra);
};

function firstUpperCase(str) {
  return str.toLowerCase().replace(/( |^)[a-z]/g, (L) => L.toUpperCase());
}

function getImports(source) {
  const reg = /{\s*\/\*\s*component\s+src\s*=\s*(?:"|')(\S+)(?:"|')\s+(?:name\s*=\s*(?:"|')(\S+)(?:"|'))?\s*\*\/\s*}/g;
  let results = source.match(reg);
  const imports = [];
  if (results) {
    results.forEach((result) => {
      const regexp = /{\s*\/\*\s*component\s+src\s*=\s*(?:"|')(\S+)(?:"|')\s+(?:name\s*=\s*(?:"|')(\S+)(?:"|'))?\s*\*\/\s*}/g;
      let [none, component, name] = regexp.exec(result);
      if (!name) {
        name = firstUpperCase(path.basename(component, '.uwx'));
      }
      imports.push({ component, name });
    });
  }
  const replaced = source.replace(reg, '');

  const { models, modelCleanSource } = getModels(replaced);
  const { styles, replacedSource } = getStyles(modelCleanSource);

  return { imports, models, styles, replacedSource };
}

function getModels(source) {
  const reg = /{\s*\/\*\s*import\s+src\s*=\s*(?:"|')(.+)(?:"|')\s*\*\/\s*}/g;
  let results = source.match(reg);
  const models = [];
  if (results) {
    results.forEach((result) => {
      const regexp = /{\s*\/\*\s*import\s+src\s*=\s*(?:"|')(.+)(?:"|')\s*\*\/\s*}/g;
      let [none, src] = regexp.exec(result);
      const name = path.basename(src, '.uw').toLowerCase();
      src = winPath(src.replace(/{{\s*app\s*}}/g, appPath));
      models.push({ src, name });
    });
  }
  

  const modelCleanSource = source.replace(reg, '');

  return { models, modelCleanSource };
}

function getStyles(source) {
  const reg = /{\s*\/\*\s*style\s+src\s*=\s*(?:"|')(.+)(?:"|')\s*\*\/\s*}/g;
  let results = source.match(reg);
  const styles = [];
  if (results) {
    results.forEach((result) => {
      const regexp = /{\s*\/\*\s*style\s+src\s*=\s*(?:"|')(.+)(?:"|')\s*\*\/\s*}/g;
      let [none, src] = regexp.exec(result);
      src = winPath(src.replace(/{{\s*app\s*}}/g, appPath));
      styles.push({ src });
    });
  }
  

  const replacedSource = source.replace(reg, '');

  return { styles, replacedSource };
}