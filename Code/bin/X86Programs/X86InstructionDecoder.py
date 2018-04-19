#!/usr/bin/python
import sys
from Pandemic.X86.X86ByteStream import StreamObj
from Pandemic.X86.X86Decoder import X86Decoder

if(len(sys.argv) == 1 or len(sys.argv) > 3):
	print "Usage: %s [byte string to decode, e.g. 33c0]" % sys.argv[0]
	sys.exit()

l = []
for i in xrange(0,len(sys.argv[1]),2):
	l.append(int("0x"+sys.argv[1][i:i+2],16))

print X86Decoder(StreamObj(l)).Decode(0).instr
