
class Records:

	def __init__(self):
		self

	def messageSplitter(self, message):
		i = 0
		text = ""
		while i < len(message):
			text += message[i] + "|"
			i += 1
		return text + "<CR>"
	
	def messageHeader(self, headerData):
		i = 0
		message = ""
		while i < len(headerData):
			message += headerData[i] + "|"
			i += 1
		return message + "<CR>"

	def messageTermination(self):
		print("message termination")

	def requestInformation(self):
		print("request information")

	def patientInformation(self):
		print("patient information")

	def testOrder(self):
		print("test order")

	def comment(self):
		print("comment")

	def result():
		print("result record")

	def establishment_phase(self, record):
		return "ACK"
		
	def orderReply(self):
		replyH = ("H","\^&","","","","host^1","cobas 311","TSDWN^REPLY","P","1")
		replyP = ("P","1","","","","","","20070921","M","","","","","","35^Y")
		replyO = ("O","1","000663","6^5002^002^^S1^SC","^^^10^3","R","","20050705093416","","","","N","","","","1","","","","","","","20050705095504","","","F","","","","","")
		replyL = ("L","1","N")

	def resultReceived(self):
		self
