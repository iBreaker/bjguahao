import re
import datetime
import logging

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
        while retry > 0:
            retry -= 1
            # 检查 SMS
            code = self._check_sms_verify_code()
            # 有效验证码？
            if code != '000000':
                break
            else:
                time.sleep(0.05)
        return code

    # 读取验证码短信
    def _check_sms_verify_code(self):
        # init
        code = '000000'
        # 获取当前的全部未读短信
        smsMessageIds = self.droid.smsGetMessageIds(True)
        # loop
        for smsId in smsMessageIds:
            # get message
            smsMessage = self.droid.smsGetMessageById(smsId)
            # TODO 时间筛选
            smsTimestamp = smsMessage.timestamp
            # 跳过开始时间点前 SMS
            if smsTimestamp < self.start_time:
                continue
            # TODO 文字匹配
            smsContent = smsMessage.content
            res = self.regex.search(smsContent)
            if res is None:
                continue
            else:
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
