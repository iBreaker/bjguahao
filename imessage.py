#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
from os.path import expanduser
import sqlite3
import datetime
import re
import time
import kbhit
import sys
import platform
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from concurrent.futures import FIRST_COMPLETED

OSX_EPOCH = 978307200


class IMessage(object):
    def __init__(self):
        self.regex = re.compile('证码为.*【(\d+)】')
        self.pool = ThreadPoolExecutor(2)
        self.done = False

    @staticmethod
    def _new_connection():
        # The current logged-in user's Messages sqlite database is found at:
        # ~/Library/Messages/chat.db
        db_path = expanduser("~") + '/Library/Messages/chat.db'
        try:
            conn = sqlite3.connect(db_path)
            return conn
        except Exception as e:
            print('找不到短信数据库', file=sys.stderr, flush=True)
            # sys.exit(-1)
        return None

    def _get_keyboard_verify_code(self):
        print('验证码: ', end='', flush=True)
        kb = kbhit.KBHit()
        code = ''
        while not self.done:
            if kb.kbhit():
                c = kb.getch()
                code += c
                print(c, end='', flush=True)
                if c == '\n':
                    break
        return code

    def _get_sms_verify_code(self):
        now = datetime.datetime.now()
        connection = self._new_connection()
        if connection is None:
            time.sleep(30)
            return '000000'
        c = connection.cursor()
        retry = 600
        code = '000000'
        while retry > 0 and not self.done:
            retry -= 1
            # The `message` table stores all exchanged iMessages.
            c.execute("SELECT text, date FROM `message` ORDER BY date DESC limit 1")
            for row in c:
                text = row[0]
                tm = row[1]
                if text is None:
                    continue
                res = self.regex.search(text)
                if res is None:
                    continue
                #osx 10.11.6，直接相加即可得正确时间。
                uname = platform.uname()
                if uname in ['18.2.0']:
                    rec_time = datetime.datetime.fromtimestamp(tm/1e9  + OSX_EPOCH)
                else:
                    rec_time = datetime.datetime.fromtimestamp(tm  + OSX_EPOCH)
                #print('find msg: rec_time=', rec_time)
                if rec_time < now:
                    continue
                code = res.group(1).strip()
                break
            if code != '000000':
                break
            time.sleep(0.05)
        connection.close()
        return code

    def get_verify_code(self):
        self.done = False
        keyboard = self.pool.submit(self._get_keyboard_verify_code)
        sms = self.pool.submit(self._get_sms_verify_code)
        done, not_done = wait([sms, keyboard], timeout=30, return_when=FIRST_COMPLETED)
        self.done = True
        code = '000000'
        for ft in done:
            code = ft.result()
        return code

    def __del__(self):
        try:
            self.pool.shutdown(False)
        except Exception as e:
            pass


def main():
    imsg = IMessage()
    code = imsg.get_verify_code()
    print(code)


if __name__ == '__main__':
    main()
