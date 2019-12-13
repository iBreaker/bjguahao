# coding:utf-8
import serial, re  # 导入模块
import serial.tools.list_ports
import threading,binascii,codecs,time
from binascii import unhexlify
import struct

ser = None
msg_buffer_ls = []
msg_buffer = b''
yanzhegnma = ''


def init():
	global ser
	portx = "COM3"
	bps = 115200
	timex = 5
	ser = serial.Serial(portx, bps, timeout=timex)
	print('串口打开状态:',ser.is_open)
	print(ser)
	threading.Thread(target=recv_data, args=(ser,)).start()
	result = ser.write(b"AT+CMGF=1\n")
	# result = ser.write(b"AT+CMGL=\"ALL\"\n")
	# result = ser.write(b"AT+CMGDA=6\n")

def recv_data(ser):
	global msg_buffer_ls
	while True:
		data_len = ser.in_waiting
		if data_len > 0:
			data = ser.read(data_len)
			msg_buffer_ls.append(data)
			msg_split()

def msg_split():
	global msg_buffer_ls, msg_buffer
	while len(msg_buffer_ls) > 0:
		msg = msg_buffer_ls.pop(0)
		msg_buffer += msg
		# print('buffer:',msg_buffer)
	if b'\r\n\r\n' in msg_buffer:
		msgs = msg_buffer.split(b'\r\n\r\n')
		assert len(msgs) == 2
		single_msg = msgs[0]
		msg_buffer = msgs[1]
		print('单条信息内容：',single_msg)
		check_store_yanzhengma(single_msg)
	if b'+CMTI' in msg_buffer:
		beg = msg_buffer.index(b'+CMTI')
		if b'\r\n' in msg_buffer[beg:]:
			# print('buffer:', msg_buffer)
			# print(msg_buffer[beg:], beg)
			end = msg_buffer[beg:].index(b'\r\n')+beg
			single_msg = msg_buffer[beg:end]
			msg_buffer = msg_buffer[end+2:]
			print('单条信息内容：',single_msg)
			# print('剩余buffer',msg_buffer)
			check_store_yanzhengma(single_msg)



def check_store_yanzhengma(msg):
	if b'+CMTI' in msg:
		print('收到新短信')
		matchObj = re.search(b'CMTI: "SM",(.*)', msg, re.M | re.I)
		msg_index = matchObj.group(1)
		print('短信序号：',msg_index)
		if ser is not None:
			result = ser.write(b"AT+CMGR="+msg_index+b"\n")
	elif b'CMGL' in msg:
		print('收到短信内容')
		matchObj = re.search(b'CMGL: .*,".*",".*","",".*"\r\n(.*)', msg, re.M | re.I)
		if matchObj is not None:
			content = matchObj.group(1)
			store_yanzhengma(content)

	elif b'CMGR' in msg:
		print('收到新短信内容')
		matchObj = re.search(b'CMGR: "REC UNREAD",".*","",".*"\r\n(.*)', msg, re.M | re.I)
		if matchObj is not None:
			content = matchObj.group(1)
			store_yanzhengma(content)


def decode(data):
	ans_str = ''
	# print(data,len(data))
	data = str.lower(data.decode('ASCII'))
	for i in range(int(len(data)/4)):
		single_hex_str = data[4*i:4*i+4]
		single_char=chr(int(single_hex_str, 16))
		ans_str += single_char
	print('解码结果:', ans_str)
	return ans_str




def store_yanzhengma(msg):
	global yanzhegnma
	print('得到短信内容：',msg)
	if len(msg)%4 == 0:
		msg = decode(msg)
		if '114' not in msg:
			return
		matchObj = re.search("码为【(.*)】", msg, re.M | re.I)
		if matchObj is not None:
			content = matchObj.group(1)
			print('当前验证码为：', content)
			yanzhegnma = content
		else:
			print('当前短信无验证码')

def get_yanzhengma():
	global yanzhegnma
	yzm = yanzhegnma
	yanzhegnma = ''
	return yzm

def get_verify_code():
	yzm = ''
	start_time = time.time()
	while yzm == '':
		yzm = get_yanzhengma()
		if time.time() - start_time > 20:
			print('获取验证码失败')
			break
	return yzm


init()
if __name__ == '__main__':
	init()


	# decode(b"6D4B8BD5")

	# decode(b'006300650073006800696D4B8BD5006300650073006800696D4B8BD5')

	# msg_buffer = b'OK\r\n\r\n+CMTI: "SM",28\r\n'
	# msg_split()
	# check_store_yanzhengma(b'+CMTI: "SM",17')
	# check_store_yanzhengma(b'+CMGL: 16,"REC READ","1069052013121","","19/12/13,13:01:24+32"\r\n30104E2D56FD79D15B66966259275B663011003C5C394E168FDC003E60A8597DFF0160A85DF26210529F98847EA6003C0032003000310039002D00310032002D00310035002000310038003A00300030003A00300030003E003C73896CC98DEF201496C168166E5600310038003A00300030FF085468672BFF09003E7EBF8DEF73ED8F663002003B')

