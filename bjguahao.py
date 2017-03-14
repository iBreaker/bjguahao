#!/usr/bin/env python
# -*- coding: utf-8
"""
北京市预约挂号统一平台
"""

import re
import json
import time
import cookielib
import urllib2

mobileNo = "136xxx"  #账号
password = "xxx"   #密码
date = "2017-02-17"       #挂号日期

hospitalId = 142          #北医三院
departmentId = 200039584  #运动医学
dutyCode = 1  #上午/下午/全天


def add_header(request):
    request.add_header('User-Agent', "Mozilla/5.0 (Windows NT 6.1; WOW64;")
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    request.add_header('Cache-Control', 'no-cache')
    request.add_header('Accept', '*/*')
    request.add_header('Connection', 'Keep-Alive')
    return request


def auth_login():
    cookiejar = cookielib.CookieJar()
    urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    AuthUrl = "http://www.bjguahao.gov.cn/quicklogin.htm"
    data = "mobileNo=" + mobileNo + "&password=" + password + "&yzm=" + "&isAjax=true"
    request = urllib2.Request(AuthUrl, data)
    request = add_header(request)
    ret = urlOpener.open(request).read()
    msg = json.loads(ret)['msg']
    if msg == 'OK':
        return urlOpener
    else:
        exit(msg)

def send_msg_code(urlOpener):
    while True:
        url = "http://www.bjguahao.gov.cn/v/sendorder.htm"
        data = ""
        request = urllib2.Request(url, data)
        request = add_header(request)
        ret = urlOpener.open(request).read()
        msg = json.loads(ret)['msg']
        if msg == 'OK.':
            break
        else:
            print msg
            time.sleep(10)

"""
-1 号没有放出，或者今天没号
-2 号被预约完了
"""
def get_ids(urlOpener):
    url = "http://www.bjguahao.gov.cn/dpt/partduty.htm"

    if dutyCode != "1" or dutyCode != "2":
        print "dutyCode 参数错误"
        exit(0)
    data = "hospitalId=" + str(hospitalId) +                \
           "&departmentId=" + str(departmentId) +           \
           "&dutyCode=" + dutyCode  + "&dutyDate=" + date + "&isAjax=true"
    request = urllib2.Request(url, data)
    request = add_header(request)
    ret = urlOpener.open(request).read()
    msg = json.loads(ret)
    if len(msg['data']) == 0:
        return -1

    # 越往后水平越高
    for doctor in msg['data'][::-1]:
        print "医生名字:\t", doctor['doctorName'], "擅长:\t", doctor['skill'], "号余量:\t", doctor['remainAvailableNumber']

    for doctor in msg['data'][::-1]:
        if doctor['remainAvailableNumber']:
            print "选中:"
            print "医生名字:\t", doctor['doctorName'], "擅长:\t", doctor['skill'], "号余量:\t", doctor['remainAvailableNumber']
            return { "dutySourceId": doctor['dutySourceId'], "doctorId": doctor['doctorId']}
    return -2

def gen_url(ids):
    return "http://www.bjguahao.gov.cn/order/confirm/" + str(hospitalId) + \
           "-" + str(departmentId) + "-" + str(ids['doctorId']) + "-" +   \
           str(ids['dutySourceId']) + ".htm"

def get_patientId(urlOpener, ids):
    url = gen_url(ids)
    request = urllib2.Request(url)
    request = add_header(request)
    ret = urlOpener.open(request).read()
    m = re.search('.*<input type=\\"radio\\" name=\\"hzr\\" value=\\"(.*?)\\".*', ret)
    if m == None:
        exit("获取患者id失败")
    else:
        return m.group(1)

"""
@dutySourceId   病号id
@hospitalId     医院id  默认: 北医三院
@departmentId   科室id  默认: 运动医学(特需)
@doctorId       医生id
@patientId      患者id
@medicreCardId  就诊类型
@smsVerifyCode  短信验证码
"""
def fuck(urlOpener, ids, patientId, msg_code):
    url = "http://www.bjguahao.gov.cn/order/confirm.htm"
    data = "dutySourceId=" + str(ids['dutySourceId']) +                              \
           "&hospitalId=" + str(hospitalId) + "&departmentId=" + str(departmentId) + \
           "&doctorId=" + str(ids['doctorId']) + "&patientId=" + str(patientId) +    \
           "&hospitalCardId=&medicareCardId=&reimbursementType=1&smsVerifyCode=" +   \
           msg_code + "&childrenBirthday=&isAjax=true"

    request = urllib2.Request(url, data)
    request = add_header(request)
    ret = urlOpener.open(request).read()
    msg = json.loads(ret)
    if msg['msg'] == "OK":
        print "恭喜, 挂号成功:)"
    else:
        print msg['msg']

def config():
    """
    读取配置文件
    """
    global mobileNo
    global password
    global date
    global hospitalId
    global departmentId
    global dutyCode

    try:
        with open('config.json') as json_file:
            data = json.load(json_file)
            mobileNo = data["username"]
            password = data["password"]
            date = data["date"]
            hospitalId = data["hospitalId"]
            departmentId = data["departmentId"]
            dutyCode = data["dutyCode"]
    except  :
        print "读取配置错误"
        exit(0)


def main():
    """
    主函数 负责主逻辑
    """
    config()
    urlOpener = auth_login()
    send_msg_code(urlOpener)
    while True:
        while True:
            ids = get_ids(urlOpener)
            if ids == -2:
                exit("今天没有号了")
            elif ids == -1:
                print "号还没有放出, 等待..."
                time.sleep(5)         #号还没有产生，sleep 5秒
                continue
            else:
                break
        patientId = get_patientId(urlOpener, ids)
        msg_code = raw_input("输入短信验证码: ")
        fuck(urlOpener, ids, patientId, msg_code)
        send_msg_code(urlOpener)

if __name__ == "__main__":
    main()
