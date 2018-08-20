from devices import Urisys1100, Cobas411

class Astm:
    
    def __init__(self,file):
        filename = file + "_log.txt"
        if(file == "cobas411"):
            self.device = Cobas411()
        if(file == "urisys1100"):
            self.device = Urisys1100()

        self.f = open(filename, "w")

    def deviceSend(self, data):
        if(data=="[EOT]"):
            self.f.write("====END OF TRANSMISSION====")
            print("====END OF TRANSMISSION====")

        else:
            if(data=="[ENQ]"):
                self.f.write("====START OF TRANSMISSION====\r\n\n")
                print("====START OF TRANSMISSION====\n")
            self.f.write("Device: "+ data + '\n')
            print("Device: "+ data)
            self.messageParser(data)
            self.f.write("Host: ACK\n")
            self.f.write("-----\r\n\n")
            
            print("Host: ACK")
            print("-----\n")        

    def cleanMessage(self, message):
        text = message
        head, sep, tail = text.partition("[CR]")
        return head[5:]

    def messageParser(self, message):
        control_character = message[:5]
        self.f.write("Control Character: " + control_character[1:4] + "\n")
        print("Control Character: " + control_character[1:4])
        if(control_character=="[STX]"):
            messageString = self.cleanMessage(message)
            self.f.write("Clean Message: " + messageString + "\n")
            print("Clean Message: " + messageString)
            messageArray = self.messageSplitter(messageString)
            m = 0
            while m < len(messageArray):
                if(m == 0):
                    self.recordType(messageArray[m],messageString)
                pos = m + 1
                info = "\t" + `pos` + " => " + messageArray[m]
                self.f.write( info + "\n")
                print(info)
                m = m + 1
            self.f.write("\n")
        return control_character

    def messageSplitter(self,message):
        messageList = message.split("|")
        return messageList

    def recordType(self,field,full_message):
        record = field[-1:]
        tagNumber = field[:1]
        title = "";
        if(record == "H"):
            title = "Message Header"
            self.device.on_header(full_message)
        if(record == "P"):
            title = "Patient Information"
            self.device.on_patient(full_message)
        if(record == "Q"):
            title = "Request Information"
            self.device.on_request(full_message)
        if(record == "O"):
            title = "Test Order"
            self.device.on_order(full_message)
        if(record == "R"):
            title = "Result"
            self.device.on_result(full_message)
        if(record == "L"):
            title = "Message Termination"
        if(record == "C"):
            title = "Comment"
            self.device.on_comment(full_message)
        if(record == "M"):
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
    
    