# -*- coding: utf-8 -*-

#: ASTM specification base encoding.
ENCODING = 'latin-1'
STX = b'\x02'
ETX = b'\x03'
EOT = b'\x04'
ENQ = b'\x05'
ACK = b'\x06'
NAK = b'\x15'
ETB = b'\x17'
LF  = b'\x0A'
CR  = b'\x0D'

#: Message records delimiter.
RECORD_SEP    = b'\x0D' # \r #
#: Record fields delimiter.
FIELD_SEP     = b'\x7C' # |  #
#: Delimeter for repeated fields.
REPEAT_SEP    = b'\x5C' # \  #
#: Field components delimiter.
COMPONENT_SEP = b'\x5E' # ^  #
#: Date escape token.
ESCAPE_SEP    = b'\x26' # &  #