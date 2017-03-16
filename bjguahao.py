#!/usr/bin/env python
# -*- coding: utf-8
"""
北京市预约挂号统一平台
"""

import os
import sys
import json
import time
import pickle
import requests
import requests.utils

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
                data = data[0]
                self.mobile_no = data["username"]
                self.password = data["password"]
                self.date = data["date"]
                self.hospital_id = data["hospitalId"]
                self.department_id = data["departmentId"]
                self.duty_code = data["dutyCode"]

                Log.info("配置加载完成")
                Log.debug("手机号:" + str(self.mobile_no ))
                Log.debug("挂号日期:" + str(self.date))
                Log.debug("医院id:" + str(self.hospital_id))
                Log.debug("科室id:" + str(self.department_id))
                Log.debug("上午/下午:" + str(self.duty_code))

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
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        self.root_path = os.path.dirname(os.path.realpath(sys.argv[0]))


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
        Log.debug("post data :" +  str(data))
        response = self.session.post(url, data=data)
        if response.status_code == 200:
            self.session.headers['Referer'] = response.url
        return response

class Guahao(object):
    """
    挂号
    """

    def __init__(self, config):
        self.browser = Browser()
        self.config = config
        self.dutys = ""

        self.login_url = "http://www.bjguahao.gov.cn/quicklogin.htm"
        self.send_code_url = "http://www.bjguahao.gov.cn/v/sendorder.htm"
        self.get_doctor_url = "http://www.bjguahao.gov.cn/dpt/partduty.htm"
        self.confirm_url = "http://www.bjguahao.gov.cn/order/confirm.htm"


    def auth_login(self):
        """
        登陆
        """
        password = self.config.password
        mobile_no = self.config.mobile_no
        preload = {
			'mobileNo': mobile_no,
			'password': password,
            'yzm':'',
			'isAjax': True,
		}
        response = self.browser.post(self.login_url, data=preload)
        Log.debug("response data:" +  response.text)
        try:
            data = json.loads(response.text)
            if data["msg"] == "OK" and data["hasError"] == False and data["code"] == 200:
                cookies_file = os.path.join(self.browser.root_path, self.config.mobile_no + ".cookies")
                self.browser.save_cookies(cookies_file)
                Log.info("登陆成功")
                return True
            else:
                Log.error(data["msg"])
                raise Exception()

        except Exception, e:
            Log.error("登陆失败")
            Log.exit(repr(e))

    def get_code(self):
        """
        获取验证码
        """
        pass

    def select_doctor(self):
        """选择合适的大夫"""

        hospital_id = self.config.hospital_id
        department_id = self.config.department_id
        duty_code = self.config.duty_code
        duty_date = self.config.date

        preload = {
            'hospitalId':hospital_id ,
            'departmentId': department_id,
            'dutyCode': duty_code,
            'dutyDate': duty_date,
			'isAjax': True
        }
        response = self.browser.post(self.get_doctor_url , data=preload)
        Log.debug("response data:" +  response.text)

        try:
            data = json.loads(response.text)
            if data["msg"] == "OK" and data["hasError"] == False and data["code"] == 200:
                self.dutys = data["data"]

        except Exception, e:
            Log.exit(repr(e))

        for doctor in self.dutys[::-1]:
            print "医生名字:", doctor['doctorName'], "\t\t擅长:", doctor['skill'], "\t\t号余量:", doctor['remainAvailableNumber']

        for doctor in self.dutys[::-1]:
            if doctor['remainAvailableNumber']:
                print "选中:"
                print "医生名字:\t", doctor['doctorName'], "擅长:\t", doctor['skill'], "号余量:\t", doctor['remainAvailableNumber']
                return doctor

    def get_it(self, doctor ):
        """
        挂号
        """
        duty_source_id = str(doctor['dutySourceId'])
        hospital_id = self.config.hospital_id
        department_id = self.config.department_id
        duty_code = self.config.duty_code
        duty_date = self.config.date
        doctor_id = str(doctor['doctorId'])

        preload = {
            'dutySourceId':duty_source_id,
            'hospitalId':hospital_id ,
            'departmentId': department_id,
            'dutyCode': duty_code,
            'dutyDate': duty_date,
            'doctorId': doctor_id,
            'patientId': "",
            'hospitalCardId': "",
            'medicareCardId': "",
            'smsVerifyCode': "",
            'childrenBirthday':"",
			'isAjax': True
        }
        response = self.browser.post(self.confirm_url , data=preload)
        #Log.debug("response data:" +  response.text)


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
        print("\033[0;37;40m " + Log.get_time()  + " [info] " + msg  + "\033[0m")

    @staticmethod
    def debug(msg):
        """
        debug
        """
        print("\033[0;34;40m " + Log.get_time()  + " [debug] " + msg  + "\033[0m")


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
    config = Config()
    config.load_conf()
    guahao = Guahao(config)
    guahao.auth_login()
    doctor = guahao.select_doctor()
    guahao.get_it(doctor)


