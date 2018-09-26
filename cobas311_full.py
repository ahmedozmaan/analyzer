import serial
import time
import json
from astm import Astm
import config 

ser = serial.Serial(port=config.COBAS_311_COMPORT,baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)


print("\n")
print("- HOST STARTED ------------------------------------------------------")
print("  COMMUNICATION PORT: " + ser.portstr)
print("---------------------------------------------------------------------")
print("\n")

astm = Astm("cobas311")
block_message = b''
answer = {}
order_response = ""
order_sent = False
sending_order = False

def checkReadLine(message):
    print("\nInstrument Send: {}".format(message))
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
        astm.cobas311Parser(message)

    time.sleep(2)
    ser.write(b'\x06')

def checkRequest():
    response = astm.checkRequest(answer)
    if response['status'] == 'ERROR':
        print("\tERROR: {}, {}".format(
            response['error_message'], response['sample_id']))
    else:
        global order_response
        order_response = response
        global sending_order
        sending_order = True
        ser.write(b'\x05')
        time.sleep(1)

def sending_reply(response):
    global answer
    # ser.write(b'\x05')
    instrument = answer.get('instrument').split('^')
    replyMessage = b"1H|\\^&|||"
    replyMessage += answer.get('host').encode() + b'^1'
    replyMessage += b"|||||" 
    replyMessage += instrument[0].encode()
    replyMessage += b"|TSDWN^REPLY|P|1\x0dP|1\x0dO|1|"
    replyMessage += answer.get('sample_id').encode()
    replyMessage += b"|" + answer.get('position').encode() + b"|"
    replyMessage += response['test_array'].encode() + b"|R||||||A||||1||||||||||O\rL|1|N\x0d\x03"

    checkSum = astm.checksum_cobas(replyMessage)
    fullMessage = b'\x02' + replyMessage + checkSum.encode() + b'\x0d\x0a'
    # time.sleep(2)
    ser.write(fullMessage)
    print(fullMessage)
    time.sleep(2)
    global order_sent 
    order_sent = True
    answer = {}
    # time.sleep(1)
    print("--EOT----------------------------------------------------------------------------------------------------")

while True:
    for c in ser.read():

        if chr(c) == '\x05':  # ENQ
            print("--ENQ FROM INSTRUMENT-----------------------------------------------------------------------------------------------")
            print("-> Reply to Instrument : ACK")
            ser.write(b'\x06')  # send ACK
            time.sleep(1)
            break
        
        if chr(c) == '\x06':
                if sending_order == True:
                    sending_reply(order_response)
                    sending_order = False
                if order_sent == True:
                    ser.write(b'\x04')
                    order_sent = False


        if chr(c) == '\x02':
            r = ser.readline()
            passdata = r
            block_message = block_message + r
            checkReadLine(passdata)
            time.sleep(2)

        if chr(c) == '\x04':
            print("\n")
            print("--END OF TRANSMISSION--------------------------------------------------------------------------------------------------\n")
            if len(answer) > 0:
                checkRequest()
                time.sleep(3)
            else: 
                astm.finaldata()
            break

ser.close()
