/*
  Tencent is pleased to support the open source community by making Metis available.
  Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
  Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
  https://opensource.org/licenses/BSD-3-Clause
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

import qs from 'qs';
import _ from 'lodash';

declare global {
  interface Window {
    uw: any;
  }
}

export default function loginValidate(location, history, navigation) {
  const query = window.location.search.replace(/^\?/, '');
  const xTicket = qs.parse(query)['ticket'];
  window.uw.request({
    url: '/unified/auth/doAuth',
    needLogin: false,
    headers: {
      'x-ticket': xTicket,
    },
    success: ({ code, data }) => {
      if (code === '4000') {
        if (navigation) {
          window.location.href = `${data.loginUrl}${window.location.href}`;
        } else {
          window.top.location.href = `${data.loginUrl}${window.top.location.href}`;
        }
      } else {
        window.uw.event.emit('@@auth_success');
        const userName = window.uw.cookie.get('userName');
        const isAdmin = window.uw.cookie.get('isAdmin');
        const userId = window.uw.cookie.get('userId');
        window.uw.storage.set('global.user', { userName, isAdmin: isAdmin === 'true' ? true : false, userId });
        const { pathname, search } = location;
        let queryWithoutTicket = _.omit(qs.parse(search.replace(/^\?/, '')), ['ticket', 'loginParam', 'lengh', 'length', 'sessionKey']);
        queryWithoutTicket = qs.stringify(queryWithoutTicket);
        history.replace(`${pathname}${queryWithoutTicket === '' ? '' : `?${queryWithoutTicket}`}`);
      }
    },
  });
}
