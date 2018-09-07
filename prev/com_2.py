import serial

ser = serial.Serial(
    port='COM2',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)
count=1


STX = 2
ENQ = 5

while True:
	for line in ser.read():
		print("output: {}".format(str(line)))
		if line == ENQ:
			print("Device sent: {}".format(ENQ))
			ser.write(b'\x06')
			
		if line == STX:
			ser.write(6)
			print("ngantor STX")
		print(str(count) + str(': ') + chr(line) )
		count = count+1

ser.close()