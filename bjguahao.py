#!/usr/bin/env python
# -*- coding: utf-8
"""
北京市预约挂号统一平台
"""

# import re
import json
import time
# import cookielib
# import urllib2

class Config(object):
    """
    配置
    """
    def __init__(self):
        self.mobile_no = ""
        self.password = ""
        self.date = ""
        self.hospital_id = ""
        self.department_id = ""
        self.duty_code = ""


        self.conf_path = ""

    def load_conf(self):
        """
        加载配置
        """
        try:
            with open('config.json') as json_file:
                data = json.load(json_file)
                self.mobile_no = data["username"]
                self.password = data["password"]
                self.date = data["date"]
                self.hospital_id = data["hospitalId"]
                self.department_id = data["departmentId"]
                self.duty_code = data["dutyCode"]
    	except  Exception, e:
            Log.exit(repr(e))

    def demo2(self):
        """
        demo2
        """
        pass


class Browser(object):
    """
    浏览器
    """

    def __init__(self):
        pass

    def http_get(self):
        """
        http get
        """
        pass

    def http_post(self):
        """
        http post
        """
        pass

class Guahao(object):
    """
    挂号
    """

    def __init__(self):
        pass

    def auth_login(self):
        """
        登陆
        """
        pass

    def get_code(self):
        """
        获取验证码
        """
        pass

    def select_doctor(self):
        """选择合适的大夫"""
        pass

    def get_it(self):
        """
        挂号
        """
        pass
class Log(object):
    """
    日志
    """
    @staticmethod
    def get_time():
        """
        获取时间
        """
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    @staticmethod
    def info(msg):
        """
        info
        """
        print(u"\033[0;37;40m " + Log.get_time()  + " [info] " + msg  + u"\033[0m")

    @staticmethod
    def debug(msg):
        """
        debug
        """
        print(u"\033[0;34;40m " + Log.get_time()  + " [debug] " + msg  + u"\033[0m")


    @staticmethod
    def error(msg):
        """
        输出错误
        """
        print("\033[0;31;40m " + Log.get_time()  + " [error] " + msg  + "\033[0m")

    @staticmethod
    def exit(msg):
        """
        打印信息，并退出
        """
        Log.error(msg)
        Log.error("exit")
        exit(0)


if __name__ == "__main__":
    guahao = Guahao()
    config = Config()
    config.load_conf()
    if guahao.auth_login() == False:
        pass

