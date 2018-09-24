import requests
import json
import time
import config

class Cobas411:
    def __init__(self):
        self.device_id = "2"
        self.device_name = "COBAS 411"
        self.params = {}
        self.transaction_code = ""
        self
 
    def message_parser(self, data):
        message_list = data.split("|")
        return message_list

    def on_header(self, data):
        message = self.message_parser(data)
        sender = message[4].split("^")
        header_info = {
            "device_name": sender[0],
            "device_software_version": sender[1],
            "instruction": message[10],
            "processing_id": message[11],
            "version_no": message[12]
        }
        
        json_data = {
            "device_id":self.device_id,
            "transaction_code": self.transaction_code,
            "record_type":"HEADER",
            "raw_message": data,
            "message_info": header_info
        }
        self.restful("POST",json_data)
        
    def on_patient(self, data):
        message = self.message_parser(data)
        patient_info = {
            "sequence_no": message[1]
        }
        json_data = {
            "device_id":self.device_id,
            "transaction_code": self.transaction_code,
            "record_type":"PATIENT",
            "raw_message": data,
            "message_info": patient_info
        }
        self.restful("POST",json_data)
    
    def on_order(self, data):
        message = self.message_parser(data)
        order_info = {
            "sequence_no": message[1],
            "specimen_id": message[2],
            "instrument_specimen_id":{
                "sequence_no": "",
                "carrier_no": "",
                "position_no": "",
                "sample_type": "",
                "container_type": "",
            },
            "universal_test_id": message[4],
            "priority": message[5],
            "specimen_datetime": message[7],
            "action_code": message[11],
            "specimen_descriptor": len(message) > 15 and message[15],
            "result_datetime": len(message) > 22 and message[22],
            "record_type": len(message) > 25 and message[25]
        }
        json_data = {
            "device_id":self.device_id,
            "transaction_code": self.transaction_code,
            "record_type":"ORDER",
            "raw_message": data,
            "message_info": order_info
        }
        self.restful("POST",json_data)

    def on_result(self, data):
        message = self.message_parser(data)
        result_type = {
            "sequence_no":message[1],
            "universal_test_id": message[2],
            "measurement_value": message[3],
            "unit": message[4],
            "reference_range": message[5],
            "result_abnormal_flags": message[6],
            "result_status": message[8],
            "operator": message[10],
            "test_start_datetime": len(message) > 11 and message[11],
            "test_complete_datetime": len(message) > 12 and message[12]
        }
        json_data = {
            "device_id":self.device_id,
            "transaction_code": self.transaction_code,
            "record_type":"RESULT",
            "raw_message": data,
            "message_info": result_type
        }
        self.restful("POST",json_data)

    def on_comment(self, data):
        message = self.message_parser(data)
        comment_info = {
            "sequence_no":"",
            "comment_source":"",
            "comment_text":"",
            "comment_type":"",
        }
        json_data = {
            "device_id":self.device_id,
            "transaction_code": self.transaction_code,
            "record_type":"COMMENT",
            "raw_message": data,
            "message_info": comment_info
        }
        self.restful("POST",json_data)

    def on_manufacturer(self, data):
        message = self.message_parser(data)
        manufacturer_info = {

        }
        json_data = {
            "device_id":self.device_id,
            "transaction_code": self.transaction_code,
            "record_type":"MANUFACTURER",
            "raw_message": data,
            "message_info": manufacturer_info
        }
        self.restful("POST",json_data)

    def checksum(self, message):
        sum_value = 16 #CR + ETX
        for i in message:
            sum_value = sum_value + ord(i)
            str_to_hex = hex(sum_value)
        return str_to_hex[-2:].upper()

    def on_request(self, data):
        message = self.message_parser(data)
        request_info = {
            "sequence_no": message[1],
            "start_range_id":{
                "sample_id":"",
                "sequence_no":"",
                "carrier_no":"",
                "position_no":"",
                "sample_type":"",
                "container_type":""
            },
            "universal_test_id":"",
            "request_information_status_code":""
        }
        machine_ask = {
            "device_id": self.device_id,
            "device_flag": 1,
            "query_info": request_info
        }
        json_data = {
            "device_id":self.device_id,
            "transaction_code": self.transaction_code,
            "record_type":"REQUEST",
            "raw_message": data,
            "message_info":request_info
        }
        self.restful("POST",json_data)
        self.restful("POST", machine_ask, 'request')

    def check_request(self, tocheck):
        print("  HOST       : Host is checking request for  {}".format(tocheck['sample_id'].lstrip()))
        p = {
            "device_id": self.device_id,
            "sample_id": tocheck['sample_id'],
            "position": tocheck['position']
        }
        query = "?device_id={}&sample_id={}".format(self.device_id, p['sample_id'])
        response = self.restful("GET", query, "request")
        time.sleep(4)
        return json.loads(response.text)

    def restful(self, method, json_data, route = "record"):
        url = "{}/{}".format(config.MIRTH_SERVER, route)
        response = ""
        if method == "POST":
            requests.post(url, data=json.dumps(json_data))
        if method == "PUT":
            requests.put(url, data=json.dumps(json_data))
        if method == "GET":
            url = url + json_data
            response = requests.get(url)
        return response
