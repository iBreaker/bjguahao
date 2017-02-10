#!/usr/bin/env python
#coding:utf-8
import sys
import urllib
import urllib2
import cookielib
import json
import time
USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/45.0.2454.93 Safari/537.36'
)
class APIError(Exception):
    pass
class MergeRequest(object):
    DEFAULT_TITLE = 'Merge Request'
    DEFAULT_CONTENT = ''
    def __init__(self, src_branch, dst_branch):
        self.src_branch = src_branch
        self.dst_branch = dst_branch
        self.title = MergeRequest.DEFAULT_TITLE
        self.content = MergeRequest.DEFAULT_CONTENT
class Client(object):
    def __init__(self):
        self.domain = "www.bjguahao.gov.cn"
        self.login_path = "quicklogin.htm"
        self.cookie = cookielib.CookieJar();
        self.opener = urllib2.build_opener(
                             urllib2.HTTPCookieProcessor(self.cookie),
                        )
        self.opener.addheaders = [
            ('User-Agent', USER_AGENT),
        ]
    def request(self, method, url, data=None):
        payload = urllib.urlencode(data) if data else None
        request = urllib2.Request(url, payload)
        request.get_method = lambda: method
        try:
            response = self.opener.open(request)
            return response
        except Exception:
            raise APIError("unknow error")
       
    def login(self, mobileNo, password):
        url = "http://" + self.domain + "/" + self.login_path
        post_data = dict(mobileNo = mobileNo, password = password, yzm = '', isAjax='true')
        page = self.request('POST', url, data=post_data)
        if(page.read() == '{"data":[],"hasError":false,"code":200,"msg":"OK"}'):
            return True
        else:
            return False
    def getOrder(self):
        url = "http://" + self.domain + "/" + "/v/sendorder.htm"
        page = self.request('POST', url)
        if(page.read() == '{"code":200,"msg":"OK."}'):
            return True
        else:
            return False
    def getDutySourceId(self, json_result):
        
        #print json_result
        s = json.loads(json_result)
        for i in s["data"]:
            if '7' in i["doctorTitleName"] and u'œ•' in i["skill"] and u'…À' in i["skill"]:
                #print [i["dutySourceId"], i["doctorId"]]
                return [i["dutySourceId"], i["doctorId"]]
        #print s["data"][0]["dutySourceId"]
        try:
            return [s["data"][1]["dutySourceId"], s["data"][1]["doctorId"]]
        except:
            return [s["data"][0]["dutySourceId"], s["data"][0]["doctorId"]]
    def makeUrl(self, hospitalId, departmentId, dutyDate, dutyCode):
        url = "http://" + self.domain + "/dpt/partduty.htm"
    #post_data = dict(hospitalId=142, departmentId='200039602', dutyCode=2, dutyDate='2016-08-01', isAjax='true')
        post_data = dict(hospitalId=hospitalId, departmentId=departmentId, dutyCode=dutyCode, dutyDate=dutyDate, isAjax='true')
        try:
            page = self.request('POST', url, post_data)
        except:
            print "403"
            return False
        htm =  page.read()
        if htm == '{"data":[],"hasError":false,"code":200,"msg":"OK"}':
            return False
        sourceId = self.getDutySourceId(htm)
        #return "http://www.bjguahao.gov.cn/order/confirm/" + str(hospitalId) + '-' + str(departmentId) + '-' + sourceId[1] + '-' + sourceId[0] + ".htm"
        url =  "http://www.bjguahao.gov.cn/order/confirm/" + str(hospitalId) + '-' + str(departmentId) + '-' + str(sourceId[1]) + '-' + str(sourceId[0]) + ".html"
    return [str(hospitalId), str(departmentId), str(sourceId[1]), str(sourceId[0]), url]
    def guahao(self, msg, patientId, smsVerifyCode):
        url = "http://" + self.domain + "/order/confirm.htm"
        post_data = dict(dutySourceId=msg[3], hospitalId=msg[0], departmentId=msg[1], doctorId=msg[2], patientId=patientId, hospitalCardId='', medicareCardId='', reimbursementType=1, smsVerifyCode=smsVerifyCode, isFirstTime=2, hasPowerHospitalCard=2, cidType=1, childrenBirthday='',childrenGender=2, isAjax='true')
        page = self.request('POST', url, post_data)
        return page.read()
        
if __name__ == "__main__":
    client = Client()
    if client.login("’ ∫≈", "√‹¬Î") != True:
        print "login error"
        exit(0)
    else:
        print "login success"
    #msg = client.makeUrl(142, 200039602, '2016-07-28', 2 )
    print "begin get doctor msg"
    i = 0
    while True:
        #msg = client.makeUrl(208, 200003296, '2016-08-01', 2 )
        msg = client.makeUrl(142, 200039602, '2016-08-02', 2 )
        if msg != False:
            break
        print "retry %s times"%i
        i+=1
        time.sleep(0.3)
    
    result = client.guahao(msg, 222444072,int(sys.argv[1]))
    print result
    if "—È÷§¬Î" in result:
        client.getOrder()
        code = raw_input("input: ")
        print client.guahao(msg, 222444072, int(code))
    #print client.getOrder() 
    pass
