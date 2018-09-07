# coding=utf-8
import serial
import time
 
#port = "COM2"
# port = '/dev/ttys005'
port = '/dev/cu.wchusbserial1410'
baud = 9600

dummy_key = 0 
waiting = False

data = (
	b'\x05',
	b"\x021H|\\^&|||host^1|||||H7600|RSREQ^BATCH|P|1\x0drQ|1|^^     2* RCPA  (109-04)0^50031^031^^S1^SC||ALL||||||||F\x0dL|1|N\x0d11\x0d\x0a",
	b'\x04'
)

dummy_messages = ""
est = 0

ser = serial.Serial(port, baud, timeout=2)
# open the serial port
def commandMessage():
	if waiting == False:
		print("\nInstruction:")
		print("\t type 'cobas311_inquiry' for cobas311 send inquiry")

if ser.isOpen():
	print(ser.name + ' is open...')
	print("\nSending Inquiry.... ENQ")
	ser.write(b'\x05')

current_loop = 1
est = 0

while True:
	oo = ser.read()
	print("Check {}".format(oo))
	if oo != b'':
		if oo == b'\x06':
			time.sleep(2)
			print("Current Loop: {}".format(current_loop))
			if est == 0:
				print("Send Queries")
				print("Loop: {} Data: {}".format(current_loop, data[current_loop]))
				ser.write(data[current_loop])
				current_loop += 1
				est = 1
			if current_loop == len(data):
				print("Finised")
			
			if current_loop == 2:
				ser.write(b'\x04')
			
		if oo == b'\x02':
			r = ser.readline()
			print("Response From Instrument: {}".format(r))
			print("----------------------------------------------------------------\n")
			print("Loop: {} Data: {}".format(current_loop, data[current_loop]))
			if current_loop < len(data):
				print("Send To Instrument: {}".format(data[current_loop]))
				ser.write(data[current_loop])
			else:
				print("finished")
			current_loop += 1
			print("----------------------------------------------------------------\n")

			#checksum function skipped

			# if current_loop == 2:
			# 	r = ser.readline()
			# 	print("Second Loop : {}".format(r))
			# 	if current_loop < len(data):
			# 		print("\tSending... : {}".format(data[current_loop]))
			# 		ser.write(data[current_loop])
			# 	else:
			# 		print("End")

			
	
