import serial
import time
from astm import Astm
import config
import os
import requests
import json

from os import system
system("title SYSMEX KX 21")

ser = serial.Serial(port=config.SYSMEX_KX21_COMPORT, baudrate=9600, timeout=1)

#test parameter list
list_param = ['WBC  :', 'RBC  :','HGB  :', 'HCT  :','MCV  :', 'MCH  :','MCHC :', 'PLT  :','LYM% :','MXD% :',
              'NEUT%:','LYM# :', 'MXD# :','NEUT#:', 'RDW  :','PDW  :', 'MPV  :','P-LCR:']
label = ['Device Name: ','Test Date  : ','Sample Id  : ']

#----------------------------------------------------------------------------------------
#result = xxxxF, 5th = F = Flag [-/+/etc]
def checkResultFlag (arg1):
    resultFlag = []
    for i in range(0,len(arg1)):
      flagbit = '-' 
      if arg1[i][-1] == '0':
            flagbit = ' '
      if arg1[i][-1] == '1':
            flagbit = '+'
      if arg1[i][-1] == '2':
            flagbit = '-'
      if arg1[i] == '*0':
            flagbit = '-' 
      resultFlag.append(str(flagbit))
    #print (resultFlag)
    return resultFlag


#raw result to readable form
def cleanresult(arg1):
    arg1 = [x[:-1] for x in arg1]
    
    for i in range(0,len(arg1)):
        if arg1[i] != '*000':
            arg1[i] = int(arg1[i])/10
        else:
            arg1[i] = '0.00'

    if arg1[1] != '0.00':
          arg1[1] = round((arg1[1]/10),2)
    if arg1[7] != '0.00':
          arg1[7] = arg1[7]*10            
    return arg1
    

def handleresult(msg):
    
    result = {}
    list_flag = []
    value = []
    rawresult = msg[29:]
    rawresult = [rawresult[i:i+5] for i in range(0, len(rawresult), 5)]
    
    #date
    get_date = [msg[3:9][i:i+2] for i in range(0, len(msg[3:9]), 2)]
    get_testdate = '/'.join(get_date[::-1])
    
    #check result flag
    flagging = checkResultFlag (rawresult)
                        
    #get result
    value = cleanresult(rawresult)
                        
    #print to screen   
    list_of_results = [list_param,flagging,value]
    for a in zip(*list_of_results):
            print(*a)
        
    print ('\n') 

    testdata = {
		    "device_name": 'Sysmex KX21',
		    "patient_id": msg[14:22],
		    "test_date": get_testdate,
		    "result": {
				"WBC": {'value': value[0],"flag" : flagging[0]},                                                  
                                "RBC": {'value': value[1],"flag" : flagging[1]},
                                "HGB": {'value': value[2],"flag" : flagging[2]}, 
                                "HCT": {'value': value[3],"flag" : flagging[3]}, 
                                "MCV": {'value': value[4],"flag" : flagging[4]}, 
                                "MCH": {'value': value[5],"flag" : flagging[5]}, 
                                "MCHC": {'value': value[6],"flag" : flagging[6]},
                                "PLT": {'value': value[7],"flag" : flagging[7]}, 
                                "LYM%": {'value': value[8],"flag" : flagging[8]}, 
                                "MXD#": {'value': value[9],"flag" : flagging[9]}, 
                                "LYM#": {'value': value[10],"flag" : flagging[10]}, 
                                "MXD#": {'value': value[11],"flag" : flagging[11]}, 
                                "NEUT#": {'value': value[12],"flag" : flagging[12]}, 
                                "RDW": {'value': value[13],"flag" : flagging[13]}, 
                                "PDW": {'value': value[14],"flag" : flagging[14]}, 
                                "MPV:": {'value': value[15],"flag" : flagging[15]},
                                "P-LCR:": {'value': value[16],"flag" : flagging[16]}, 
                            }   
		    }                     
                           
    return testdata

#serial start
#--------------------------------------------------------------------------------------------

print("\n")
print("- HOST STARTED ------------------------------------------------------")
print("  COMMUNICATION PORT: " + ser.portstr)
print("---------------------------------------------------------------------")
print("\n")

            
while True:
        c = ser.readline()
        if c != b'':
            print("- RECEIVED RESULT ---------------------------------------------------\n")
            print("Read: {}".format(c))
            message = c[1:-1].decode('utf-8')

            f = open("sysmex_KX21.txt", "a") 
     
            #result
            testResult = handleresult(message)
            print(testResult)
                                 
            url = config.MIRTH_SERVER + "/record"
            transaction_code = int(round(time.time() * 1000))
            json_data = {   "device_id":5,
                            "transaction_code": transaction_code,
                            "record_type":"RESULT",
                            "raw_message": message,
                            "message_info":testResult
                        }
            
            astm_order = {
                "device_id": 5,
                "transaction_code": transaction_code,
                "record_type":"ORDER",
                "raw_message":message,
                "message_info": {
                    "specimen_id": "960" + testResult['patient_id']
                    }
                }
        
            requests.post(url, data=json.dumps(astm_order))

            requests.post(url, data=json.dumps(json_data))
            f.write("ASTM ORDER: {}".format(astm_order))

            f.write("RESULT DATA: {}".format(json_data))
            data_to_send = {
                "transaction_code": transaction_code
            }
            requests.post(config.MIRTH_SERVER + "/result-to-rhis", data=json.dumps(data_to_send))
            print("Send Result to RHIS transaction code : {}".format(transaction_code))
            f.write('\n')
            f.write('\n')
            f.close()
            print("\n")
            print("- COMPLETED ---------------------------------------------------------")
            print('\r\n')
            
f.close()                                 
ser.close()




