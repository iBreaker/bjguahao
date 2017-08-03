## 北京挂号网站协议分析

### 登陆

#### 登陆请求

|参数名|含义|举个栗子|
|------|----|----|
|mobileNo|手机号|181\*\*\*\*\*\*\*\*|
|password|密码|123456|
|yzm|是个谜，不影响|空|
|isAjax|是个谜，不影响|true|

抓包
```
POST /quicklogin.htm HTTP/1.1
Host: www.bjguahao.gov.cn
Connection: keep-alive
Content-Length: 55
Accept: application/json, text/javascript, */*; q=0.01
Origin: http://www.bjguahao.gov.cn
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Referer: http://www.bjguahao.gov.cn/logout.htm
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8
Cookie: SESSION_COOKIE=3cab1829cea36adbceb47f7e; Hm_lvt_bc7eaca5ef5a22b54dd6ca44a23988fa=1488332034,1488961795,1488964531,1489046102; Hm_lpvt_bc7eaca5ef5a22b54dd6ca44a23988fa=1489051044; JSESSIONID=72682F948A035CA8B7AE4FCA180EF92E

mobileNo=185********&password=********&yzm=&isAjax=true
```


#### 登陆回应
|参数名|含义|举个栗子|
|------|----|----|
|data||一般为空|
|hasError|是否有错误|false|
|code||200|
|msg|是否登陆成功(重要)|OK|

抓包(登陆成功)
```
HTTP/1.1 200 OK
Set-Cookie: JSESSIONID=8154A5F2CFA1A140155CCAD2A13480B2; Path=/; HttpOnly
Content-Disposition: inline;filename=f.txt
Accept-Charset: big5, big5-hkscs, cesu-8, euc-jp, euc-kr, gb18030, gb2312, gbk, ibm-thai, ibm00858, ibm01140, ibm01141, ibm01142, ibm01143, ibm01144, ibm01145, ibm01146, ibm01147, ibm01148, ibm01149, ibm037, ibm1026, ibm1047, ibm273, ibm277, ibm278, ibm280, ibm284, ibm285, ibm290, ibm297, ibm420, ibm424, ibm437, ibm500, ibm775, ibm850, ibm852, ibm855, ibm857, ibm860, ibm861, ibm862, ibm863, ibm864, ibm865, ibm866, ibm868, ibm869, ibm870, ibm871, ibm918, iso-2022-cn, iso-2022-jp, iso-2022-jp-2, iso-2022-kr, iso-8859-1, iso-8859-13, iso-8859-15, iso-8859-2, iso-8859-3, iso-8859-4, iso-8859-5, iso-8859-6, iso-8859-7, iso-8859-8, iso-8859-9, jis_x0201, jis_x0212-1990, koi8-r, koi8-u, shift_jis, tis-620, us-ascii, utf-16, utf-16be, utf-16le, utf-32, utf-32be, utf-32le, utf-8, windows-1250, windows-1251, windows-1252, windows-1253, windows-1254, windows-1255, windows-1256, windows-1257, windows-1258, windows-31j, x-big5-hkscs-2001, x-big5-solaris, x-compound_text, x-euc-jp-linux, x-euc-tw, x-eucjp-open, x-ibm1006, x-ibm1025, x-ibm1046, x-ibm1097, x-ibm1098, x-ibm1112, x-ibm1122, x-ibm1123, x-ibm1124, x-ibm1166, x-ibm1364, x-ibm1381, x-ibm1383, x-ibm300, x-ibm33722, x-ibm737, x-ibm833, x-ibm834, x-ibm856, x-ibm874, x-ibm875, x-ibm921, x-ibm922, x-ibm930, x-ibm933, x-ibm935, x-ibm937, x-ibm939, x-ibm942, x-ibm942c, x-ibm943, x-ibm943c, x-ibm948, x-ibm949, x-ibm949c, x-ibm950, x-ibm964, x-ibm970, x-iscii91, x-iso-2022-cn-cns, x-iso-2022-cn-gb, x-iso-8859-11, x-jis0208, x-jisautodetect, x-johab, x-macarabic, x-maccentraleurope, x-maccroatian, x-maccyrillic, x-macdingbat, x-macgreek, x-machebrew, x-maciceland, x-macroman, x-macromania, x-macsymbol, x-macthai, x-macturkish, x-macukraine, x-ms932_0213, x-ms950-hkscs, x-ms950-hkscs-xp, x-mswin-936, x-pck, x-sjis_0213, x-utf-16le-bom, x-utf-32be-bom, x-utf-32le-bom, x-windows-50220, x-windows-50221, x-windows-874, x-windows-949, x-windows-950, x-windows-iso2022jp
Content-Type: text/html;charset=UTF-8
Content-Length: 50
Date: Thu, 09 Mar 2017 09:22:32 GMT
Connection: close
Server: Tengine/2.1.2

{"data":[],"hasError":false,"code":200,"msg":"OK"}
```

抓包(登陆失败)
```

```

### 查询
|参数名|含义|举个栗子|
|------|----|-----|
|hospitalId|医院ID|270|
|departmentId|科室ID|200003874|
|dutyCode|上午下午|1表示上午，2表示下午|
|dutyDate|挂号日期|2017-03-13|
|isAjax|是个谜|true就好|
```
POST /dpt/partduty.htm HTTP/1.1
Host: www.bjguahao.gov.cn
Connection: keep-alive
Content-Length: 80
Accept: application/json, text/javascript, */*; q=0.01
Origin: http://www.bjguahao.gov.cn
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Referer: http://www.bjguahao.gov.cn/dpt/appoint/270-200003874.htm
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8
Cookie: SESSION_COOKIE=3cab1829cea36adbceb47f7e; Hm_lvt_bc7eaca5ef5a22b54dd6ca44a23988fa=1488332034,1488961795,1488964531,1489046102; Hm_lpvt_bc7eaca5ef5a22b54dd6ca44a23988fa=1489051826; JSESSIONID=6DFFC0825127030360E31B2C0E11E031

hospitalId=270&departmentId=200003874&dutyCode=1&dutyDate=2017-03-13&isAjax=true
```
### 挂号
```
dutySourceId:46882064
hospitalId:102
departmentId:200039730
doctorId:201125970
patientId:123321123
jytCardId:
medicareCardId:
reimbursementType:1
smsVerifyCode:326814
childrenName:
cidType:1
childrenIdNo:
childrenBirthday:2011-07-03
childrenGender:2
isAjax:true
```
|------|----|-----|
|dutySourceId|当天医生挂号页面ID|46882064|
|hospitalId|医院ID|270|
|departmentId|科室ID|200003874|
|doctorId|医生ID|201125970|
|patientId|挂号人ID|123321123|
|jytCardId|京医通号码|xxxxxxxxxxxx|
|medicareCardId|医保卡号码|xxxxxxxxxxx|
|reimbursementType|报销类型|1.医疗保险、2.商业保险、3.公费医疗、4.新农合、5.异地医保、6.红本医疗、7.工伤、8.一老一小、9.超转、10.自费、11.生育险、12.其他|
|smsVerifyCode|短信验证码|326814|
|childrenName|患儿名称|当需要挂儿研所这类医院时需要|
|cidType|患儿证件类型|1为身份证 2为其他|
|childrenIdNo|患儿身份证|18位身份证|
|childrenBirthday|患儿生日|当cidType为2时此项为必填|
|childrenGender|患儿性别|1为男，2为女。当cidType为2时此项为必填|
|isAjax|是个谜|true就好|

### 关于验证码
