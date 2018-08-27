
def start_establishment():
    print('Enter your commands below.\r\nInsert "exit" to leave the application.')
    user_input = input(">> ")
    if user_input == 'exit':
        exit()
    else:
        input_response(user_input)

def input_response(input_msg):
    upperMsg = input_msg.upper()
    writeToDevice = ""
    if upperMsg == "ENQ":
        writeToDevice = "ACK"
    if upperMsg == "EOT":
        writeToDevice = "ACK"
    
    print("Write to Device : {}".format(writeToDevice))

start_establishment()