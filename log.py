#!/usr/bin/env python
# -*- coding: utf-8

import time


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
        print("\033[0;37m " + Log.get_time()  + " [info] " + msg  + "\033[0m")

    @staticmethod
    def debug(msg):
        """
        debug
        """
        print("\033[0;34m " + Log.get_time()  + " [debug] " + msg  + "\033[0m")


    @staticmethod
    def error(msg):
        """
        输出错误
        """
        print("\033[0;31m " + Log.get_time()  + " [error] " + msg  + "\033[0m")

    @staticmethod
    def exit(msg):
        """
        打印信息，并退出
        """
        Log.error(msg)
        Log.error("exit")
        exit(0)

