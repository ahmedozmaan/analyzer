
def checksum(input_string):
    messages = input_string.encode()
    lrc = 0
    for b in messages[1:]:
        lrc ^= b
    print(lrc)  


def firstBit(input_string):
    print(input_string)

# firstBit(b'\x02')

# checksum("1H|\^&|||URISYS1100^99305^SW5.31^INT|||||||P||20090116184200")

import binascii

def checksum_algob():
    messages = "6C|10|I|*|I"
    clean = messages.split(',')
    check = ''
    calc = 0
    for i in clean:
        if i != 'STX' and i != 'CR':
            if i == 'ETX':
                val = '03'
            else:
                val = i.encode('utf-8').hex()
                print("val {} \n".format(val))
            calc = int(calc) + int(val, 16)
        
        c = 0
    for a in str(calc):
        c = c + int(a)

    d = (c + 62) % 256
    hexa = hex(d)
    print("calc : {}".format(c))
    print("final : {}".format(d))
    print("hex : {}".format(hexa))

            
# checksum_algob()

def cs_algo_a():
    import binascii
    import re
    message = b"7L|1|N"
    hexstring = binascii.hexlify(message)
    listArr = re.findall('..', hexstring.decode())
    lrc = 0
    for i in listArr:
        lrc ^= 1 * ('0x' + str(i))
    
    print(lrc.encode())

def checkSum_cobas411():
    import binascii
    import codecs

    message = ("1","T","e","s","t")
    sumHexa = 0
    for i in message:
        hexS = hex(ord(i))
        aa = bytes(hexS, encoding="ascii")
        ab = codecs.encode(aa,"hex")
        print("decode : " + ab )
        print("hexa :" + aa.decode())
        sumHexa = sumHexa + int(hexS[2:])
        hexDecimal = hex(sumHexa)
        print("{} => Hexa : {}".format(i,hexDecimal))
        print(sumHexa)
    # print(sumHexa)

# checkSum_cobas411()

def checksumCobas411(message):
    import binascii
    sum_value = 16
    position = 0
    for i in message:
        str_char = ord(i)
        sum_value = sum_value + str_char
        position = position + 1
        str_to_hex = hex(sum_value)
        print("{} => {} sum : {} => {}".format(i,str_char,sum_value, str_to_hex))
    print("Checksum : {}".format(str_to_hex[-2:].upper()))
    
def checksumUrisys():
    # message = input("ASTM >> ")
    # message = b'1H|\\^&|||H7600^1|||||host|RSUPL^BATCH|P|1\rP|1|||||||U||||||^\rO|1|PCCC2                 |4030^30064^064^^QC^SC|^^^798^\\^^^435^\\^^^717^\\^^^552^\\^^^781^|||||||Q||||1|||||||20180702152234|||F\rC|1|I|^^^^|G\rR|1|^^^798/|4.60|mmol/l||A||||ADMIN |||P'
    message = b'1H|\\^&|||cobas-e411^1|||||host|RSUPL^BATCH|P|1\rP|1\rO|1|880912-08-5309|3104^0001^2^^S1^SC|^^^117^1\\^^^900^1\\^^^880^1\\^^^136^1|R||20180821095503||||N||||1|||||||20180821104134|||F\rR|1|^^^117/1/not|<2.00|IU/l||LL||F||ADMIN|||E1\rC|1|I|27|I\rR|2|^\x173F\r\n'
    m = message.decode().split('\r')
    j = 0
    s = 0
    sum_value = 0
    hexxx = 4
    while j < len(m):
        # sum_value += 13 #CR + ETX
        for i in m[j]:
            sum_value = sum_value + ord(i)
        # str_to_hex = hex(sum_value)
        s += sum_value
        print("message: {} >> {}".format(m[j], hex(s)))
        hexxx += int(hex(s), 16)
        j += 1
    # s = s + 17
    print("HEXX : {}".format(hex(hexxx-49)))
    return hex(s)[-2:].upper()
    # for m in message.split('\r'):
        # print(m)
    # message = message.replace('\\',"\")
    # print("\n Output: {}".format(bmsg))
    # sum_value = 16 #CR + ETX
    # for i in message:
    #     sum_value = sum_value + ord(i)
    #     str_to_hex = hex(sum_value)
    # return str_to_hex[-2:].upper()

    #6

# print(checksumUrisys())



def message_construct():
    import codecs
    STX = b'\x02'
    CR  = b'\x13'
    ETX = b'\x03'
    LF  = b'\x10'
    msg = b"1H|\^&|||URISYS1100^99305^SW5.31^INT|||||||P||20090116184200"
    # test = codecs.decode("10bc47510","hex")
    return STX + msg + CR + ETX
    # "[STX]1H|\^&|||URISYS1100^99305^SW5.31^INT|||||||P||20090116184200[CR][ETX]F8[CR][LF]"

#print(message_construct())

#"4R|01|01^ SG|1.020|gcm3|||||20090116|LNorman^A"

def checksum_cobas():
    # message = b'1H|\\^&|||cobas-e411^1|||||host|RSUPL^BATCH|P|1\rP|1\rO|1|880912-08-5309|3104^0001^2^^S1^SC|^^^117^1\\^^^900^1\\^^^880^1\\^^^136^1|R||20180821095503||||N||||1|||||||20180821104134|||F\rR|1|^^^117/1/not|<2.00|IU/l||LL||F||ADMIN|||E1\rC|1|I|27|I\rR|2|^\x173F\r\n'
    # message = b'1H|\\^&|||host^1|||||H7600|RSREQ^BATCH|P|1\rQ|1|^^PCCC2                 ^4030^30064^064^^SC^QC^SC||ALL||||||||F\rL|1|N\x0381\r\n'
    message = b'1H|\\^&|||host^1|||||H7600|RSREQ^BATCH|P|1\x0drQ|1|^^     2* RCPA  (109-04)0^50031^031^^S1^SC||ALL||||||||F\x0dL|1|N\x0d8D\x0d\x0a'
    i = 0
    sum_value = 0
    while i < (len(message)-4):
        print("Ascii: {}, Decimal: {}".format(chr(message[i]), message[i]))
        # sum_value = sum_value + ord(message[i])
        sum_value = sum_value + message[i]
        i += 1
    print("Sum Value: {}".format(sum_value))
    print("Sum Value to Hex: {}".format(hex(sum_value)))
    print("Checksum: {}".format(message[-4:-2].decode()))

checksum_cobas()

## 126-004
## 340 0002

#check whether <CR> is in the terminus if L record
