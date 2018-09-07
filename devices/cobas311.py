import requests
import json
import time

class Cobas311:

    def __init__(self):
        self.device_id = "3"
        self.device_name = "COBAS 311"
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
            "receiver_id": len(message) > 9 and message[9],
            "instruction": len(message) > 10 and message[10],
            "processing_id": len(message) > 11 and message[11]
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
        specimen = message[3].split('^')
        order_info = {
            "sequence_no": message[1],
            "specimen_id": message[2],
            "instrument_specimen_id":{
                "sequence_no": specimen[0],
                "rack_id": specimen[1],
                "position_no": specimen[2],
                "sample_type": specimen[4],
                "container_type": len(specimen) > 5 and specimen[5],
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
        # self.restful("POST",json_data)

    def checksum(self, message):
        sum_value = 16 #CR + ETX
        for i in message:
            sum_value = sum_value + ord(i)
            str_to_hex = hex(sum_value)
        return str_to_hex[-2:].upper()

    def on_request(self, data):
        message = self.message_parser(data)
        rangeInfo = message[2].split('^')
        request_info = {
            "sequence_no": message[1],
            "start_range_id":{
                "sample_id": rangeInfo[2],
                "sequence_no": rangeInfo[3],
                "rack_id_no": rangeInfo[4],
                "position_no": rangeInfo[5],
                "sample_type": rangeInfo[7],
                "container_type": rangeInfo[8]
            },
            "universal_test_id":message[4],
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
        self.params = {
            "sample_id": rangeInfo[2],
            "sequence_no": rangeInfo[3],
            "position_no": rangeInfo[5]
        }
        self.restful("POST",json_data)
        self.restful("POST", machine_ask, 'request')

    def check_request(self):
        print("Info : Host is checking if any request required by this machine")
        p = {
            "device_id": self.device_id,
            "sample_id": self.params.get("sample_id"),
            "sequence_no": self.params.get('sequence_no'),
            "position_no": self.params.get('position_no')
        }
        query = "?device_id={}&sample_id={}&sequence_no={}&position_no={}".format(p.get('device_id'), p.get('sample_id'), p.get('sequence_no'), p.get('position_no'))
        response = self.restful("GET", query, "request")
        time.sleep(4)
        return json.loads(response.text)

    def restful(self, method, json_data, route = "record"):
        url = "http://localhost:8022/analyzer/{}".format(route)
        response = ""
        if method == "POST":
            requests.post(url, data=json.dumps(json_data))
        if method == "PUT":
            requests.put(url, data=json.dumps(json_data))
        if method == "GET":
            url = url + json_data
            response = requests.get(url)
        return response
