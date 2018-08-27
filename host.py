import serial
import time

ser = serial.Serial(
    port='COM1',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

		
def printMsg():
	return true
	
print("connected to: " + ser.portstr)
print("\n")
count=1

STX = 2
ENQ = 5

seq = []

def checkMessage(message):
	data = message.encode()
	stx = data.find(b'\x02')
	etx = data.find(b'\x03')
	lf = data.find(b'\x10')
	cr = data.find(b'\x13')
	crlf = lf + cr
	text =  message[stx+1:-6]
	checksum = message[-4:-2]
	print("Raw Message : {}".format(data))
	print("Clear Message : {}".format(text))
	print("Checksum : {}".format(checksum))
	print("-------------\n")
	time.sleep(1)
	ser.write(b'\x06')
	print("Send ACK\n")

while True:
	for c in ser.read():
		if chr(c) == '\x05':
			print("Host inquiry")
			print("---------------\n")
			ser.write(b'\x06')
		if chr(c) == '\x04':
			print("End Of Transmission")
			print("---------------\n")
			ser.write(b'\x06')
			break
		else:
			seq.append(chr(c))
			joined_seq = ''.join(str(v) for v in seq)
		
			if chr(c) == '\x10':
				#print("Line " + str(count) + ': ' + joined_seq)
				seq = []
				count += 1
				checkMessage(joined_seq)
				
				break
ser.close()