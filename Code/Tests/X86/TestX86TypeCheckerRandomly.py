from Pandemic.X86.X86InternalOperand import *
from Pandemic.X86.X86TypeChecker import X86TypeChecker,TypeCheckInfo
from X86Random import X86RandomOperand, rnd_bool
import random
from ..VerboseTestCase import VerboseTestCase

num_iterations = 10000

class TestX86TypeCheckerRandomly(VerboseTestCase):
	tc = X86TypeChecker()
	rog = X86RandomOperand()

	def do_test(self,aop,opnd,res,(m,sego,s,a)):
		if self.verbose:
			print "Testing", opnd, "against abstract operand", aop, "expecting result", res, m,sego,s,a
		error = "%s: operand %r(%s) did not match!" % (aop,opnd,opnd)
		self.assertIsNotNone(res,error)
		bFailed = res is None
		error = "X86TypeChecker(%s,%s) should have returned a TypeCheckInfo object, not type %s" % (aop,opnd,type(res))
		self.assertIsInstance(res,TypeCheckInfo,error)
		bFailed |= not(isinstance(res,TypeCheckInfo))
		error = "%s: operand %r(%s) did not report that a size prefix was required!" % (aop,opnd,opnd)
		self.assertFalse(s and res.sizeo == False,error)
		bFailed |= s and res.sizeo == False
		error = "%s: operand %r(%s) did not report that an address prefix was required!" % (aop,opnd,opnd)
		self.assertFalse(a and res.addro == False,error)
		bFailed |= a and res.addro == False
		if self.verbose and not bFailed:
			print "%s: matched %s (test passed)!" % (aop,opnd)

	def one_iteration(self):
		m,sego,so,ao = rnd_bool(),rnd_bool(),rnd_bool(),rnd_bool()
		aop = AOTElt(random.randint(0,X86_INTERNAL_OPERAND_LAST))
		opnd = self.rog.gen(aop,(m,sego,so,ao))
		res  = self.tc.check(aop,opnd)
		self.do_test(aop,opnd,res,(m,sego,so,ao))
		
	def test_Randomly(self):
		for i in xrange(0,num_iterations):
			self.one_iteration()