# coding=utf-8
from astm import Astm
import time

# "4R|01|01^ SG|1.020|gcm3|||||20090116|LNorman^A"
# "5R|02|02^ pH|    7||||||20090116|LNorman^A"
# "5R|10|10^ERY|   50^   3+| Ery/ul|||||20090116|LNorman^A"
### machine sending sample

dummy_messages = (
    "[ENQ]",
    "[STX]1H|\^&|||URISYS1100^99305^SW5.31^INT|||||||P||20090116184200[CR][ETX]F8[CR][LF]",
    "[STX]2P|1[CR][ETX]3F[CR][LF]",
    "[STX]3O|1||001^00036^C10|Urinalysis^Incubated|R||||||X|||20090116184100[CR][ETX]00[CR][LF]",
    "[STX]4R|01|01^·SG|1.020|gcm3|||||20090116|LNorman^A[CR][ETX]BB[CR][LF]",
    "[STX]5R|02|02^·pH|····7||||||20090116|LNorman^A[CR][ETX]09[CR][LF]",
    "[STX]6R|03|03^LEU|··neg^··neg|·Leu/ul|||||20090116|LNorman^A[CR][ETX]0B[CR][LF]",
    "[STX]7R|04|04^NIT|··neg^··neg||||||20090116|LNorman^A[CR][ETX]BD[CR][LF]",
    "[STX]0R|05|05^PRO|··neg^··neg|·mg/dl·|||||20090116|LNorman^A[CR][ETX]D1[CR][LF]",
    "[STX]1R|06|06^GLU|·norm^··neg|·mg/dl·|||||20090116|LNorman^A[CR][ETX]2D[CR][LF]",
    "[STX]2R|07|07^KET|··neg^··neg|·mg/dl·|||||20090116|LNorman^A[CR][ETX]CA[CR][LF]",
    "[STX]3R|08|08^UBG|·norm^··neg|·mg/dl·|||||20090116|LNorman^A[CR][ETX]29[CR][LF]",
    "[STX]4R|09|09^BIL|··neg^··neg|·mg/dl·|||||20090116|LNorman^A[CR][ETX]C3[CR][LF]",
    "[STX]5R|10|10^ERY|···50^···3+|·Ery/ul|||||20090116|LNorman^A[CR][ETX]A9[CR][LF]",
    "[STX]6C|10|I|*|I[CR][ETX]96[CR][LF]",
    "[STX]7L|1|N[CR][ETX]0A[CR][LF]",
    "[EOT]",
)

astm = Astm("urisys1100")
run = 0
while run < len(dummy_messages):
    astm.deviceSend(dummy_messages[run])
    run = run + 1
    time.sleep(1)