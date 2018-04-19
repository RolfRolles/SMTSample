#!/usr/bin/python
import sys
from Pandemic.X86.X86Parser import parser
from Pandemic.X86.X86Encoder import X86Encoder

if(len(sys.argv) == 1 or len(sys.argv) > 3):
	print "Usage: %s \"instruction to encode\" [optional address]" % sys.argv[0]
	sys.exit()

res = parser.parse(sys.argv[1])
addr = 0 if len(sys.argv)==2 else int(sys.argv[2])
bytes = X86Encoder().EncodeInstruction(res,addr)
print res, "(%r) encoded as [" % res,
for b in bytes:
	print "%#02lx" % b,
print "]"