import requests
import json

class Cobas411:

    def __init__(self):
        self

    def message_parser(self, data):
        message_list = data.split("|")
        return message_list

    def on_header(self, data):
        message = self.message_parser(data)
        sender = message[4].split("^")
        sender_name = sender[0]
        sender_serial_no = sender[1]
        sender_software_version = sender[2]
        sender_range_boundry = sender[3]

        processing_id = message[11]
        date_and_time = message[13]
        
        json_data = {
            "device_id":"1",
            "record_type":"HEADER",
            "raw_message": data
        }
        self.restful("POST",json_data)
        
    def on_patient(self, data):
        message = self.message_parser(data)
        json_data = {
            "device_id":"1",
            "record_type":"PATIENT",
            "raw_message": data
        }
        self.restful("POST",json_data)

    def on_order(self, data):
        message = self.message_parser(data)
        _record_type = message[0]
        _seq_no = message[1]
        _specimen_id = message[2]
        instrument_specimen_id = message[3].split("^")
        _instrument_sample_no = instrument_specimen_id[0]
        _instrument_rack_id = instrument_specimen_id[1]
        _instrument_position_no = instrument_specimen_id[2]
        _instrument_operator_id = instrument_specimen_id[3]
        _instrument_data_carrier_type = instrument_specimen_id[4]

        _priority = message[5]
        _action_code = message[11]
        _data_and_time = message[14]

        json_data = {
            "device_id":"1",
            "record_type":"ORDER",
            "raw_message": data
        }
        self.restful("POST",json_data)

    def on_result(self, data):
        message = self.message_parser(data)
        _record_type = message[0]
        _seq_no = message[1]
        universal_test_id = message[2].split("^")
        _universal_test_test_no = universal_test_id[0]
        _universal_test_test_code = universal_test_id[1]
        data_measurement = message[3].split("^")
        # _data_measurement_result = data_measurement[0]
        # _data_arbitrary_value = data_measurement[1]
        _unit = message[4]
        _operator_id = message[10]
        json_data = {
            "device_id":"1",
            "record_type":"RESULT",
            "raw_message": data
        }
        self.restful("POST",json_data)

    def on_comment(self, data):
        message = self.message_parser(data)
        _record_type = message[0]
        _seq_no = message[1]
        _comment_source = message[2]
        _comment_text = message[3]
        _comment_type = message[4]
        json_data = {
            "device_id":"1",
            "record_type":"COMMENT",
            "raw_message": data
        }
        self.restful("POST",json_data)

    def on_manufacturer(self, data):
        message = self.message_parser(data)
        _record_type = message[0]
        _seq_no = message[1]
        _record_type = message[2]
        universal_test_id = message[3].split("^")
        # _universal_test_id_no = universal_test_id[0]
        # _universal_test_id_code = universal_test_id[1]
        _test_frequency = message[4]
        _raw_result_value = message[5]
        json_data = {
            "device_id":"1",
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
            "device_id":"1",
            "record_type":"REQUEST",
            "raw_message": data
        }
        self.restful("POST",json_data)

    def restful(self, method, json_data):
        url = "http://localhost:8022/analyzer/header"
        if(method=="POST"):
            requests.post(url, data=json.dumps(json_data))
