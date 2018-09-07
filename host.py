import serial
import time
from astm import Astm

# ser = serial.Serial(
#     port='COM1',\
#     baudrate=9600,\
#     parity=serial.PARITY_NONE,\
#     stopbits=serial.STOPBITS_ONE,\
#     bytesize=serial.EIGHTBITS,\
#         timeout=0)

ser = serial.Serial(port='/dev/ttys006',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)
# ser = serial.Serial(port='/dev/cu.wchusbserial1410',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)
		
def printMsg():
	return true
	
print("connected to: " + ser.portstr)
print("\n")
count=1

seq = []

astm = Astm("cobas411")
# astm = Astm("urisys1100")

def checkMessage(message):
	data = message.encode()
	stx = data.find(b'\x02')
	etx = data.find(b'\x03')
	lf = data.find(b'\x10')
	cr = data.find(b'\x13')
	crlf = lf + cr
	text =  message[1:-6]
	checksum = message[-4:-2]
	print("\n----------------------------------------------------------------------------------------------------")
	print("From device:")
	#print("\tRaw Message : {}".format(data))
	print("\tMessage : {}".format(text))
	print("\tChecksum : {}".format(checksum))
	astm.deviceSend(data)
	time.sleep(1)
	ser.write(b'\x06')

def checkRequest():
	print('check if any request is required')
	time.sleep(1)
	print("check completed")

while True:
	time.sleep(1)
	for c in ser.read():
		print(c)
		if chr(c) == '\x05': 							#ENQ
			print("\n----------------------------------------------------------------------------------------------------")
			print("Device ask for handshake")
			print("Reply to Device : ACK\n")
			ser.write(b'\x06')							#send ACK
			break
		
		if chr(c) == '\x04':
			print("\nEnd Of Transmission")
			print("-------------------\n")
			ser.write(b'\x06')
			checkRequest()
			break
		
		if chr(c) == '\x02':
			r = ser.readline()
			print("Sending: {}".format(r))
			ser.write(b'\x02' + r)
			break
		else:
			seq.append(chr(c))
			joined_seq = ''.join(str(v) for v in seq)
			if chr(c) == '\x10':						# if message ending with LF
				seq = []
				count += 1
				checkMessage(joined_seq)
				break
ser.close()