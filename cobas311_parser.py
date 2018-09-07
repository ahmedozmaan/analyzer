


combine = []

def parser(message):
    data = message.decode()
    splitter = data.split('\r')
    i = 0
    while i < len(splitter):
        print("message {}:".format(splitter[i]))
        i += 1


blocks = (
    b'1H|\\^&|||H7600^1|||||host|RSUPL^BATCH|P|1\rP|1|||||||U||||||^\rO|1|PCCC2                 |4030^30064^064^^QC^SC|^^^798^\\^^^435^\\^^^717^\\^^^552^\\^^^781^|||||||Q||||1|||||||20180702152234|||F\rC|1|I|^^^^|G\rR|1|^^^798/|4.60|mmol/l||A||||ADMIN |||P\x17E0\r\n',
    b'21\rC|1|I|101|I\rR|2|^^^435/|1.55|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rR|3|^^^717/|13.12|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rR|4|^^^552/|2.42|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rR|5|^^^781/|2.35|mmol/l||N||||ADMIN |||P1\rC|1|I|0|I\rL|1|N\r\x03A5\r\n'   
)

combine_block = b""
i = 0
while i < len(blocks):
    combine_block += blocks[i]
    i += 1

print(combine_block)
