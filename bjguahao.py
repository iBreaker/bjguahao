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
import datetime


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
        self.patient_name = ""
        self.patient_id = ""

    def load_conf(self, config_path):
        """
        加载配置
        """

        try:
            with open(config_path) as json_file:
                data = json.load(json_file)
                data = data[0]
                self.mobile_no = data["username"]
                self.password = data["password"]
                self.date = data["date"]
                self.hospital_id = data["hospitalId"]
                self.department_id = data["departmentId"]
                self.duty_code = data["dutyCode"]
                self.patient_name = data["patientName"]

                Log.info("配置加载完成")
                Log.debug("手机号:" + str(self.mobile_no ))
                Log.debug("挂号日期:" + str(self.date))
                Log.debug("医院id:" + str(self.hospital_id))
                Log.debug("科室id:" + str(self.department_id))
                Log.debug("上午/下午:" + str(self.duty_code))
                Log.debug("就诊人姓名:" + str(self.patient_name))

    	except  Exception, e:
            Log.exit(repr(e))

class Guahao(object):
    """
    挂号
    """

    def __init__(self):
        self.browser = Browser()
        self.dutys = ""
        self.refresh_time = ''

        self.login_url = "http://www.bjguahao.gov.cn/quicklogin.htm"
        self.send_code_url = "http://www.bjguahao.gov.cn/v/sendorder.htm"
        self.get_doctor_url = "http://www.bjguahao.gov.cn/dpt/partduty.htm"
        self.confirm_url = "http://www.bjguahao.gov.cn/order/confirm.htm"
        self.patient_id_url = "http://www.bjguahao.gov.cn/order/confirm/"
        self.department_url = "http://www.bjguahao.gov.cn/dpt/appoint/"


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
	
	# log current date
        Log.debug("当前挂号日期: " + self.config.date)

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
        patient_id = self.config.patient_id
        doctor_id = str(doctor['doctorId'])

        preload = {
            'dutySourceId':duty_source_id,
            'hospitalId':hospital_id ,
            'departmentId': department_id,
            'doctorId': doctor_id,
            'patientId': patient_id,
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



    def gen_doctor_url(self, doctor):

        return self.patient_id_url + str(self.config.hospital_id) + \
           "-" + str(self.config.department_id) + "-" + str(doctor['doctorId']) + "-" +   \
            str(doctor['dutySourceId']) + ".htm"

    def get_patient_id(self, doctor):
        """获取就诊人Id"""
        addr = self.gen_doctor_url(doctor)
        response = self.browser.get(addr, "")
        ret = response.text
        m = re.search(u'<input type=\\"radio\\" name=\\"hzr\\" value=\\"(?P<patientId>\d+)\\"[^>]*> ' + self.config.patient_name, ret)
        if m == None:
            exit("获取患者id失败")
        else:
            self.config.patient_id = m.group('patientId')
            Log.info( "病人ID:" + self.config.patient_id)

            return self.config.patient_id

    def gen_department_url(self):
        return self.department_url + str(self.config.hospital_id) + \
            "-" + str(self.config.department_id) + ".htm"

    def get_duty_time(self):
        """获取放号时间"""
        addr = self.gen_department_url()
        response = self.browser.get(addr, "")
        ret = response.text

        # 放号时间
        m = re.search(u'<span>更新时间：</span>每日(?P<refreshTime>\d{1,2}:\d{2})更新', ret)
        refresh_time = m.group('refreshTime')
        # 放号日期
        m = re.search(u'<span>预约周期：</span>(?P<appointDay>\d+)<script.*',ret)
        appoint_day = m.group('appointDay')

        today = datetime.date.today()
	
	# 优先确认最新可挂号日期
        self.stop_date = today + datetime.timedelta(days=int(appoint_day))
        Log.info("今日可挂号到: " + self.stop_date.strftime("%Y-%m-%d"))
	
	# 自动挂最新一天的号
        if self.config.date == 'latest':
            self.config.date = unicode(self.stop_date.strftime("%Y-%m-%d"))
            Log.info("当前挂号日期变更为: " + self.config.date)

        # 生成放号时间和程序开始时间
        con_data_str = self.config.date + " " + refresh_time + ":00"
        self.start_time =  datetime.datetime.strptime(con_data_str, '%Y-%m-%d %H:%M:%S') +  datetime.timedelta(days= - int(appoint_day))
        Log.info("放号时间: " + self.start_time.strftime("%Y-%m-%d %H:%M"))

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

    def run(self, config_path):
        """主逻辑"""

        config = Config()                       # config对象
        config.load_conf(config_path)                      # 加载配置
        self.config = config
        self.get_duty_time()


        self.auth_login()                       # 1. 登陆

        if self.start_time > datetime.datetime.now():
            seconds =  (self.start_time -  datetime.datetime.now()).total_seconds()
            Log.info("距离放号时间还有" + str(seconds) + "秒")
            sleep_time = seconds - 60
            if sleep_time > 0:
                Log.info("程序休眠" + str(sleep_time) + "秒后开始运行")
                time.sleep(sleep_time)

        doctor = "";
        while True:
            doctor = self.select_doctor()            # 2. 选择医生
            if doctor == "NoDuty":
                Log.error("没号了,  亲~")
                break
            elif doctor == "NotReady":
                Log.info("好像还没放号？重试中")
                time.sleep(1)
            else:
                sms_code = self.get_sms_verify_code()               # 获取验证码
                if sms_code == None:
                    time.sleep(1)

                self.get_patient_id(doctor)         # 3. 获取病人id
                result = self.get_it(doctor, sms_code)                 # 4.挂号
                if result == True:
                    break                                    # 挂号成功

if __name__ == "__main__":
    # 生成默认 config 地址
    config_path = 'config.json'

    # 覆盖 config 地址
    for i in range(1, len(sys.argv)):
        if (sys.argv[i] == '-c') & (i+1 < len(sys.argv)):
            config_path = sys.argv[i+1]
    Log.load_config(config_path)
    guahao = Guahao()
    guahao.run(config_path)
