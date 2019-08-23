#!/usr/bin/env python
# -*- coding: utf-8 -

# 这里需修改 config_name 为你的配置文件名称，如
config_name = "config.yaml"

# 以脚本地址作为配置文件地址
import sys, os
config_path = os.path.join(os.path.dirname(sys.argv[0]), config_name)

try:
    import requests
except:
    import pip
    pip.main(['install', 'requests'])

try:
    import yaml
except:
    import pip
    pip.main(['install', 'PyYAML'])

if __name__ == "__main__":
    from bjguahao import Guahao
    guahao = Guahao(config_path)
    guahao.run()
