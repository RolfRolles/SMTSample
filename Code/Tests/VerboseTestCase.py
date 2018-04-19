"""Python's unittest module has the deficiency where TestCase classes aren't 
able to discover whether the verbose option was passed on the command line.  
This class remedies the situation in a very inelegant way:  it checks the
command-line arguments for "-v" and/or "--verbose", and sets the "verbose"
instance method if such an argument was present.  This allows test cases to 
print extra information if the verbose flag was specified."""
import unittest
import sys

class VerboseTestCase(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		unittest.TestCase.__init__(self,*args,**kwargs)
		# UGLY, INELEGANT HACK HERE:
		verbosecount = sys.argv.count("-v") + sys.argv.count("--verbose")
		self.verbose = verbosecount >= 2
		
