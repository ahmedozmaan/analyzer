from devices import Urisys1100, Cobas411, Cobas311, Sysmex350xn
import time

class Astm:
    def __init__(self, file):
        self.STX = b"\x02"
        self.ETX = b"\x03"
        self.ENQ = b"\x05"
        self.ACK = b"\x06"
        self.LF  = b"\x10"
        self.CR  = b"\x13"
        self.NAK = b"\x21"
        self.EOT = b"\x04"

        self.combine_message = b""
        self.checksum_array = {}

        filename = file + "_log.txt"
        if(file == "cobas411"):
            self.device = Cobas411()
        if(file == "urisys1100"):
            self.device = Urisys1100()
        if(file == 'cobas311'):
            self.device = Cobas311()
        if(file == 'sysmex350xn'):
            self.device = Sysmex350xn()

        self.f = open(filename, "w")

    def deviceSend(self, data):
        print("ASTM Parser:")
        self.messageParser(data)

    def messageParser(self, message):
        control_character = message[0]
        if control_character == 2:
            messageString = message.decode()[1:-6].replace("Â·"," ")
            print("\tClean message: {}".format(messageString))
            messageArray = self.messageSplitter(messageString)
            m = 0
            while m < len(messageArray):
                if(m == 0):
                    self.recordType(messageArray[m],messageString)
                pos = m + 1
                info = "\t\t" + str(pos) + " => " + messageArray[m]
                print(info)
                m = m + 1
            # cs_from_message = message[-4:-2].decode() 
            # print("\tChecksum: {}".format(cs_from_message))                          #change accordingly
            # self.reply_message(cs_from_message, messageString)

    def messageSplitter(self,message):
        messageList = message.split("|")
        return messageList

    def recordType(self,field,full_message):
        record = field[-1:]
        tagNumber = field[:1]
        title = ""
        if record == "H":
            title = "Message Header"
            self.device.on_header(full_message)
        if record == "P":
            title = "Patient Information"
            self.device.on_patient(full_message)
        if record == "Q":
            title = "Request Information"
            self.device.on_request(full_message)
        if record == "O":
            title = "Test Order"
            self.device.on_order(full_message)
        if record == "R":
            title = "Result"
            self.device.on_result(full_message)
        if record == "L":
            title = "Message Termination"
        if record == "C":
            title = "Comment"
            self.device.on_comment(full_message)
        if record == "M":
            title = "Manufacturer"
            self.device.on_manufacturer(full_message)
        self.f.write("\t\tTag No " + tagNumber + "\n")
        self.f.write("\t\t" + title + " Record\n")
        self.f.write("\t\t---------------------\n")

        print("\tTag No " + tagNumber)
        print("\t" + title + " Record")
        print("\t---------------------")

    def classLoader(self, recordType):
        print("load class " + recordType)
    
    def reply_message(self, cs, message):
        cs_calc = self.device.checksum(message)
        reply = ""
        if cs == cs_calc:
            reply = "PASS"
        else:
            reply = "FAILED #bypass"
        print("\tFrom Record: {} Checksum: {}".format(cs, cs_calc))
        print("\tChecksum check result: {}".format(reply))
        return reply
    
    def checkRequest(self, tocheck):
        return self.device.check_request(tocheck)

    def cobas311Parser(self, message):
        self.combine_message += message[1:-5]
        self.checksum_array[chr(message[0])] = message[-4:-2] 
    
    def cobas411Parser(self, message):
        self.combine_message += message[1:-5]
        self.checksum_array[chr(message[0])] = message[-4:-2]

    def finaldata(self):
        self.device.transaction_code = int(round(time.time() * 1000))
        output = self.combine_message
        s = self.combine_message.split(b'\r')
        i = 0
        a = 1
        b = 0
        while i < len(s):
            clean = s[i].decode().strip()
            if clean != '':
                print("\nMessage {}: {}".format(a, clean))
                print("Transaction Code: {}".format(self.device.transaction_code))
                firstLetter = str(b) + clean[0]
                checksum = self.device.checksum(firstLetter + clean)
                byteMessage = b'\x02' + clean.encode() + b'\x13' + b'\x03' + checksum.encode() + b'\x13' + b'\x10'  # construct as ASTM frame format
                self.deviceSend(byteMessage)
                a += 1
                if b > 7:
                    b = 0
                else:
                    b += 1
            i += 1
        self.device.transaction_code = ""
        print("---------------------------------------------------------------------")
        self.combine_message = b''

    def checksum_cobas(self, message):
        i = 0
        sum_value = 0
        while i < (len(message)):
            sum_value = sum_value + message[i]
            i += 1
        return hex(sum_value)[-2:].upper()
