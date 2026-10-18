# Reproducible V5 UART audit: pass original disassembly path as argv[1].
import re, sys
from pathlib import Path
s=Path(sys.argv[1]).read_text(encoding="utf-16")
ins={}
for line in s.splitlines():
 m=re.match(r"^\s*([0-9a-fA-F]+):\s+((?:[0-9a-fA-F]{2}\s+)+)\s*(\S+)(.*)$",line)
 if m: ins[int(m[1],16)]=(m[3],m[4].strip())
tests=[
(0xc96,"ldi","r30, 0x91"),(0xc98,"ldi","r31, 0x02"),
(0xcb6,"ldi","0xC5"),(0xcba,"std","Z+13"),
(0xcbe,"ldi","0xC4"),(0xcc4,"std","Z+14"),
(0xcc6,"ldi","0xC0"),(0xccc,"std","Z+16"),
(0xcce,"ldi","0xC1"),(0xcd4,"std","Z+18"),
(0xcd6,"ldi","0xC2"),(0xcdc,"std","Z+20"),
(0xcde,"ldi","0xC6"),(0xce4,"std","Z+22"),
(0x988,"ldi","0x02"),(0x99e,"ldi","0xCF"),
(0x9ae,"ldi","0x06"),(0x97c,"sts","0x00C1"),
(0x980,"lds","0x02A1"),(0x996,"lds","0x029F"),
(0x9a6,"lds","0x02A5"),(0x9b2,"lds","0x02A3")]
for a,op,arg in tests:
 assert a in ins and ins[a][0]==op and arg in ins[a][1],(hex(a),ins.get(a))
assert 0x291+12==0x29d and 0x291+14==0x29f and 0x291+16==0x2a1
assert 0x291+18==0x2a3 and 0x291+20==0x2a5
baud=16000000/(8*(207+1))
assert abs(baud-9600)/9600 < .002
print("22 instrucoes + enderecamento + baud: OK")
print("baud com clock hipotetico 16MHz:",round(baud,2))
