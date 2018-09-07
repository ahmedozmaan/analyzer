import serial
import time
from astm import Astm

ser = serial.Serial(port='/dev/ttys003',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

reply_processing = False
reply_message = ""

def printMsg():
	return true
	
print("connected to: " + ser.portstr)
print("\n")

astm = Astm("cobas311")

def checkReadLine(message):
	print("\nDevice Send: {}".format(message))
	astm.deviceSend(message)
	time.sleep(1)
	ser.write(b'\x06')

def checkRequest():
	print('check if any request is required')
	# response = astm.checkRequest()
	# print(response)
	# time.sleep(1)
	# sending_reply(response[0])
	print("SKIPPED")

def sending_reply(response):
	print("Response: {}".format(response))
	i = 0
	message = (
		b'\x05',
		b'\x02' + "1H|\^&|||host^1|||||cobas c 311|TSDWN^REPLY|P|1".encode() + b'\x13' + b'\x03' + b"C" + b"1" + b'\x13' + b'\x10' ,
		b'\x02' + "2P|1".encode() + b'\x13' + b'\x03' + b"3" + b"F" + b'\x13' + b'\x10',
		b'\x02' + "3O|1|000002|3^50002^002^^S1^SC|^^^10^|R|||||||A||||1|||||||||||O".encode() + b'\x13' + b'\x03' + b"9" b"1" + b'\x13' + b'\x10',
		b'\x02' + "4L|1|N".encode() + b'\x13' + b'\x03' + b"0" + b"7" + b'\x13' + b'\x10'
	)
	ser.write(message[0])
	while i < len(message):
		ser.write(message[i])
		i = i+1
		time.sleep(1)
		print("Send Message {}: {}".format(i, message[0]))

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
			break
	
		if chr(c) == '\x04':
			print("\nEnd Of Transmission")
			print("----------------------------------------------------------------------------------------------------\n")
			ser.write(b'\x06')
			checkRequest()
			break
		
		if chr(c) == '\x02':
			r = ser.readline()
			passdata = b'\x02' + r
			checkReadLine(passdata)
ser.close()