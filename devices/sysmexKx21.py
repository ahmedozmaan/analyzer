import requests
import json
import time
import config

class SysmexKx21:

    def __init__(self):
        self

    def message_parser(self, data):
        message_list = data.split("|")
        return message_list


    def on_header(self, data):
        message = self.message_parser(data)
        device = message[4].split("^")
        header_info = {
            "device_type": device[0],
            "device_id": device[1],
            "device_software_version": device[2],
            "limit_table_type": device[3],
            "message_date_time": message[13]
        }
        
        json_data = {
            "device_id":"2",
            "record_type":"HEADER",
            "raw_message": data,
            "message_info": header_info
        }
        self.restful("POST",json_data)

    def on_patient(self, data):
        message = self.message_parser(data)
        _record_type = message[0]
        _seq_no = message[1]
        json_data = {
            "device_id":"2",
            "record_type":"PATIENT",
            "raw_message": data
        }
        self.restful("POST",json_data)

    def on_order(self, data):
        message = self.message_parser(data)
        instrument_specimen_id = message[3].split("^")
        order_info = {
            "patient_identifier": message[2],
            "measurement_no": instrument_specimen_id[0],
            "serial_no": instrument_specimen_id[1],
            "strip_type_setting": instrument_specimen_id[2],
            "type_of_measurement": message[4],
            "date_time_test": message[14]
        }
        json_data = {
            "device_id":"2",
            "record_type":"ORDER",
            "raw_message": data,
            "message_info" : order_info
        }
        self.restful("POST",json_data)

    def on_result(self, data):
        message = self.message_parser(data)
        result_info = {
            "record_serial_number": message[1],
            "parameter_serial_number": message[2],
            "result_setted_system": message[3],
            "setted_result_unit": message[4],
            "date_last_menu_calibrate": message[9],
            "operator_code": message[10]
        }
        json_data = {
            "device_id":"2",
            "record_type":"RESULT",
            "raw_message": data,
            "message_info": result_info
        }
        self.restful("POST",json_data)

    def on_comment(self, data):
        message = self.message_parser(data)
        comment_data = {
            "record_serial_no": message[1],
            "flag": message[3]
        }
        json_data = {
            "device_id":"2",
            "record_type":"COMMENT",
            "raw_message": data,
            "message_info": comment_data
        }
        self.restful("POST",json_data)

    def on_manufacturer(self, data):
        message = self.message_parser(data)
        _record_type = message[0]
        _seq_no = message[1]
        _record_type = message[2]
        universal_test_id = message[3].split("^")
        _universal_test_id_no = universal_test_id[0]
        _universal_test_id_code = universal_test_id[1]
        _test_frequency = message[4]
        _raw_result_value = message[5]
        json_data = {
            "device_id":"2",
            "record_type":"MANUFACTURER",
            "raw_message": data
        }
        self.restful("POST",json_data)

    def on_request(self, data):
        message = self.message_parser(data)
        _record_type = message[0]
        _seq_no = message[1]
        record_type_sub_id = message[2].split("^")
        _record_type_sub_id_all = record_type_sub_id[1]
        json_data = {
            "device_id":"2",
            "record_type":"REQUEST",
            "raw_message": data
        }
        self.restful("POST",json_data)
    
    def checksum(self, message):
        print("to calc: {}".format(message))
        sum_value = 16 #CR + ETX
        for i in message:
            sum_value = sum_value + ord(i)
            str_to_hex = hex(sum_value)
        return str_to_hex[-2:].upper()

    def check_request(self):
        print("Info : Host is checking if any request required by this machine")
        params = {
            "device_id": self.device_id
        }
        response = self.restful("GET", params, "request")
        time.sleep(4)
        print("INFO : Checking done")
        print(json.loads(response.text))
    
    def restful(self, method, json_data, route = "record"):
        url = "{}/{}".format(config.MIRTH_SERVER, route)
        response = ""
        if method == "POST":
            requests.post(url, data=json.dumps(json_data))
        if method == "PUT":
            requests.put(url, data=json.dumps(json_data))
        if method == "GET":
            params = "?device_id={}".format(json_data["device_id"])
            url = url + '?device-id={}'.format(params)
            response = requests.get(url)
        return response
