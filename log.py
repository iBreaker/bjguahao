#!/usr/bin/env python
# -*- coding: utf-8

import time
import json

class Debug_level():
    debug = 1
    info = 2
    error = 3


debug_level = Debug_level.info

class Log(object):
    """
    日志
    """

    @staticmethod
    def load_debug_level():
        """获取log配置"""
        try:
            with open('config.json') as json_file:
                data = json.load(json_file)
                data = data[0]
                if data["DebugLevel"] == "info":
                    debug_level = Debug_level.info
                elif data["DebugLevel"] == "debug":
                    debug_level = Debug_level.debug
                elif data["DebugLevel"] == "error":
                    debug_level = Debug_level.error

    	except  Exception, e:
            Log.error(repr(e))
            Log.error("获取Log模块配置失败，DebugLevel设置为默认值:info")


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
        if debug_level <= Debug_level.info:
            print("\033[0;37m " + Log.get_time()  + " [info] " + msg  + "\033[0m")

    @staticmethod
    def debug(msg):
        """
        debug
        """
        if debug_level <= Debug_level.debug:
            print("\033[0;34m " + Log.get_time()  + " [debug] " + msg  + "\033[0m")


    @staticmethod
    def error(msg):
        """
        输出错误
        """
        if debug_level <= Debug_level.error:
            print("\033[0;31m " + Log.get_time()  + " [error] " + msg  + "\033[0m")

    @staticmethod
    def exit(msg):
        """
        打印信息，并退出
        """
        Log.error(msg)
        Log.error("exit")
        exit(0)

