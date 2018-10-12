/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

import React from 'react';
import { BrowserRouter as Router, Route, Redirect, Switch } from 'react-router-dom';
import Layout from './theme/layout/layout';
import Login from './theme/login/login';

export default function (settings) {
  const { homePage, language = [], custom = {} } = settings;
  const hasLanguage = language.length !== 0;

  if (_.isFunction(custom.onLaunch)) {
    custom.onLaunch();
  }
  
  if (hasLanguage) {
    const defaultLang = language[0];
    const currentLang = window.location.pathname.split('/')[1];
    const useDefaultLang = language.indexOf(currentLang) === -1;
    const basename = useDefaultLang ? '/' : currentLang;
    const lang = useDefaultLang ? defaultLang : currentLang;

    return () => (
      <Router basename={`${basename}`}>
        <Switch>
          <Route path="/users/login" render={(props) => {
            return <Login settings={settings} {...props} lang={lang} />
          }} />
          <Route path="/" render={(props) => {
            const { location } = props;
            if (homePage && location.pathname === `/`) {
              return <Redirect to={`${homePage}`} />;
            }
            return <Layout settings={settings} {...props} lang={useDefaultLang ? defaultLang : currentLang} />;
          }} />
        </Switch>
      </Router>
    );
  }

  return () => (
    <Router>
      <Switch>
        <Route path="/users/login" render={(props) => {
          return <Login settings={settings} {...props} />
        }} />
        <Route path="/" render={(props) => {
          const { location } = props;
          if (homePage && location.pathname === '/') {
            return <Redirect to={homePage} />;
          }
          return <Layout settings={settings} {...props} />
        }} />
      </Switch>
    </Router>
  );
}
