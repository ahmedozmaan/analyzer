
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
    
#checksumCobas411("5R|2|2^pH|7|||||||service")

def checksumUrisys():
    message = input("ASTM >> ");
    sum_value = 16 #CR + ETX
    for i in message:
        sum_value = sum_value + ord(i)
        str_to_hex = hex(sum_value)
    return str_to_hex[-2:].upper()

print(checksumUrisys())

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

"4R|01|01^ SG|1.020|gcm3|||||20090116|LNorman^A"