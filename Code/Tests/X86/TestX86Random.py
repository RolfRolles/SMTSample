from Pandemic.X86.X86InternalOperand import X86_INTERNAL_OPERAND_LAST, AOTElt
from X86Random import X86RandomOperand, rnd_bool
import random
from ..VerboseTestCase import VerboseTestCase

num_iterations = 10000

class TestX86Random(VerboseTestCase):
	rog = X86RandomOperand()

	def random_aop(self): 
		return AOTElt(random.randint(0,X86_INTERNAL_OPERAND_LAST))

	def one_iteration(self,i):
		m,sego,s,b = rnd_bool(),rnd_bool(),rnd_bool(),rnd_bool()
		aop = self.random_aop() 
		print "%d %s:" % (i,aop),
		opnd  = self.rog.gen(aop,(m,sego,s,b))
		print "%r %s" % (opnd,opnd)
	
	def test_X86Random(self):
		for i in xrange(num_iterations):
			self.one_iteration(i)