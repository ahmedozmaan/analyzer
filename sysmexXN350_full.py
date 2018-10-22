import serial
import time
import json
from astm import Astm
import config

#ser = serial.Serial(port='/dev/ttys006', baudrate=9600, parity=serial.PARITY_NONE,
#                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)
ser = serial.Serial(port= config.SYSMEX_XN_350_COMPORT ,baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

print("\n")
print("-| HOST STARTED |----------------------------------------------------")
print("   COMMUNICATION PORT: " + ser.portstr)
print("---------------------------------------------------------------------")
print("\n")

astm = Astm("sysXn350")
block_message = b''
answer = {}
count = 0

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
                "ASTMversion": firstHeader[12],
                "sample_id": query[2].strip(),
                "position": hs[2],
                'datetest': hs[6]
            }
        h = h + 1
    if len(answer) == 0:
        astm.sysXn350Parser(message)

    time.sleep(2)
    print("  HOST       : ACK")
    ser.write(b'\x06')


def checkRequest():
    if answer:
        response = astm.checkRequest(answer)
        if response['status'] == 'ERROR':
            print("  HOST       : {}, {}".format(response['error_message'], response['sample_id']))
        else:
            sending_reply()
    else:
        astm.finaldata()


def sending_reply():
      global answer
      if len(answer) > 0:
          print("  HOST       : ENQ")   
          ser.write(b'\x05')
          time.sleep(2)

def host_send(count):          
      i = count
      global answer
    
      param = b'|^^^^WBC\\^^^^RBC\\^^^^HGB\\^^^^HCT\\^^^^MCV\\^^^^MCH\\^^^^MCHC\\^^^^PLT\\^^^^NEUT%\\^^^^LYMPH%\\^^^^MONO%\\^^^^EO%\\^^^^BASO%\\^^^^RDW-CV\\^^^^MPV|'
      #ordermsg = b'4O|1|' + answer.get('position').encode() + '|' + response['test_array'].encode() + answer.get('datetest').encode() + b'|||||N||||||||||||||Q||||||\r\x03'
    
      ordermsg = b'4O|1|' + answer.get('position').encode() + param + answer.get('datetest').encode() + b'|||||N||||||||||||||Q||||||\r\x03'
      recordinfo  = (   b'1H|\\^&|||||||||||E1394-97\r\x03',
                        b'2P|1||||^^||||||||^||||||||||||^^^\r\x03',
                        b'3C|1||\r\x03',
                        ordermsg,
                        b'5C|1||\r\x03',
                        b'6L|1|N\r\x03')
      if i < 6:
          replyMessage = recordinfo[i]
          checkSum = astm.checksum_cobas(replyMessage)
          fullMessage = b'\x02' + replyMessage + checkSum.encode() + b'\x0d\x0a'
          ser.write(fullMessage)
          print(fullMessage)
          time.sleep(1)
      if i == 6:
          #ser.write(b'\x04')
          #print("  HOST       : EOT")
          #print("--EOT----------------------------------------------------------------")
          answer = {}
 
while True:
    for c in ser.read():
        #print (c)
        if chr(c) == '\x05':  # ENQ
            print('\n')
            print("  INSTRUMENT : ENQ")
            print("  HOST       : ACK")
            ser.write(b'\x06')  # send ACK
            time.sleep(1)
            break

        if chr(c) == '\x02':
            r = ser.readline()
            checkReadLine(r)
            time.sleep(1)

        if chr(c) == '\x06':
            print("  INSTRUMENT : ACK")
            host_send(count)
            if len(answer) > 0:
                  count += 1
            else:
                  ser.write(b'\x04')
                  count = 0
                  print("  HOST       : EOT")
                  print("--EOT----------------------------------------------------------------")
            time.sleep(1)
            
        if chr(c) == '\x04':
            print("  INSTRUMENT : EOT")
            if len(answer) > 0:
                checkRequest()
                time.sleep(1)
            else:
                astm.finaldata()
            break

ser.close()
