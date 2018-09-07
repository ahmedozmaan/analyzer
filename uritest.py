import serial
import time
from astm import Astm
import os
import requests
import json

ser = serial.Serial(port='/dev/cu.wchusbserial1410',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

d = open('testuni-1.txt','w')
def printMsg():
	return true
	
print("connected to: " + ser.portstr)
print("\n")
count=1
seq = []

# def replybak():
# 	print("reply back")
# 	ser.write(b'\x02')
# 	ser.write(b'\x3E')
# 	ser.write(b'\x03')
# 	ser.write(b'\x33')
# 	ser.write(b'\x45')
# 	ser.write(b'\x0D')
# 	time.sleep(5)
# 	print('reply end')

number = 1
result = {}

def cleanResult(result):
	return result[8:13].strip()

while True:
	c = ser.readline()
	if c != b'': 
		if c != b'\r':
			d.write(str(number) + " : " + c.decode())
			result[number] = c.decode()
			number = number +1
			if number == 17:
				testResult = {
					"device_name": result.get(1)[:23].strip(),
					"sequence_no": result.get(2)[10:13].strip(),
					"patient_id": result.get(3)[11:23],
					"test_date": result.get(4).strip(),
					"result": {
						"SG": cleanResult(result.get(6)),
						"pH": cleanResult(result.get(7)),
						"LEU": cleanResult(result.get(8)),
						"NIT": cleanResult(result.get(9)),
						"PRO": cleanResult(result.get(10)),
						"GLU": cleanResult(result.get(11)),
						"KET": cleanResult(result.get(12)),
						"UBG": cleanResult(result.get(13)),
						"BIL": cleanResult(result.get(14)),
						"ERY": cleanResult(result.get(15))
					}
				}
				print("-------------------------")
				print(testResult)
				url = "http://localhost:8022/analyzer/record"
				json_data = {
					"device_id":1,
					"record_type":"RESULT",
					"raw_message": "",
					"message_info":testResult
				}
				requests.post(url, data=json.dumps(json_data))
				print("-------------------------")
				number = 1
				result = {}
ser.close()