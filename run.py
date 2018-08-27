import serial
import time

ENQ = b'\x05'
ACK = b'\x06'
STX = b'\x02'
EOT = b'\x05'

with serial.Serial('comport',9600,timeout=1) as ser:
    while True:
        control_character = ser.read() #read first bit
        print("Device Send: {}".format(control_character))
        reply = ""
        if control_character == ENQ:    
            ser.write(ACK)

        if control_character == STX:
            received = ser.readline()
            
            ser.write(ACK)
        
        if control_character == EOT
            ser.write(ACK)


