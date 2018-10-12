/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

import React from 'react';
import _ from 'lodash';
const { View, Button } = require('../../../../uw2/index');
import loginValidate from '../../core/builtIn/login';
import '../static/index.less';

declare global {
  interface Window {
    uw: any;
    Plugins: any;
  }
}

interface LayoutProps {
  location: any;
  settings: any;
  history: any;
  lang: any;
}

const { Header, Sider } = View;

export default class Layout extends React.PureComponent<LayoutProps, any> {
  sourceTree;
  state = {
    is404: false,
    iframe: '',
  };
  constructor(props) {
    super(props);
    this.sourceTree = props.settings.sourceTree;

    window.uw.go = (link) => {
      props.history.push(link);
    };

    window.uw.back = () => {
      props.history.goBack();
    };
  }

  componentDidMount() {
    const { loginType, navigation } = this.props.settings;
    window.uw.event.on('@@auth_expired', () => {
      loginValidate(this.props.location, this.props.history, navigation);
    });

    if (loginType) {
      window.uw.event.emit('@@auth_expired');
    } else {
      this.componentDidUpdate(null);
    }

    if (!navigation) {
      document.body.style.minWidth = '0px';
      document.getElementsByTagName('html')[0].style.minWidth = '0px';
    }
  }

  getHeaderModules(navi) {
    return navi.map((nav) => {
      // 默认模块的跳转为 pages 中的第一项的 path， 如果第一项为分类，则取分类的第一项 path
      const link = _.get(nav.pages[0], 'path', _.get(nav.pages[0], 'pages.0.path', ''));
      return {
        title: nav.title,
        link,
      };
    });
  }

  getSiderModules(location, modules) {
    const sider = {
      title: '',
      moduleList: [],
      currentKey: '',
      openedKeys: [],
      appName: '',
      sider: true,
    };

    let finded = false;

    _.forEach(modules, ({ pages, title, sider: showSider = true }) => {
      if (finded) return;
      findModule(pages);
      if (finded) {
        sider.title = title;
        (sider.moduleList as any) = generateModule(pages);
        if (!_.isUndefined(showSider)) sider.sider = showSider;
      }
    });

    function findModule(pages) {
      _.forEach(pages, (page) => {
        if (location.indexOf(page.path) !== -1) {
          finded = true;
          sider.currentKey = page.path;
          sider.appName = page.title;
        } else if (page.pages) {
          findModule(page.pages);
        }
      });
    }

    function generateModule(pages) {
      return _.map(pages, (page, index) => {
        let key = page.path;
        if (!key) {
          key = index;
          (sider.openedKeys as string[]).push(key);
        }
        return {
          title: page.title,
          externalLink: page.externalLink,
          external: page.external,
          key,
          link: page.path,
          children: generateModule(page.pages),
          iframe: page.iframe,
        };
      });
    }

    return sider;
  }

  logout = () => {
    window.uw.request({
      url: '/unified/login/doOut',
      success: () => {
        this.props.history.push('/');
        window.uw.storage.clear('global');
      },
    });
  }

  componentDidUpdate(prev) {
    const { location, history, lang, settings } = this.props;
    const { pathname } = location;
    const { moduleList } = this.getSiderModules(pathname, settings.modules);

    if (prev && (this.props.location === prev.location && settings.modules === prev.settings.modules)) return;

    const filePath = this.sourceTree[pathname];
    const iframe = _.get(_.find(moduleList, ['link', pathname]), 'iframe');
    if (filePath && moduleList.length !== 0) {
      this.setState({ is404: false, iframe: false }, () => window.uw.event.emit('@@page_start_download', { pathname, filePath, props: { history, location, lang } }));
    } else if (iframe) {
      this.setState({ is404: false, iframe }, () => {
        const ele: any = document.getElementById('uw_child_page');
        const iframeEle = document.createElement('iframe');
        if (ele.firstChild) ele.removeChild(ele.firstChild);
        iframeEle.src = this.state.iframe;
        ele.appendChild(iframeEle);
      });
    } else {
      this.setState({ is404: true, iframe: false });
    }
  }

  render() {
    const { location, settings, history } = this.props;
    const { pathname } = location;
    const { modules, navigation, logoUrl = require('../static/zhiyun-logo.svg') } = settings;

    const { title, currentKey, moduleList, openedKeys, sider, appName } = this.getSiderModules(pathname, modules);
    const extra = [
      {
        title: window.uw.storage.get('global.user.userName'),
        children: [
          { content: <div onClick={this.logout}>退出登录</div> },
        ],
      },
    ];

    if (this.state.is404) {
      return (
        <View title="404 无法找到页面" mode={navigation ? 'normal' : 'iframe'}>
          <Header logo={logoUrl} modules={this.getHeaderModules(modules)} extra={extra} onPathChange={(path) => history.push(path)} />
          <div className="notfound-bg">
            <window.Plugins.Placeholder
              image={require('../static/404.svg')}
              title="哎呀，该页面无法找到"
              content="请检查输入的地址是否有误，或者你可以"
              footer={(<Button onClick={() => history.push(settings.homePage || '/')} type="primary">返回主页</Button>)}
            />
          </div>
        </View>
      );
    }

    return (
      <View title={`${appName} - ${title}`} mode={navigation ? 'normal' : 'iframe'}>
        <Header logo={logoUrl} modules={this.getHeaderModules(modules)} extra={extra} onPathChange={(path) => history.push(path)} />
        {sider && <Sider defaultOpenedKeys={openedKeys} title={title} modules={moduleList} selectedKeys={[currentKey]} onPathChange={(path) => history.push(path)} />}
        {this.state.iframe ? (
          <div id="uw_child_page" className={sider ? 'iframe' : 'no-sider iframe'}></div>
        ) : (
          <div id="uw_child_page" className={sider ? undefined : 'no-sider'}></div>
        )}
      </View>
    );
  }
}
