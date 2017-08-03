# 北京市预约挂号统一平台脚本

Copyright (C) 2017

https://bjguahao.0x7c00.cn/

**目前还在调试中，没有稳定的版本，欢迎吐槽和试用**

* 本程序用于 [北京市预约挂号统一平台](http://www.bjguahao.gov.cn/) 的挂号，只支持北京地区医院的挂号。
* 挂号是刚需。帝都有些医院号源紧张，放号瞬间被秒杀一空，遂产生了撸一脚本挂号的念头。说干就干，简单的分析和调试后于16年8月份左右产出第一版，顺利挂上了XXX院运动医学科的号。很开心。
* 17年2月底的时候，朋友也需要挂一个号，脚本给他改了改，貌似删了重写的？没有仔细看。经过精心的分析和调试，挂了一个专家号。很开心。
* 17年3月8号，两位热心网友github上发起issues，提出反馈，让我很意外。本来想着这脚本自己写着用就可以了。接到反馈后觉得可以写成一个成熟的软件了。两位热心网友也主动提出改进代码的愿望。很开心。
* __还看什么看，来贡献代码__ ;-)

`2017-03-08 17:12:20 breaker`

## 环境

- Python

## 运行

- 默认用法： ```python2 bjguahao.py```
- 指定配置： ```python2 bjguahao.py -c test.json```

## 配置文件

在脚本目录将 `_config.josn` 重命名为 `config.json`, 然后写入如下数据：

```json
[
    {
        "username":"185xxxxxxx",
        "password":"*******",
        "date":"2017-02-17",            # 挂号日期，当 date='latest' 时，自动挂最新一日
        "hospitalId":"142",             # 142 北医三院
        "departmentId":"200039602",     # 运动医学科
        "dutyCode":"1",                 # 1:上午  2:下午
        "patientName":"张三",           # 就诊人姓名,可不填,适配多就诊人情况


        "DebugLevel":"info"             # debug / info / error
    }
]
```

## 文档

[文档](doc.md) 中有比较详细的接口分析和装包。

[ChangeLog](ChangeLog.md) release版本更新内容

## 调试

开发者请将`config.json`配置文件中的`DebugLevel`参数设置为`debug`

## 加入我们

在使用过程中有任何问题建议，或者共享代码，请加入交流群


![image](https://github.com/iBreaker/bjguahao/raw/master/img/qq-qun.png)



## 协议

bjguahao 基于 GPL-3.0 协议进行分发和使用，更多信息参见协议文件。
