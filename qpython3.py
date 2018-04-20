import re
import datetime
import logging
import time

from androidhelper import Android

# 主 Class
class QPython3(object):
    # 初始化
    def __init__(self):
        self.regex = re.compile('证码为.*【(\d+)】') # regex
        self.start_time = datetime.datetime.now()
        # Android QPython3
        self.droid = Android()
        logging.debug("QPython3 实例初始化完成")
    # 读取验证码短信
    def _get_sms_verify_code(self):
        # init
        self.start_time = datetime.datetime.now()
        code = '000000'
        retry = 600
        # loop
        logging.debug("监控短信中……")
        while retry > 0:
            retry -= 1
            # 检查 SMS
            code = self._check_sms_verify_code()
            # 有效验证码？
            if code != '000000':
                logging.debug("取得有效验证码……"+code)
                break
            else:
                logging.debug("未找到有效验证码……重试中, retry = {}".format(retry))
                time.sleep(0.05)
        else:
            logging.debug("未找到有效验证码……"+code)
        return code
    # 读取验证码短信
    def _check_sms_verify_code(self):
        # init
        code = '000000'
        # 获取当前的全部未读短信
        smsMessageIds = self.droid.smsGetMessageIds(True)
        # 无短信退出
        if len(smsMessageIds.result) == 0:
            logging.debug("无短信退出……")
            return code
        # loop
        for smsId in smsMessageIds.result:
            # get message
            smsMessage = self.droid.smsGetMessageById(smsId)
            # 时间筛选
            smsTimestamp = datetime.datetime.fromtimestamp(int(smsMessage.result['date'])/1e3)
            # 跳过开始时间点前 SMS
            if smsTimestamp < self.start_time:
                # print("时间跳过:", smsMessage)
                continue
            # 文字匹配
            smsContent = smsMessage.result['body']
            res = self.regex.search(smsContent)
            if res is None:
                # print("匹配跳过:", smsMessage)
                continue
            else:
                # print("发现短信:", smsMessage)
                code = res.group(1).strip()
                break
        return code
    # 获取验证码的外部调用
    def get_verify_code(self):
        logging.debug("获取验证码中……")
        # 读取验证码短信
        return self._get_sms_verify_code()



## 测试使用
def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    droid = QPython3()
    code = droid.get_verify_code()
    print(code)

if __name__ == '__main__':
    main()
