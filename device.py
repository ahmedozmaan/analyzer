# coding=utf-8
import serial
import time
 
#port = "COM2"
port = '/dev/ttys002'
baud = 9600

dummy_key = 0 
waiting = False

def message_sample(sample):
	if sample == "urisys1100":
		data = (
			b'\x05',
			b'\x02'+ "1H|\^&|||URISYS1100^99305^SW5.31^INT|||||||P||20090116184200".encode() + b'\x13'  + b'\x03' + b"F8" + b'\x13'  + b'\x10' ,
			b'\x02'+ "2P|1".encode() + b'\x13'  + b'\x03' +b"3F" + b'\x13'  + b'\x10' ,
			b'\x02'+ "3O|1||001^00036^C10|Urinalysis^Incubated|R||||||X|||20090116184100".encode() + b'\x13'  + b'\x03' + b"00" + b'\x13' + b'\x10' ,
			b'\x02'+ "4R|01|01^·SG|1.020|gcm3|||||20090116|LNorman^A".encode() + b'\x13' + b'\x03' + b"BB" + b'\x13' + b'\x10' ,
			b'\x02'+ "5R|02|02^·pH|····7||||||20090116|LNorman^A".encode() + b'\x13'  + b'\x03' + b"09" + b'\x13'  + b'\x10' ,
			b'\x02'+ "6R|03|03^LEU|··neg^··neg|·Leu/ul|||||20090116|LNorman^A".encode() + b'\x13'  + b'\x03' + b"0B" + b'\x13'  + b'\x10' ,
			b'\x02'+ "7R|04|04^NIT|··neg^··neg||||||20090116|LNorman^A".encode() + b'\x13'  + b'\x03' + b"BD" + b'\x13'  + b'\x10' ,
			b'\x02'+ "0R|05|05^PRO|··neg^··neg|·mg/dl·|||||20090116|LNorman^A".encode() + b'\x13'  + b'\x03' + b"D1" + b'\x13'  + b'\x10' ,
			b'\x02'+ "1R|06|06^GLU|·norm^··neg|·mg/dl·|||||20090116|LNorman^A".encode() + b'\x13'  + b'\x03' + b"2D" + b'\x13'  + b'\x10' ,
			b'\x02'+ "2R|07|07^KET|··neg^··neg|·mg/dl·|||||20090116|LNorman^A".encode() + b'\x13'  + b'\x03' + b"CA" + b'\x13'  + b'\x10' ,
			b'\x02'+ "3R|08|08^UBG|·norm^··neg|·mg/dl·|||||20090116|LNorman^A".encode() + b'\x13'  + b'\x03' + b"29" + b'\x13'  + b'\x10' ,
			b'\x02'+ "4R|09|09^BIL|··neg^··neg|·mg/dl·|||||20090116|LNorman^A".encode() + b'\x13'  + b'\x03' + b"C3" + b'\x13'  + b'\x10' ,
			b'\x02'+ "5R|10|10^ERY|···50^···3+|·Ery/ul|||||20090116|LNorman^A".encode() + b'\x13'  + b'\x03' + b"A9" + b'\x13'  + b'\x10' ,
			b'\x02'+ "6C|10|I|*|I".encode() + b'\x13'  + b'\x03' + b"96" + b'\x13'  + b'\x10',
			b'\x02'+ "7L|1|N".encode() + b'\x13'  + b'\x03' + b"0A" + b'\x13'  + b'\x10' ,
			b'\x04',
		)
	if sample == "cobas411":
		data = (
			b'\x05',
			b'\x02' + "1H|\^&|||cobas·u·411^8^3.2.0.1001^Int|||||||P||20110315101822".encode() + b'\x13' + b'\x03' + b"71" + b'\x13' + b'\x10',
			b'\x02' + "2P|1".encode() + b'\x13' + b'\x03' + b"3F" + b'\x13' + b'\x10',
			b'\x02' + "3O|1|001|1^^^^SAMPLE||R||||||X|||20110315101754".encode() + b'\x13' + b'\x03' + b"F0" + b'\x13' + b'\x10',
			b'\x02' + "4R|1|1^SG|1.005|||||||service".encode() + b'\x13' + b'\x03' + b"AD" + b'\x13' + b'\x10',
			b'\x02' + "5R|2|2^pH|7|||||||service".encode() + b'\x13' + b'\x03' + b"11" + b'\x13' + b'\x10',
			b'\x02' + "6R|3|3^LEU|neg|||||||service".encode() + b'\x13' + b'\x03' + b"45" + b'\x13' + b'\x10',
			b'\x02' + "7R|4|4^NIT|neg|||||||service".encode() + b'\x13' + b'\x03' + b"4D" + b'\x13' + b'\x10',
			b'\x02' + "0R|5|5^PRO|neg|||||||service".encode() + b'\x13' + b'\x03' + b"4E" + b'\x13' + b'\x10',
			b'\x02' + "1R|6|6^GLU|neg|||||||service".encode() + b'\x13' + b'\x03' + b"48" + b'\x13' + b'\x10',
			b'\x02' + "2R|7|7^KET|neg|||||||service".encode() + b'\x13' + b'\x03' + b"47" + b'\x13' + b'\x10',
			b'\x02' + "3R|8|8^UBG|neg|||||||service".encode() + b'\x13' + b'\x03' + b"44" + b'\x13' + b'\x10',
			b'\x02' + "4R|9|9^BIL|neg|||||||service".encode() + b'\x13' + b'\x03' + b"40" + b'\x13' + b'\x10',
			b'\x02' + "5R|10|10^ERY|neg|||||||service".encode() + b'\x13' + b'\x03' + b"AA" + b'\x13' + b'\x10',
			b'\x02' + "6R|11|11^COL|p.yel|||||||service".encode() + b'\x13' + b'\x03' + b"49" + b'\x13' + b'\x10',
			b'\x02' + "7R|12|12^CLA||||||||service".encode() + b'\x13' + b'\x03' + b"56" + b'\x13' + b'\x10',
			b'\x02' + "0M|1|RC|||2001601|20111001|||".encode() + b'\x13' + b'\x03' + b"8F" + b'\x13' + b'\x10',
			b'\x02' + "1L|1|N".encode() + b'\x13' + b'\x03' + b"04" + b'\x13' + b'\x10',
			b'\x04'
		)
	if sample == "cobas311":
		data = (
			b'\x05',
			b'\x02' + "1H|\^&|||cobas u 311^1|||||||P||20110315101822".encode() + b'\x13' + b'\x03' + b"7" + b"1" + b'\x13' + b'\x10',
			b'\x02' + "2P|1".encode() + b'\x13' + b'\x03' + b"71" + b'\x13' + b'\x10',
			b'\x02' + "3O|000010|442^50001^001^^S1^SC|^^^672^|R||||||N||||1|||||||20051220104418|||F".encode() + b'\x13' + b'\x03' + b"7" + b"1" + b'\x13' + b'\x10',
			b'\x02' + "4R|1|^^^400/|-1^0.303|umol/l||N||F||admin|||P1".encode() + b'\x13' + b'\x03' + b"7" + b"1" + b'\x13' + b'\x10',
			b'\x02' + "5C|1|I|45|I".encode() + b'\x13' + b'\x03' + b"7" + b"1" + b'\x13' + b'\x10',
			b'\x02' + "6L|1|N".encode() + b'\x13' + b'\x03' + b"7" + b"1" + b'\x13' + b'\x10',
			b'\x04'
		)
	if sample == "cobas311_realtime":
		data = (
			b'\x05',
			b'\x02' + "1H|\^&|||cobas u 311^1|||||host|TSREQ^REAL|P|1".encode() + b'\x13' + b'\x03' + b"6" + b"A" + b'\x13' + b'\x10',
			b'\x02' + "2Q|1|^^00002^3^50002^002^^S1^SC||ALL||||||||O".encode() + b'\x03' + b"7" + b"4" + b'\x13' + b'\x10',
			b'\x02' + "3L|1|N".encode() + b'\x13' + b'\x03' + b"0" + b"6" + b'\x13' + b'\x10',
			b'\x04'
		)
	if sample == "cobas311_sendresult":
		data = (
			b'\x05',
			# b'\x02' + b'1H|\\^&|||H7600^1|||||host|RSUPL^BATCH|P|1\rP|1|||||||U||||||^\rO|1|PCCC2                 |4030^30064^064^^QC^SC|^^^798^\\^^^435^\\^^^717^\\^^^552^\\^^^781^|||||||Q||||1|||||||20180702152234|||F\rC|1|I|^^^^|G\rR|1|^^^798/|4.60|mmol/l||A||||ADMIN |||P\x17E0\r\n',
    		# b'\x02' + b'21\rC|1|I|101|I\rR|2|^^^435/|1.55|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rR|3|^^^717/|13.12|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rR|4|^^^552/|2.42|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rR|5|^^^781/|2.35|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rL|1|N\r\x03A5\r\n',
			b'\x02' + b'1H|\\^&|||H7600^1|||||host|RSUPL^BATCH|P|1\rP|1|||||||U||||||^\rO|1|PCCC2                 |4030^30064^064^^QC^SC|^^^798^\\^^^435^\\^^^717^\\^^^552^\\^^^781^|||||||Q||||1|||||||20180702152234|||F\rC|1|I|^^^^|G\rR|1|^^^798/|4.60|mmol/l||A||||ADMIN |||P\x17E0\r\n',
			b'\x02' + b'21\rC|1|I|101|I\rR|2|^^^435/|1.55|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rR|3|^^^717/|13.12|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rR|4|^^^552/|2.42|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rR|5|^^^781/|2.35|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rL|1|N\r\x03A5\r\n',
			b'\x04'
		)
	return data

