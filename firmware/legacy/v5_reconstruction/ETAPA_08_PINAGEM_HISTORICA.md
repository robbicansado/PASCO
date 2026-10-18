# V5 historical reverse engineering — stage 08

Source: original `flexduino_v5_disassembly.txt` from the supplied PASCO archive. This is **historical** firmware; do not use these pins as the current validated PASCO wiring.

## Candidate Arduino `pinMode` calls

The AVR instructions at 0x09EA–0x0A00 load arguments into r24 and r22 and call 0x01A8, consistent with the Arduino AVR `pinMode(pin, mode)` function.

| Location | Registers and call | Candidate reconstruction |
| --- | --- | --- |
| 0x09EA | r22=0x01, r24=0x0B, call 0x01A8 | `pinMode(11, OUTPUT)` |
| 0x09F2 | r22=0x00, r24=0x0A, call 0x01A8 | `pinMode(10, INPUT)` |
| 0x09FA | r22=0x00, r24=0x0E, call 0x01A8 | `pinMode(14, INPUT)` (A0 on Nano) |

**Confidence:** actual instruction bytes confirmed; identification as `pinMode` is a strong but not yet independently validated inference. We have not proven this path is reached during normal execution.

Calls at 0x0A02 and 0x0A0A pass 286 and 320 to 0x04D2; the function and units are still unknown.

The application writes to 0x00C1 at 0x097C and 0x1C02. Some peripheral configuration is indirect through SRAM pointers. The bootloader serial initialization at 0x7A7E must not be mistaken for the application's serial speed.

## Do not infer

- That pins 11, 10 or 14 are correct for the current physical FlexDuino.
- That any specific sensor is associated with a pin.
- That the original source code has been recovered.
- That the firmware is safe to flash onto a working board.

Next: identify 0x04D2 and trace the main program's call graph. This document is analysis, not executable firmware.
