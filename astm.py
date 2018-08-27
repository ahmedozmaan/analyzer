from devices import Urisys1100, Cobas411
import time

class Astm:
    # STX = b'\x02'
    # ETX = b'\x03'
    # ENQ = b'\x05'
    # ACK = b'\x06'
    # LF  = b'\x10'
    # CR  = b'\x13'
    # NAK = b'\x21'
    # EOT = b'\x04'

    def __init__(self,file):
        self.STX = "[STX]"
        self.ETX = "[ETX]"
        self.ENQ = "[ENQ]"
        self.ACK = "[ACK]"
        self.LF  = "[LF]"
        self.CR  = "[CR]"
        self.NAK = "[NAK]"
        self.EOT = "[EOT]"

        filename = file + "_log.txt"
        if(file == "cobas411"):
            self.device = Cobas411()
        if(file == "urisys1100"):
            self.device = Urisys1100()

        self.f = open(filename, "w")

    def deviceSend(self, data):
        if data == self.EOT:
            self.device.check_request()
            time.sleep(5)
            self.f.write("====END OF TRANSMISSION====")
            print("====END OF TRANSMISSION====")

        else:
            if data == self.ENQ:
                self.f.write("====START OF TRANSMISSION====\r\n\n")
                print("====START OF TRANSMISSION====\n")
            self.f.write("Device: {} \n".format(data))
            print("Device: {}".format(data))
            self.messageParser(data)
            self.f.write("Host: ACK\n")
            self.f.write("-----\r\n\n")
            
            print("Host: ACK")
            print("-----\n")        

    def cleanMessage(self, message):
        text = message
        head, sep, tail = text.partition(self.CR)
        return head[5:]

    def messageParser(self, message):
        control_character = message[:5]
        self.f.write("Control Character: " + control_character[1:4] + "\n")
        print("Control Character: " + control_character[1:4])
        if control_character== self.STX:
            messageString = self.cleanMessage(message)
            self.f.write("Clean Message: " + messageString + "\n")
            print("Clean Message: " + messageString)
            messageArray = self.messageSplitter(messageString)
            m = 0
            while m < len(messageArray):
                if(m == 0):
                    self.recordType(messageArray[m],messageString)
                pos = m + 1
                info = "\t" + str(pos) + " => " + messageArray[m]
                self.f.write( info + "\n")
                print(info)
                m = m + 1
            self.f.write("\n")
            cs_from_message = message[-10:-8]                           #change accordingly
            self.reply_message(cs_from_message, messageString)
        return control_character

    def messageSplitter(self,message):
        messageList = message.split("|")
        return messageList

    def recordType(self,field,full_message):
        record = field[-1:]
        tagNumber = field[:1]
        title = "";
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
        self.f.write("\tTag No " + tagNumber + "\n")
        self.f.write("\t" + title + " Record\n")
        self.f.write("\t---------------------\n")

        print("\tTag No " + tagNumber)
        print("\t" + title + " Record")
        print("\t---------------------")

    def classLoader(self, recordType):
        print("load class " + recordType)
    
    def reply_message(self, cs, message):
        cs_calc = self.device.checksum(message)
        reply = ""
        if cs == cs_calc:
            reply = self.ACK
        else:
            reply = self.NAK
        print("From msg: {} Checksum: {}".format(cs, cs_calc))
        print("Reply to Device: {}".format(reply))
        return reply
        