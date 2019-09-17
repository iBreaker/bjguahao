# 北京市预约挂号统一平台脚本

![](https://img.shields.io/badge/Language-Python-007fc0.svg)
![](https://img.shields.io/badge/license-GPLv3-000000.svg)
![](https://img.shields.io/badge/made%20with-%3C3-red.svg)

Copyright (C) 2017-2019

**目前稳定版已经发布，欢迎吐槽和试用**

* 本程序用于 [北京市预约挂号统一平台](http://www.bjguahao.gov.cn/) 的挂号，只支持北京地区医院的挂号。
* 挂号是刚需。帝都有些医院号源紧张，放号瞬间被秒杀一空，遂产生了撸一脚本挂号的念头。说干就干，简单的分析和调试后于 16 年 8 月份左右产出第一版，顺利挂上了XXX院运动医学科的号。很开心。
* 17 年 2 月底的时候，朋友也需要挂一个号，脚本给他改了改，貌似删了重写的？没有仔细看。经过精心的分析和调试，挂了一个专家号。很开心。
* 17 年 3 月 8 号，两位热心网友github上发起issues，提出反馈，让我很意外。本来想着这脚本自己写着用就可以了。接到反馈后觉得可以写成一个成熟的软件了。两位热心网友也主动提出改进代码的愿望。很开心。
* __还看什么看，来贡献代码__ ;-)

`2017-03-08 17:12:20 breaker`

## 环境

### 正式版已经不支持python2环境，请使用python3运行本程序
- Python3

## 使用方法

1. 安装依赖库，例如：``` pip install --user -r requirements.txt ```
2. 修改配置文件
3. 运行命令：
    - 默认用法： ```python bjguahao.py```
    - 指定配置： ```python bjguahao.py -c your-conf.yaml```

**Android QPython3 使用方法**
1. 安装 [QPython3](https://play.google.com/store/apps/details?id=org.qpython.qpy3) 和 [QPython](https://play.google.com/store/apps/details?id=org.qpython.qpy)
2. 安装 [QPy3.6](https://play.google.com/store/apps/details?id=org.qpython.qpy36) 并运行（会安装 Python 3.6）
3. 在 QPython3 中将版本切为 Python 3.6（默认为 Python 3.2）
4. 修改配置文件(```config.yaml```或自定义)
5. 由于 QPython3 不支持传参，如需指定配置文件，需手动修改```qpython3_run.py```中的```config_name```配置文件名
6. 将整个项目复制到你的 Android
7. 在 QPython3 中运行```qpython3_run.py```

*备注：*
- 若配置文件不在项目目录，也可修改```qpython3_run.py```中的```config_path```为配置文件的**绝对**地址
- 如需以项目的形式直接运行脚本，可以将```qpython3_run.py```改名为```main.py```，并将文件夹放置在```qpython/projects3/```下
- 也可将文件夹放置在```qpython/scripts3/```下，而后为```qpython3_run.py```建立桌面快捷方式。


**Windows 环境使用方法**
1. 新增了windows版本的exe文件
2. 把配置文件放在exe文件同目录
3. 修改配置文件
4. 双击exe开始挂号，成功后程序自动退出


## 配置文件

默认配置文件 `config.yaml`

```yaml

# username: 您的的用户名(一般是手机号码)
username: "13888888888"

# password: 密码
password: "*****"

# date: 挂号日期
date: "2018-01-01"


# hospitalId: 医院id
hospitalId: "162"

# departmentId: 科室id
departmentId: "200002248"

# 关于如何获取 hospitalId 和 departmentId
# 1. 打开挂号页面
# 2. 假设地址栏中地址是 http://www.bjguahao.gov.cn/dpt/appoint/162-200002248.htm
# 3. 其中 162 是 hospitalId
# 4. 其中 200002248 是 departmentId


# 需要挂早上的号请填写1  需要挂下午的号请填写2
dutyCode: "1"

# patientName: 患者姓名
# 若是自己挂号可为空
patientName: "曹操"

# doctorName: 医生姓名
# 不填写的话默认选最好的医生
# 填写后若这个医生没有号，会自动选其余号中最好的医生
doctorName:
  - "扁鹊"
  - "华佗"
  - "杨永信"

# 指定医生
# false:默认不指定
# true:只挂指定医生的号
assign: "false"

#true:检索每天余票
remaining: "false"

#remaining=true时,默认检索工作日,周末:6,7
week: "1,2,3,4,5"

#挂号类型是否为儿童号
children: "false"

#患儿名字 如果儿童挂号必须填写
childrenName: ""

#患儿证件号 如果儿童挂号必须填写
childrenIdNo: ""

#患儿证件
#1:身份证
#2:其他
cidType: "1"

# chooseBest: 选择模式
# 不填写的默认从最好的医生开始选择
# 可选项为"yes" 或者 "no"
chooseBest: "yes"


# DebugLevel: 调试等级
# 支持的调试等级有 debug/info/warning/error/critical
DebugLevel: "info"

#使用ios短信和mac电脑接收验证码
useIMessage: "false"

# 是否使用 QPython3.6 运行本脚本
useQPython3: "false"
```

## 文档

[文档](doc.md) 中有比较详细的接口分析和装包。

[ChangeLog](ChangeLog.md) release版本更新内容

## 挂号攻略

[攻略](tips.md) 中有详细的挂号攻略, 感谢[@lily0101](https://github.com/lily0101)提供

## 调试

开发者请将`config.yaml`配置文件中的`DebugLevel`参数设置为`debug`

## 加入我们

在使用过程中有任何问题建议，或者贡献代码，请加入交流群

![image](https://github.com/iBreaker/bjguahao/raw/master/img/qq-qun.png)

## 致谢

感谢 [yiqian987](https://github.com/yiqian987) 修改 [issues#27](https://github.com/iBreaker/bjguahao/issues/27)

感谢 [coeusite](https://github.com/coeusite) 支持android挂号 [pull#56](https://github.com/iBreaker/bjguahao/pull/56)

感谢 [cuteapi](https://github.com/cuteapi) 添加 iphone mac 验证码自动获取的功能，抢号神器哦

感谢 [cxl008](https://github.com/cxl008) 更新登录以及获取验证码代码

感谢 [haoming06](https://github.com/haoming06) 支持挂指定大夫号、可监测每天余号,捡漏等功能 [pull#96](https://github.com/iBreaker/bjguahao/pull/96)、[pull#99](https://github.com/iBreaker/bjguahao/pull/99)

若遗漏了您，请发邮件通知我 <791628659#qq.com>

## 协议

![](https://www.gnu.org/graphics/gplv3-127x51.png)

bjguahao 基于 GPL-3.0 协议进行分发和使用，更多信息参见协议文件。


## Stargazers over time

![Stargazers over time](https://starchart.cc/iBreaker/bjguahao.svg)


