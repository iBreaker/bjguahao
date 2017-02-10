#!/bin/python
# -*- coding: utf-8

import re
import json
import time
import cookielib
import urllib2

mobileNo = "136xxx"
password = "xxx"
date = "2017-02-16"

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

def get_ids(urlOpener):
    url = "http://www.bjguahao.gov.cn/dpt/partduty.htm"
    data = "hospitalId=142&departmentId=200039674&dutyCode=1&dutyDate=" + date + "&isAjax=true"
    request = urllib2.Request(url, data)
    request = add_header(request)
    ret = urlOpener.open(request).read()
    msg = json.loads(ret)
    doctorId =  msg['data'][0]['doctorId']
    dutySourceId = msg['data'][0]['dutySourceId']
    return { "dutySourceId": dutySourceId, "doctorId": doctorId}

def gen_url(ids):
    return "http://www.bjguahao.gov.cn/order/confirm/142-200039674-" + \
           str(ids['doctorId']) + "-" + str(ids['dutySourceId']) + ".htm"

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
    data = "dutySourceId=" + str(ids['dutySourceId']) +                            \
           "&hospitalId=142&departmentId=200039674&doctorId=" +                    \
           str(ids['doctorId']) + "&patientId=" + str(patientId) +                 \
           "&hospitalCardId=&medicareCardId=&reimbursementType=1&smsVerifyCode=" + \
           msg_code + "&childrenBirthday=&isAjax=true"

    request = urllib2.Request(url, data)
    request = add_header(request)
    ret = urlOpener.open(request).read()
    msg = json.loads(ret)
    print msg['msg']

def main():
    urlOpener = auth_login()
    ids = get_ids(urlOpener)
    patientId = get_patientId(urlOpener, ids)
    send_msg_code(urlOpener)
    msg_code = raw_input("input: ")
    fuck(urlOpener, ids, patientId, msg_code)

main()
