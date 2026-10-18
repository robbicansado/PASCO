# Reproducible static assertions on original UTF-16 AVR disassembly.
# Run from a checkout that has the original disassembly path below.
from pathlib import Path
import re
p = Path("PASCO/flexduino_v5_disassembly.txt")
s = p.read_text(encoding="utf-16")
ins = {int(m.group(1), 16): m.group(2) for m in re.finditer(
    r"^\s*([0-9a-f]+):\s+((?:[0-9a-f]{2} )+\s+\S+[^\n]*)", s, re.M)}
checks = {
    "ADC0 selected": "0x40" in ins[0xa1e] and "0x007C" in ins[0xa20],
    "ADC conversion started": "0x40" in ins[0xa28],
    "ADC low/high read": "0x0078" in ins[0xa36] and "0x0079" in ins[0xa3a],
    "61 samples": (0x288 - 0x194)//4 == 61 and "brne" in ins[0xa86],
    "median index 30": (0x20c - 0x194)//4 == 30,
    "pulse limit 15000": "0x98" in ins[0xb4e] and "0x3A" in ins[0xb50],
    "five echo attempts": "0x05" in ins[0xb06],
    "pulse loop counter": "sub" in ins[0x8b4] and "ld" in ins[0x8c6],
    "28-bit mask": "0x0F" in ins[0xb6e],
    "50ms delay argument": "0x32" in ins[0xc66] and "0x254" in ins[0xc6e],
    "loop back": "0xa1a" in ins[0xc7a],
    "fallback print": "0x4d2" in ins[0xc90] and "0xc5e" in ins[0xc94],
}
for label, ok in checks.items():
    print(("OK" if ok else "FAIL"), label)
assert all(checks.values())
print(len(checks), "static invariants passed")
