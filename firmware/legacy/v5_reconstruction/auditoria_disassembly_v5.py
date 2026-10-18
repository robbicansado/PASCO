# Verify selected V5 AVR disassembly invariants.
# Run from repository root with original disassembly at PASCO/flexduino_v5_disassembly.txt
from pathlib import Path
import re
p = Path("PASCO/flexduino_v5_disassembly.txt")
s = p.read_text(encoding="utf-16")
ins = {int(m.group(1), 16): m.group(2) for m in re.finditer(r"^\s*([0-9a-f]+):\s+([^\n]+)$", s, re.M)}
checks = {
    "ADC prescaler bits": all("ori" in ins[a] for a in (0x958,0x962,0x96c)),
    "ADC enabled": "0x80" in ins[0x976],
    "ADC0 selected": "0x40" in ins[0xa1e] and "0x007C" in ins[0xa20],
    "ADC started": "0x40" in ins[0xa28],
    "ADC low/high": "0x0078" in ins[0xa36] and "0x0079" in ins[0xa3a],
    "61 samples": (0x288-0x194)//4 == 61 and "brne" in ins[0xa86],
    "median index": (0x20c-0x194)//4 == 30,
    "UCSR0B reset": "0x00C1" in ins[0x97c],
    "serial U2X candidate": "0x02" in ins[0x988],
    "baud divisor candidate": "0xCF" in ins[0x99e],
    "serial frame candidate": "0x06" in ins[0x9ae],
    "echo timeout": "0x98" in ins[0xb4e] and "0x3A" in ins[0xb50],
    "echo counter": "sub" in ins[0x8b4] and "ld" in ins[0x8c6],
    "echo mask": "0x0F" in ins[0xb6e],
    "sampling loop": "0xa1e" in ins[0xa86],
}
for label, ok in checks.items():
    print(("PASS" if ok else "FAIL"), label)
assert all(checks.values())
print(len(checks), "invariantes aprovadas")
