import serial
import time
from astm import Astm
import config
import os
import requests
import json

ser = serial.Serial(port=config.URYSIS_1100_COMPORT, baudrate=9600, timeout=1)

print("\n")
print("- HOST STARTED ------------------------------------------------------")
print("  COMMUNICATION PORT: " + ser.portstr)
print("---------------------------------------------------------------------")
print("\n")
count = 1
seq = []
number = 1
result = {}

def cleanResult(result):
    print(result)
    return result[8:14].strip()

while True:
    c = ser.readline()
    if c != b'':
        if c != b'\r':
            d.write(str(number) + " : " + c.decode())
            result[number] = c.decode()
            print("Number : {}".format(number))
            number = number + 1
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
                url = config.MIRTH_SERVER + "/record"
                json_data = {
					"device_id": 1,
                                        "transaction_code": int(round(time.time() * 1000)),
					"record_type": "RESULT",
					"raw_message": "",
					"message_info": testResult
				}
                requests.post(url, data=json.dumps(json_data))
                print("-------------------------")
                number = 1
                result = {}
ser.close()
