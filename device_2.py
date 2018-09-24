# coding=utf-8
import serial
import time

port = '/dev/ttys002'
baud = 9600

ser = serial.Serial(port, baud, timeout=1)

def unitest():
    data = (
        b'\x02URISYS1100 URINALYSIS',
        b'\x02Seq.No.     8',
        b'\x02Pat.ID:',
        b'\x0229.08.2018         16: 16',
        b'\x02  SG    1.005',
        b'\x02  pH        5',
        b'\x02  LEU     neg',
        b'\x02  NIT     neg',
        b'\x02  PRO     neg',
        b'\x02  GLU     neg',
        b'\x02  KET     neg',
        b'\x02* UBG      1+',
        b'\x02  BIL     neg',
        b'\x02  ERY     neg'
    )
    i = 0
    while i < len(data):
        ser.write(data[i])
        time.sleep(0.3)
        i += 1

if ser.isOpen():
    print(ser.name + ' is open...')

while True:
    cmd = input("\r\nEnter command or 'exit': ")

    if cmd == 'exit':
        ser.close()
        exit()
    elif cmd == 'URYSIS':
        print("SEND URYSIS RESULT:")
        unitest()
        # ser.write(b'\x02URISYS1100 URINALYSIS')
    elif cmd == 'ENQ':
        print("Send ENQ")
        ser.write(b'\x05')
    elif cmd == 'ACK':
        print("Send ACK")
        ser.write(b'\x06')
        time.sleep(4)
    elif cmd == 'EOT':
        print("Send EOT")
        ser.write(b'\x04')
    elif cmd == 'BK1':
        msg = b'\x021H|\\^&|||cobas-e411^1|||||host|RSUPL^BATCH|P|1\rP|1\rO|1|801030-02-6026|2596^0012^2^^S1^SC|^^^117^1\\^^^900^1\\^^^880^1\\^^^136^1|R||20180730143855||||N||||1|||||||20180730152212|||F\rR|1|^^^117/1/not|317.6|IU/l||H||F||ADMIN|||E1\rC|1|I|40|I\rR|2|^^\x1744\r\n'
        ser.write(msg)
    elif cmd == 'BK2':
        msg = b'\x022^900/1/not|-1^0.750|COI||N||F||ADMIN|||E1\rR|3|^^^880/1/not|-1^0.288|COI||N||F||ADMIN|||E1\rR|4|^^^136/1/not|-1^0.128|COI||N||F||ADMIN|||E1\rL|1|N\r\x0339\r\n'
        ser.write(msg)
    elif cmd == '4BK1':
        msg = b'\x021H|\\^&|||cobas-e411^1|||||host|RSUPL^BATCH|P|1\rP|1\rO|1|880912-08-5309|3104^0001^2^^S1^SC|^^^117^1\\^^^900^1\\^^^880^1\\^^^136^1|R||20180821095503||||N||||1|||||||20180821104134|||F\rR|1|^^^117/1/not|<2.00|IU/l||LL||F||ADMIN|||E1\rC|1|I|27|I\rR|2|^\x173F\r\n'
        ser.write(msg)
    elif cmd == '4BK2':
        msg = b'\x022^^900/1/not|-1^0.567|COI||N||F||ADMIN|||E1\rR|3|^^^880/1/not|-1^0.313|COI||N||F||ADMIN|||E1\rR|4|^^^136/1/not|-1^0.127|COI||N||F||ADMIN|||E1\rL|1|N\r\x0391\r\n'
        ser.write(msg)
    elif cmd == 'RT411':
        msg = b'\x021H|\\^&|||cobas-e411^1|||||host|TSREQ^REAL|P|1\x0dQ|1|^^91101800034^3668^@8^1^^S1^SC||ALL||||||||O\x0dL|1|N\x0d\x0a'
        ser.write(msg)
    elif cmd == 'RT311':
        sendMessage = b'\x021H|\\^&|||H7600^1|||||host|TSREQ^REAL|P|1\x0dQ|1|^^           91101800034^3^50002^002^^S1^SC||ALL||||||||O\x0dL|1|N\x0d76\x0d\x0a'
        ser.write(sendMessage)
    else:
        print("No Command")
        # sendMessage = b'\x021H|\\^&|||H7600^1|||||host|TSREQ^REAL|P|1\x0dQ|1|^^91101800034^3^50002^002^^S1^SC||ALL||||||||O\x0dL|1|N\x0d76\x0d\x0a'
        # ser.write(sendMessage)
        # out = ser.read()
        # print('Receiving...'+ out.decode("utf-8"))

    time.sleep(2)
    oo = ser.readline()
    print("Replied: {}".format(oo))
