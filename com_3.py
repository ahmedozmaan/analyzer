import serial
 
port = "COM3"
baud = 9600
 
ser = serial.Serial(port, baud, timeout=1)
# open the serial port
if ser.isOpen():
	print(ser.name + ' is open...')
	#ser.write(b'\x05')
	full_stx = b'\x02' + b"1H||||||||||SETS^KJAYS^^" + b'\x03'
	ser.write(full_stx)
 
while True:
	oo = ser.read()
	print("Host send: " + oo.decode())
	cmd = input("Enter command or 'exit':")
	if cmd == 'exit':
		ser.close()
		exit()
	else:
		ser.write(cmd.encode('ascii') + b'\r\n')
		out = ser.read()
		print('Receiving...'+ out.decode("utf-8"))