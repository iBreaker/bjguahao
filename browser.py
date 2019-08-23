#!/usr/bin/env python
# -*- coding: utf-8


import pickle
import requests


class Browser(object):
    """
    浏览器
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

    def load_cookies(self, path):
        with open(path, 'rb') as f:
            self.session.cookies = requests.utils.cookiejar_from_dict(pickle.load(f))

    def save_cookies(self, path):
        with open(path, 'wb') as f:
            cookies_dic = requests.utils.dict_from_cookiejar(self.session.cookies)
            pickle.dump(cookies_dic, f)

    def get(self, url, data):
        """
        http get
        """
        pass
        response = self.session.get(url)
        if response.status_code == 200:
            self.session.headers['Referer'] = response.url
        return response

    def post(self, url, data):
        """
        http post
        """
        response = self.session.post(url, data=data)
        if response.status_code == 200:
            self.session.headers['Referer'] = response.url
        return response

