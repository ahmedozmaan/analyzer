import json
import requests

class Urisys1100:

    def __init__(self):
        self

    def message_parser(self, data):
        message_list = data.split("|")
        return message_list


    def on_header(self, data):
        message = self.message_parser(data)
        sender = message[4].split("^")
        _sender_device_type = sender[0]
        _sender_device_id = sender[1]
        _sender_software_version = sender[2]
        _sender_limit_table_type = sender[3]

        _processing_id = message[11]
        _date_and_time = message[13]
        json_data = {
            "device_id":"2",
            "record_type":"HEADER",
            "raw_message": data
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
        """
        required fields: 1,2,3,4,5,10,11
        """
        message = self.message_parser(data)
        _record_type = message[0]
        _seq_no = message[1]
        _specimen_id = message[2]
        instrument_specimen_id = message[3].split("^")
        _instrument_sample_no = instrument_specimen_id[0]
        _instrument_rack_id = instrument_specimen_id[1]
        _instrument_position_no = instrument_specimen_id[2]
        # _instrument_operator_id = instrument_specimen_id[3]
        # _instrument_data_carrier_type = instrument_specimen_id[4]

        _setted_result = message[4]
        _last_menu_calibrate = message[9]
        _operator_code = message[10]
        json_data = {
            "device_id":"2",
            "record_type":"ORDER",
            "raw_message": data
        }
        self.restful("POST",json_data)

    def on_result(self, data):
        """
        required fields: 1,2,3,4,5
        """
        message = self.message_parser(data)
        _record_type = message[0]
        _record_serial_no = message[1]
        _field_3 = message[2]
        field_4 = message[3].split("^")
        _field_4_1 = field_4[0]
        # _field_4_2 = field_4[1]
        _field_5 = message[4]
        json_data = {
            "device_id":"2",
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
            "device_id":"2",
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

    def restful(self, method, json_data):
        url = "http://localhost:8022/analyzer/header"
        if(method=="POST"):
            requests.post(url, data=json.dumps(json_data))