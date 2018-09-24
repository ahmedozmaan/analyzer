import serial
import time
from astm import Astm

# ser = serial.Serial(port='/dev/ttys006',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)
ser = serial.Serial(port='/dev/cu.wchusbserial1410',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

reply_processing = False
reply_message = ""

def printMsg():
	return True
	
print("connected to: " + ser.portstr)
print("\n")

astm = Astm("cobas411")

block_message = b''

def checkReadLine(message):
	print("\nDevice Send: {}".format(message))
	# astm.deviceSend(message)
	astm.cobas311Parser(message)
	# time.sleep(2)
	ser.write(b'\x06')

def checkRequest():
	print('check if any request is required')
	# response = astm.checkRequest()
	# print(response)
	# time.sleep(1)
	sending_reply("ok")

def reply_order():
	ser.write(b'\x05')
	time.sleep(3)
	message = b"\x02H|\\^&|||host^1|||||cobas-e411^1|TSDWN^REPLY|P|1\rP|1\rO|1|^^   ^3^50002^002^^S1^SC|^^^150^\\^^^140^||ALL||||||||O\rL|1|N\r\n"
	ser.write(message)

def sending_reply(response):
	ser.write(b'\x05')
	time.sleep(3)
	print("Send Reply from instrument inquiry")
	reply = b"\x021H|\\^&|||host^1|||||cobas-e411|TSDWN^REPLY|P|1\x0dP|1\x0dO|1|91101800034|3668^@8^1^^S1^SC|^^^150^\\^^^140^|R||||||A||||1||||||||||O\rL|1|N\x0d\x0359\x0d\x0a"
	print("SEND ORDER TO INSTRUMENT: {}".format(reply))
	
	ser.write(reply)
	time.sleep(2)
	ser.write(b'\x04')
	time.sleep(2)

while True:
	for c in ser.read():
		# if chr(c) == '\x06':
		# 	print("proses next: {}".format(reply_processing))
		# 	# sending_reply
		# 	break
		
		if chr(c) == '\x05': 							#ENQ
			print("\n----------------------------------------------------------------------------------------------------")
			print("Device ask for handshake")
			print("Reply to Device : ACK\n")
			ser.write(b'\x06')							#send ACK
			time.sleep(1)
			break
	
		if chr(c) == '\x04':
			print("\nEnd Of Transmission")
			print("----------------------------------------------------------------------------------------------------\n")
			
			checkRequest()
			
			astm.finaldata()
			break
		
		if chr(c) == '\x02':
			r = ser.readline()
			passdata = r
			# time.sleep(5)
			block_message = block_message + r
			checkReadLine(passdata)
			time.sleep(3)
ser.close()