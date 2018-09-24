import serial
import time
import json
from astm import Astm
import config

#ser = serial.Serial(port='/dev/ttys006', baudrate=9600, parity=serial.PARITY_NONE,
#                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)
ser = serial.Serial(port= config.COBAS_411_COMPORT ,baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

print("\n")
print("-| HOST STARTED |----------------------------------------------------")
print("   COMMUNICATION PORT: " + ser.portstr)
print("---------------------------------------------------------------------")
print("\n")

astm = Astm("cobas411")
block_message = b''
answer = {}

def checkReadLine(message):
    print("  INSTRUMENT : {}".format(message))
    header = message.split(b'\x0d')
    h = 0
    while h < len(header):
        hs = header[h].decode().split('|')
        if hs[0][-1] == 'Q':
            firstHeader = header[0].decode().split('|')
            query = hs[2].split('^')
            global answer
            answer = {
                "instrument": firstHeader[4],
                "host": firstHeader[9],
                "sample_id": query[2],
                "position": query[3] + '^' + query[4] + '^' + query[5] + '^^S1^SC'
            }
        h = h + 1
    if len(answer) == 0:
        astm.cobas411Parser(message)

    time.sleep(2)
    print("  HOST       : ACK")
    ser.write(b'\x06')


def checkRequest():
    if answer:
        response = astm.checkRequest(answer)
        if response['status'] == 'ERROR':
            print("  HOST       : {}, {}".format(response['error_message'], response['sample_id']))
        else:
            sending_reply(response)
    else:
        astm.finaldata()

def sending_reply(response):
    global answer
    ser.write(b'\x05')
    instrument = answer.get('instrument').split('^')
    replyMessage = b"1H|\\^&|||"
    replyMessage += answer.get('host').encode() + b'^1'
    replyMessage += b"|||||"
    replyMessage += instrument[0].encode()
    replyMessage += b"|TSDWN^REPLY|P|1\x0dP|1\x0dO|1|"
    replyMessage += answer.get('sample_id').encode()
    replyMessage += b"|" + answer.get('position').encode() + b"|"
    replyMessage += response['test_array'].encode() + \
        b"|R||||||A||||1||||||||||O\rL|1|N\x0d\x03"

    checkSum = astm.checksum_cobas(replyMessage)
    fullMessage = b'\x02' + replyMessage + checkSum.encode() + b'\x0d\x0a'
    time.sleep(3)
    ser.write(fullMessage)
    print(fullMessage)
    time.sleep(2)
    ser.write(b'\x04')
    answer = {}
    time.sleep(1)
    print("--EOT----------------------------------------------------------------")

while True:
    for c in ser.read():

        if chr(c) == '\x05':  # ENQ
            print('\n')
            print("  INSTRUMENT : ENQ")
            print("  HOST       : ACK")
            ser.write(b'\x06')  # send ACK
            time.sleep(1)
            break

        if chr(c) == '\x02':
            r = ser.readline()
            passdata = r
            block_message = block_message + r
            checkReadLine(passdata)
            time.sleep(3)

        if chr(c) == '\x04':
            print("  INSTRUMENT : EOT")
            if len(answer) > 0:
                checkRequest()
                time.sleep(3)
            else:
                astm.finaldata()
            break

ser.close()
