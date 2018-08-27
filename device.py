# coding=utf-8
import serial
import time
 
port = "COM2"
baud = 9600

dummy_key = 0 
dummy_messages = (
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

ser = serial.Serial(port, baud, timeout=1)
# open the serial port
if ser.isOpen():
	print(ser.name + ' is open...')

while True:
	time.sleep(3)
	oo = ser.read()
	if oo:
		print("\nHost replied: {}".format(oo.decode()))
		
	if oo == b'\x06':
		dummy_key = dummy_key + 1
		if dummy_key < len(dummy_messages):
			print("\tSending Message {} : {}".format(dummy_key, dummy_messages[dummy_key].decode()[1:-6]))	
			cmd = 'step'
		else:
			print("End of dummy message")
			dummy_key = 0
			cmd = input("\r\nEnter command or 'exit': ")
	else:
		cmd = input("\r\nEnter command or 'exit': ")
	
	if cmd == 'exit':
		ser.close()
		exit()
	if cmd == 'eot':
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
		#ser.write(cmd.encode('ascii'))
		ser.write(sendMessage)
		out = ser.read()
		print('Receiving...'+ out.decode("utf-8"))
