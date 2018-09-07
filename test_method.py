
def order_instrument_speciment(astmstring):
    string = astmstring.split('^')
    print("\tSequence No: {}".format(string[0]))
    print("\tCarrier No: {}".format(string[1]))
    print("\tPosition No: {}".format(string[2]))
    print("\tSample Type: {}".format(string[4]))
    print("\tContainer Type: {}".format(string[5]))
    print("\n")

def order_universal_test_id(astmstring):
    repeater = astmstring.split("\\")
    for r in repeater:
        string = r.split('^')
        print('\t--------------------')
        print("\tApplication Code: {}".format(string[3]))
        print("\tDilution: {}".format(string[4]))

def order_reply():
    data = {
        "record_type": "O",
        "sequence_no": "1",
        "specimen_id": "0000",
        "instrument_specimen_id":{
            "sequence_no": "6",
            "carrier_no": "44",
            "position_no": "2",
            "sample_type": "S1",
            "container_type":"SC",
        },
        "universal_test_id":[{
            "application_code":"30",
            "dilution":"2"
        },
        {
            "application_code":"30",
            "dilution":"2"
        }],
        "priority":"R",
        "specimen_collection_date": "",
        "action_code": "",
        "speciment_descriptor": "",
        "date_result": "YYYYMMDDHHMMSS",
        "report_types": "F"
    }

    instrument_specimen_id = data['instrument_specimen_id']['sequence_no']
    instrument_specimen_id += "^" + data['instrument_specimen_id']['carrier_no']
    instrument_specimen_id += "^" + data['instrument_specimen_id']['position_no']
    instrument_specimen_id += "^^" + data['instrument_specimen_id']['sample_type']
    instrument_specimen_id += "^" + data['instrument_specimen_id']['container_type']

    uti = 0
    universal_test_id = ""
    while uti < len(data['universal_test_id']):
        universal_test_id += "^^^" + data['universal_test_id'][uti]['application_code']
        universal_test_id += "^" + data['universal_test_id'][uti]['dilution']
        if uti < (len(data['universal_test_id'])-1):
            universal_test_id += "\\"
        uti = uti + 1

    astm = (
        data['record_type'],
        data['sequence_no'],
        data['specimen_id'],
        instrument_specimen_id,
        universal_test_id
    )

    astm_string = ""
    i = 0
    while i < len(astm): 
        astm_string += str(astm[i])
        if i < (len(astm)-1):
            astm_string += '|'
        i = i+1
        

    print("ASTM string: {}".format(astm_string))

#order_instrument_speciment('6^44^2^^S1^SC')
#order_universal_test_id('^^^10^\^^^30^2\^^^40^')

# order_reply()

test = {
    1: "record_type",
    2: "sequence_no",
    5: "universal test"
}

# print(test.get(5))

a = b"\x021H|\\^&|||H7600^1|||||host|RSUPL^BATCH|P|1\rP|1|||||||U||||||^\rO|1|PCCC2                 |4051^30064^064^^QC^SC|^^^798^\\^^^435^\\^^^717^\\^^^552^\\^^^781^|||||||Q||||1|||||||20180824103051|||F\rC|1|I|^^^^|G\rR|1|^^^798/|4.60|mmol/l||N||||ADMIN |||P\x17EE\r\n"
b = b"\x0221\rC|1|I|0|I\rR|2|^^^435/|1.51|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rR|3|^^^717/|12.99|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rR|4|^^^552/|2.56|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rR|5|^^^781/|2.47|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rL|1|N\r\x0355\r\n"
c = b"\x02H|\\^&|||host^1|||||H7600|TSDWN^REPLY|P|1\rP|1\rO|1|^^   ^3^50002^002^^S1^SC|^^^717^||ALL||||||||O\rL|1|N\r\n"
d = b"\x02H|\\^&|||host^1|||||H7600|RSREQ^REAL|P|1\rQ|1|^^PCCC2                 ^4030^30064^064^^SC^QC^SC||ALL||||||||F\rL|1|N\r\n"
string = d.decode()
print(len(string))
