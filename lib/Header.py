class Header:

    def __init__(self):
        self

    def getHeader(self,message):
        self.messageSplitter(message)

    def putHeader(self):
        delimeterDefinition = "OK"
        print(delimeterDefinition)
        print("putHeader")

    def messageSplitter(self,message):
        listMessage = message.split("|")
        print(len(listMessage))