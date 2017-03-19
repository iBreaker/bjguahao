#!/usr/bin/env python
# -*- coding: utf-8
"""
北京市预约挂号统一平台
"""

import os
import sys
import re
import json
import time

from log import Log
from browser import Browser
from lib.prettytable import PrettyTable

reload(sys)
sys.setdefaultencoding( "utf-8" )

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

class Guahao(object):
    """
    挂号
    """

    def __init__(self):
        self.browser = Browser()
        self.dutys = ""

        self.login_url = "http://www.bjguahao.gov.cn/quicklogin.htm"
        self.send_code_url = "http://www.bjguahao.gov.cn/v/sendorder.htm"
        self.get_doctor_url = "http://www.bjguahao.gov.cn/dpt/partduty.htm"
        self.confirm_url = "http://www.bjguahao.gov.cn/order/confirm.htm"
        self.patient_id_url = "http://www.bjguahao.gov.cn/order/confirm/"


    def auth_login(self):
        """
        登陆
        """
        Log.info("开始登陆")
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

        if len(self.dutys) == 0:
            return "NotReady"

        self.print_doctor()

        for doctor in self.dutys[::-1]:
            if doctor['remainAvailableNumber']:
                Log.info(u"选中:" + str(doctor["doctorName"]))
                return doctor
        return "NoDuty"

    def print_doctor(self):

        Log.info("当前号余量:")
        x = PrettyTable()
        x.border = True
        x.field_names = ["医生姓名", "擅长", "号余量"]
        for doctor in self.dutys:
            x.add_row([doctor["doctorName"], doctor['skill'], doctor['remainAvailableNumber']])
        print x.get_string()
        pass

    def get_it(self, doctor, sms_code):
        """
        挂号
        """
        duty_source_id = str(doctor['dutySourceId'])
        hospital_id = self.config.hospital_id
        department_id = self.config.department_id
        doctor_id = str(doctor['doctorId'])

        preload = {
            'dutySourceId':duty_source_id,
            'hospitalId':hospital_id ,
            'departmentId': department_id,
            'doctorId': doctor_id,
            'patientId': "222444072",
            'hospitalCardId': "",
            'medicareCardId': "",
            "reimbursementType":"10",       # 报销类型
            'smsVerifyCode': sms_code,        # TODO 获取验证码
            'childrenBirthday':"",
			'isAjax': True
        }
        response = self.browser.post(self.confirm_url , data=preload)
        Log.debug("response data:" +  response.text)

        try:
            data = json.loads(response.text)
            if data["msg"] == "OK" and data["hasError"] == False and data["code"] == 200:
                Log.info("挂号成功")
                return True
            else:
                Log.error(data["msg"])
                return False

        except Exception, e:
            Log.error(repr(e))
            time.sleep(1)



    def gen_url(self, doctor):

        return self.patient_id_url + str(self.config.hospital_id) + \
           "-" + str(self.config.department_id) + "-" + str(doctor['doctorId']) + "-" +   \
            str(doctor['dutySourceId']) + ".htm"

    def get_patient_id(self, doctor):
        addr = self.gen_url(doctor)
        response = self.browser.get(addr, "")
        ret = response.text
        m = re.search('.*<input type=\\"radio\\" name=\\"hzr\\" value=\\"(.*?)\\".*', ret)
        if m == None:
            exit("获取患者id失败")
        else:
            return m.group(1)

    def get_duty_time(self):
        """获取放号时间"""
        return "9:30"

    def get_sms_verify_code(self):
        """获取短信验证码"""
        response = self.browser.post(self.send_code_url, "")
        data = json.loads(response.text)
        Log.debug(response.text)
        if data["msg"] == "OK." and data["code"] == 200:
            Log.info("获取验证码成功")
            return raw_input("输入短信验证码: ")
        elif data["msg"] == "短信发送太频繁" and data["code"] == 812:
            Log.exit(data["msg"])
        else:
            Log.error(data["msg"])
            return None

    def run(self):
        """主逻辑"""

        config = Config()                       # config对象
        config.load_conf()                      # 加载配置
        self.config = config
        self.auth_login()                       # 1. 登陆
        while True:
            print ""
            print ""
            # TODO 获取放号时间，放号前一分钟获取验证码, 放号时间前30秒开始循环
            sms_code = self.get_sms_verify_code()               # 获取验证码
            if sms_code == None:
                continue
            doctor = self.select_doctor()            # 2. 选择医生
            Log.info( "病人ID:" + str(self.get_patient_id(doctor)))       # 3. 获取病人id
            if doctor == "NoDuty":
                Log.error("没号了,  亲~")
                break
            elif doctor == "NotReady":
                Log.info("好像还没放号？重试中")
                time.sleep(1)
            else:
                result = self.get_it(doctor, sms_code)                 # 4.挂号
                if result == True:
                    break                                    # 挂号成功

if __name__ == "__main__":
    Log.load_debug_level()
    guahao = Guahao()
    guahao.run()
