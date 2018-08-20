# coding=utf-8
import time
from astm import Astm

### machine sending sample
dummy_messages = (
    "[ENQ]",
    "[STX]1H|\^&|||cobas·u·411^8^3.2.0.1001^Int|||||||P||20110315101822[CR][ETX]71[CR][LF]",
    "[STX]2P|1[CR][ETX]3F[CR][LF]",
    "[STX]3O|1|001|1^^^^SAMPLE||R||||||X|||20110315101754[CR][ETX]F0[CR][LF]",
    "[STX]4R|1|1^SG|1.005|||||||service[CR][ETX]AD[CR][LF]",
    "[STX]5R|2|2^pH|7|||||||service[CR][ETX]11[CR][LF]",
    "[STX]6R|3|3^LEU|neg|||||||service[CR][ETX]45[CR][LF]",
    "[STX]7R|4|4^NIT|neg|||||||service[CR][ETX]4D[CR][LF]",
    "[STX]0R|5|5^PRO|neg|||||||service[CR][ETX]4E[CR][LF]",
    "[STX]1R|6|6^GLU|neg|||||||service[CR][ETX]48[CR][LF]",
    "[STX]2R|7|7^KET|neg|||||||service[CR][ETX]47[CR][LF]",
    "[STX]3R|8|8^UBG|neg|||||||service[CR][ETX]44[CR][LF]",
    "[STX]4R|9|9^BIL|neg|||||||service[CR][ETX]40[CR][LF]",
    "[STX]5R|10|10^ERY|neg|||||||service[CR][ETX]AA[CR][LF]",
    "[STX]6R|11|11^COL|p.yel|||||||service[CR][ETX]49[CR][LF]",
    "[STX]7R|12|12^CLA||||||||service[CR][ETX]56[CR][LF]",
    "[STX]0M|1|RC|||2001601|20111001|||[CR][ETX]8F[CR][LF]",
    "[STX]1L|1|N[CR][ETX]04[CR][LF]",
    "[EOT]"
)

astm = Astm("cobas411")
run = 0
while run < len(dummy_messages):
    astm.deviceSend(dummy_messages[run])
    run = run + 1
    time.sleep(1)