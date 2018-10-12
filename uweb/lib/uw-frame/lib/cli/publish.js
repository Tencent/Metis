/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

const spawn = require('child_process').spawn;
const path = require('path');
const fs = require('fs');
require('colors');

const scriptPath = path.join(__dirname, 'app.js');
const npmignore = path.join(process.cwd(), '.npmignore');

if (!fs.existsSync(npmignore)) {
  fs.writeFileSync(npmignore, `
*
!dist/**/*.*
`);
}

const appProcess = spawn('node', [scriptPath]);

let hasError = false;

appProcess.stdout.on('data', (data) => {
  console.log(data.toString());
});

appProcess.stderr.on('data', (data) => {
  console.log(data.toString().red);
});

appProcess.on('close', () => {
  if(hasError) return;
  const publishProcess = spawn('tnpm', ['publish']);

  publishProcess.stdout.on('data', (data) => {
    console.log(data.toString());
  });

  publishProcess.stderr.on('data', (data) => {
    console.log(data.toString().red);
  });
});