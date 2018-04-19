from Pandemic.X86.X86MetaData import *
from Pandemic.X86.X86ByteStream import StreamObj
from Pandemic.X86.X86Encoder import X86Encoder
from Pandemic.X86.X86Decoder import X86Decoder
from X86Random import generate_random_instruction
import random
from ..VerboseTestCase import VerboseTestCase

num_iterations = 10000

# For these mnemonics, sometimes we encode them with zero operands, and 
# sometimes we encode them with one or two operands.  This screws up the 
# comparison below, as it is strictly based on mnemonic, number of operands,
# and equality of operands.  Hence, skip those mnemonics.
multi_operand_mnems = [
  Das,Aad,Aam,Lodsb,Lodsw,Lodsd,Cmpsb,Cmpsw,Cmpsd,Movsb,Movsw,Movsd,
  Stosb,Stosw,Stosd,Scasb,Scasw,Scasd]

class TestX86EndToEnd(VerboseTestCase):
	encoder = X86Encoder()
	def one_iteration(self,i):
		instr = generate_random_instruction(lambda x: x in multi_operand_mnems)		
		print "Iteration", i, instr, "%r" % instr, 
		enc = self.encoder.EncodeInstruction(instr)
		self.assertIsNotNone(enc,"[I] %s: Couldn't encode!" % instr)
		bFailed = enc is None
		for x in enc: print hex(x),
		print ""
		decoder = X86Decoder(StreamObj(enc))
		i2container = decoder.Decode(0)
		i2 = i2container.instr
		if i2 == None:
			print "[I]", instr
			print "[I] Bytes:", map(lambda x: hex(x),enc) 
			print "Couldn't decode!"
			self.assertIsNotNone(i2)
			bFailed = True
		if instr != i2:
			print "[I] %s (%r)" % (instr,instr)
			print "[I] Bytes:", map(lambda x: hex(x),enc) 
			print "[!] %s (%r): decoded instruction did not match!" % (i2,i2)
			print "[!] instr.prefixes", instr.prefixes
			print "[!] i2.prefixes", i2.prefixes
			self.assertEqual(instr,i2)
			bFailed = True
		if self.verbose and not bFailed:
			print "%s: end-to-end test passed!" % instr
	
	def test_Randomly(self):
		for i in xrange(num_iterations):
			self.one_iteration(i)