# sampling = "urisys1100"
# dummy_messages = message_sample(sampling)

ser = serial.Serial(port, baud, timeout=1)
# open the serial port
def commandMessage():
	if waiting == False:
		print("\nInstruction:")
		print("\t type 'cobas411' for cobas 411 sample data")
		print("\t type 'cobas311' for cobas 311 sample data")
		print("\t type 'cobas311_realtime' for cobas 311 Test Selection Information in realtime sample data")
		print("\t type 'urisys1100' for urisys sample data")
		print("\t type 'cobas311_sendresult' for cobas311 send result from device")

if ser.isOpen():
	print(ser.name + ' is open...')
	commandMessage()

while True:
	time.sleep(2)
	oo = ser.read()
	
	if oo:
		print("----------------------------------------------------------------------------------------------------")
		print("Host replied: {}".format(oo))
	
	if oo == b'\x05':
		ser.write(b'\x06')
		print("\tDevice Replied : ACK")
	
	if oo == b'\x06':
		dummy_key = dummy_key + 1
		if dummy_key < len(dummy_messages):
			print("\tSending Message {} : {}".format(dummy_key, dummy_messages[dummy_key].decode()[1:-6]))	
			cmd = 'step'
		else:
			print("End of dummy message")
			dummy_key = 0
			commandMessage()
			# waiting = True
			print("\nDevice in waiting a response from host...")
			cmd = input("\r\nEnter command or 'exit': ")
	else:
		cmd = input("\r\nEnter command or 'exit': ")
	
	if cmd == 'exit':
		ser.close()
		exit()
	elif cmd == "cobas311_sendresult":
		dummy_messages = message_sample(cmd)
		print("\n\nUsing Cobas 311 send data from device")
		ser.write(dummy_messages[dummy_key])
	elif cmd == "cobas311":
		dummy_messages = message_sample("cobas311")
		print("\n\nUsing Cobas 311 sampling data")
		ser.write(dummy_messages[dummy_key])
	elif cmd == "cobas311_realtime":
		dummy_messages = message_sample("cobas311_realtime")
		print("\n\nUsing Cobas 311 Test Selection RealTime sampling data")
		print("Expecting Replies from host...")
		ser.write(dummy_messages[dummy_key])
	elif cmd == "cobas411":
		dummy_messages = message_sample("cobas411")
		print("\n\nUsing Cobas 411 sampling data")
		ser.write(dummy_messages[dummy_key])
	elif cmd == "urisys1100":
		dummy_messages = message_sample("urisys1100")
		print("\n\nUsing Urisys1100 sampling data")
		ser.write(dummy_messages[dummy_key])
	elif cmd == 'enq':
		print("Enq....")
		ser.write(dummy_messages[0])
	elif cmd == 'H':
		print("Header....")
		ser.write(dummy_messages[1])
	elif cmd == 'eot':
		print("Send EOT")
		ser.write(b'\x04')
	elif cmd == 'step':
		ser.write(dummy_messages[dummy_key])
	elif cmd == 'loop':
		num = 0
		while num < len(dummy_messages):
			ser.write(dummy_messages[num])
			time.sleep(1)
			num = num + ser.write(sample)
	else:
		sendMessage = b'\x02' + cmd.encode('ascii') + b'\x10'
		ser.write(sendMessage)
		out = ser.read()
		print('Receiving...'+ out.decode("utf-8"))
		
