# coding=utf-8
import serial
import time
 
#port = "COM2"
port = '/dev/ttys004'
baud = 9600

dummy_key = 0 
dummy_messages = (
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

ser = serial.Serial(port, baud, timeout=1)
if ser.isOpen():
	print(ser.name + ' is open...')

while True:
	time.sleep(3)
	oo = ser.read()
	if oo:
		print("\nHost replied: {}".format(oo))
	
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
