"""The type-checker for :mod:`~.X86 :class:`~.Operand` and 
:class:`~.Instruction` objects.  It is important for its own sake (to ensure 
that user-created :class:`~.Instruction` objects are valid within the X86 
instruction set), as well as during encoding (to determine how the instruction
should be encoded).  It supports three interfaces:
	
* :meth:`.check`, to check a single :class:`~.Operand` against a single :class:`~.AOTElt`;
* :meth:`.TypeCheckInstruction_exn`, to check an instruction against a list of :class:`~.AOTElt` types and raise a :class:`X86TypeCheckError` on failure;
* :meth:`.TypeCheckInstruction_opt`, to check an instruction against a list of :class:`~.AOTElt` types and return ``None`` on failure.
"""

from X86 import *
from X86InternalOperand import *
from X86InternalOperandDescriptions import *
from Pandemic.Util.Visitor import Visitor2
from Pandemic.Util.ExerciseError import ExerciseError

class X86TypeCheckError(Exception):
	"""This exception may be thrown during type-checking.  One interface method
	allows exceptions to pass through; another catches them and returns `None`.
	"""
	def __init__(self,str):
		self.str = str
	def __str__(self):
		return self.str

class TypeCheckInfo(object):
	"""This class holds information about the overrides required by an operand.
	Any member may be `None`, in which case that particular override is not 
	meaningful for the operand.
	
	:ivar bool sizeo: operand size OPSIZE prefix required or not
	:ivar bool addro: address size ADDRSIZE prefix required or not
	:ivar `.SegElt` sego: a segment, if such a prefix is required
	"""
	def __init__(s,sizeo=None,addro=None,sego=None):
		s.sizeo,s.addro,s.sego = sizeo,addro,sego

def SizePFX(b,t=None): 
	"""Either return a new :class:`.TypeCheckInfo` object with the *sizeo* field
	set to *b* if *t* is `None`, or update *t* with that information.
	
	:ivar bool b: operand size prefix required
	:ivar `.TypeCheckInfo` t: existing :class:`TypeCheckInfo` object or `None`
	:rtype: .TypeCheckInfo
	"""
	if t is None: return TypeCheckInfo(sizeo=b)
	t.sizeo = b
	return t

def AddrPFX(b,t=None):
	"""Either return a new :class:`.TypeCheckInfo` object with the *addro* field
	set to *b* if *t* is `None`, or update *t* with that information.
	
	:ivar bool b: address size prefix required
	:ivar `.TypeCheckInfo` t: existing :class:`TypeCheckInfo` object or `None`
	:rtype: .TypeCheckInfo
	"""
	if t is None: return TypeCheckInfo(addro=b)
	t.addro = b
	return t

def SegPFX(s,t=None):  
	"""Either return a new :class:`.TypeCheckInfo` object with the *sego* field
	set to *s* if *t* is `None`, or update *t* with that information.
	
	:ivar `.SegElt` s: segment prefix required
	:ivar `.TypeCheckInfo` t: existing :class:`TypeCheckInfo` object or `None`
	:rtype: .TypeCheckInfo
	"""
	if t is None: return TypeCheckInfo(sego=s)
	t.sego = s
	return t

def MATCHES(): 
	"""Return an empty :class:`.TypeCheckInfo` object."""
	return TypeCheckInfo()

class X86TypeChecker(Visitor2):
	"""This :class:`~.Visitor.Visitor2` class implements type-checking for X86
	instructions.
	"""
	
	def check(self,aop,opnd):
		"""The main interface method that clients should call when type-checking a
		single abstract operand / x86 operand pair.  Look up the :class:`.X86AOTDL`
		for *aop*, and check its compatibility with *opnd*.
		
		:param `.AOTElt` aop:
		:param `.X86Internal.Operand` opnd:
		:rtype: .TypeCheckInfo
		:returns: Information about required prefix overrides, or `None` if *opnd*
			was incompatible with *aop*.

		"""
		self.check_sizes = not aop in self.lenient_sizes
		return self.visit(opnd,AOTtoAOTDL[aop.IntValue()])

	#: For these abstract operand types, don't check the sizes.
	lenient_sizes = set([OFPEnv,OFPEnvLow,OSimdState])
	
	def TypeCheckInstruction_exn(self,instr,aops):
		"""Checks the instruction's operands against a list of abstract
		operand types.  This particular variant of the function will throw an 
		exception with information as to why the instruction was not accepted.
		Another method, :meth:`TypeCheckInstruction_opt`, catches exceptions and 
		returns ``None`` if one was raised.
		
		:param `.X86.Instruction` instr: instruction to type-check
		:param aops: list of abstract operand types to check against
		:type aops: :class:`.AOTElt` list
		:rtype: ( `bool` , `bool`, `.SegElt` ) tuple
		:raises `X86TypeCheckError`: if the instruction or one of its operands did 
			not match.
		"""

		# If the number of operands differs, the encoding cannot be valid.
		if len(aops) != instr.NumOps():
			raise X86TypeCheckError("Operand lengths differ!")

		# If there are no operands, there can be no overrides.
		if len(aops) == 0:
			return (False,False,None)

		# Given two TypeCheckInfo objects, ensure that their override requirements
		# do not conflict.  Return whether the prefix is required, or None.
		def reduce_typeinfo(t1,t2):
			def opcheck(bo1,bo2,errorstr):
				if bo1 is None: return bo2
				if bo2 is None: return bo1
				if bo1 == bo2:  return bo1
				raise X86TypeCheckError(errorstr)
			
			# "Accumulate" the override information in t1.  I.e., if the first 
			# operand specified an address size override, and the second operand
			# specified an operand size override, we need to have both of those
			# facts available when checking the third operand.  Update the t1 
			# structure and return it.

			# If both sizes can be overriden, they must either both be overridden, 
			# or both not be overridden.  Same for address sizes.
			t1.sizeo = opcheck(t1.sizeo,t2.sizeo,"Size mismatch!")
			t1.addro = opcheck(t1.addro,t2.addro,"Address size mismatch!")
		
			# For segments, if multiple segment overrides are present, ensure the
			# overrides match.
			t1.sego  = opcheck(t1.sego,t2.sego,"Segments clash!")
			return t1

		# Begin with a non-existent TypeCheckInfo last_ti.
		last_ti = None
		
		# Iterate through all of the TypeCheckInfo objects and make sure that they
		# are mutually coherent, using the reduce_typeinfo function above.
		for i in xrange(len(aops)):
			# Visit the operand and turn it into a TypeCheckInfo object.
			ti = self.check(aops[i],instr.GetOp(i))
			if ti is None: raise X86TypeCheckError("Operand does not match!")
			last_ti = ti if last_ti is None else reduce_typeinfo(last_ti,ti)

		# Return a triple describing required overrides.
		return (last_ti.sizeo == True,last_ti.addro == True,last_ti.sego)
		
	def TypeCheckInstruction_opt(self,instr,aops):
		"""Calls :meth:`TypeCheckInstruction_exn`.  If it throws an exception,
		return `None`.
		
		:param `.X86.Instruction` instr: instruction to type-check
		:param aops: list of abstract operand types to check against
		:type aops: :class:`.AOTElt` list
		:rtype: ( `bool` , `bool`, `.SegElt` ) tuple
		"""
		retval = None
		try: retval = self.TypeCheckInstruction_exn(instr,aops)
		except X86TypeCheckError, e: pass
		return retval

	def MakeMethodName(s,op1,enc):
		"""We override this method from the :class:`~.Visitor.Visitor` class to
		simplify the design.  In particular, we separate the types that may be held
		by :class:`~.ImmEnc` and :class:`~.SignedImm` operand descriptions.
		
		:param `.Operand` op1:  X86 operand to check
		:param `.X86AOTDL` enc:  AOTDL for which to choose a 
			:meth:`visit_` method.
		:rtype: string
		:returns: a string naming one of the `visit_` methods.
		
		"""
		if isinstance(enc,ImmEnc):
			op = enc.archetype
			if isinstance(op,MemExpr):   return "visit_Immediate_MemExpr"
			if isinstance(op,FarTarget): return "visit_Immediate_FarTarget"
			if isinstance(op,Immediate): return "visit_Immediate_Immediate"
			return "visit_Immediate_%s" % op.__class__.__name__

		elif isinstance(enc,SignedImm):
			op = enc.archetype
			if isinstance(op,JccTarget): return "visit_Immediate_JccTarget"
			return "visit_SignExtImm_%s" % op.__class__.__name__

		return "visit_" + enc.__class__.__name__
	
	def Default(s,op1,enc):
		"""This method is invoked when the operand *op1* and AOTDL *enc* were
		incompatible, the default case for a :class:`~.Visitor.Visitor` object.
		
		:param `.Operand` op1:  X86 operand which failed type-checking
		:param `.X86AOTDL` enc:  AOTDL which failed type-checking
		:rtype: ``None``
		"""
		return None
	
	def visit_SizePrefix(s,op,z): 
		"""Used when visiting prefixed operand types.  First, try to visit the 
		member where a prefix is required (i.e., *z*'s *yes* member).  If it 
		matches, update the information returned to indicate that the prefix was 
		required.  Otherwise, visit the member where no prefix is required (i.e., 
		*z*'s *no* member), and if that matches, return the flags from the match 
		plus a flag indicating that an override is possible (but not required).  
		Otherwise, no match, i.e. return ``None``.
		
		:param `.Operand` op1:  X86 operand
		:param `.SizePrefix` z:
		:rtype: TypeCheckInfo
		"""
		raise ExerciseError("X86TypeChecker::visit_SizePrefix")

	def visit_AddrPrefix(s,op,a): 
		"""See comments for :meth:`visit_SizePrefix`.

		:param `.Operand` op1:  X86 operand
		:param `.AddrPrefix` a:
		:rtype: TypeCheckInfo
		"""
		raise ExerciseError("X86TypeChecker::visit_AddrPrefix")
		
	def visit_Exact(s,op,a): 
		"""For Exact AOTDL elements, *op* must match *a*'s *value* member exactly.

		:param `.Operand` op:  X86 operand
		:param `.Exact` a:
		:rtype: TypeCheckInfo
		"""
		if op == a.value:
			raise ExerciseError("X86TypeChecker::visit_Exact")
		return None
	
	def visit_ExactSeg(s,op,a): 
		"""For ExactSeg AOTDL elements, *op* must match *a*'s *value* member 
		exactly, or it must match *value* when *value*'s :attr:`~.Seg` attribute
		is changed to that of *op*.  In the latter case, the return value must
		indicate that a segment override prefix is required.

		:param `.Operand` op:  X86 operand
		:param `.ExactSeg` a:
		:rtype: TypeCheckInfo
		"""
		if op == a.value: 
			raise ExerciseError("X86TypeChecker::visit_ExactSeg: Exact match")

		if isinstance(op,MemExpr) and isinstance(a.value,MemExpr):
			# Make a copy of a.value with op's segment, and compare it to op.
			if a.value(op.Seg) == op: 
				raise ExerciseError("X86TypeChecker::visit_ExactSeg: Segment differs")
		return None

	def visit_RegOrMem(s,op,m):
		"""For RegOrMem AOTDL elements, check both possibilities:  that *op* may 
		match *m*'s *reg* component, or that it may match the *mem* component 
		(specified by a :class:`~.MSElt` enumeration element).  When comparing 
		memories, issue any necessary address and/or segment override prefixes.
		The size of the memory is part of the comparison, unless the abstract
		operand type is one of those for which size comparisons should not occur
		(see :attr:`.lenient_sizes`).
		
		:param `.Operand` op:  X86 operand
		:param `.RegOrMem` m:
		:rtype: TypeCheckInfo
		"""
		if m.reg is not None and type(op) == type(m.reg):
			raise ExerciseError("X86TypeChecker::visit_RegOrMem:Register")

		if m.mem is not None and isinstance(op,MemExpr):
			# For certain memory-related AOTs, we are lenient about the sizes of 
			# memory operands.  I.e., we just ensure that the operand is a memory
			# without regard to its size.  For all other AOTs, check that the size
			# is correct.
			if m.mem == op.size or not s.check_sizes:
				
				# Check whether op's segment differs from its default segment.  If so,
				# indicate that that particular segment prefix is required.
				raise ExerciseError("X86TypeChecker::visit_RegOrMem:Memory:Segment")
				s_tc = None
				
				# Check whether op is a Mem16, i.e., requires an ADDRSIZE prefix.  a_tc
				# should be created based on s_tc.
				raise ExerciseError("X86TypeChecker::visit_RegOrMem:Memory:Addrsize")
				a_tc = None

				return a_tc
		return None
	
	def visit_GPart(s,op,a):
		"""For GPart AOTDL elements, ensure that the operand type specified in 
		*a*'s *archetype* member has the same type as the operand *op*.
		
		:param `.Operand` op:  X86 operand
		:param `.GPart` a:
		:rtype: TypeCheckInfo
		"""
		if type(op) == type(a.archetype):
			raise ExerciseError("X86TypeChecker::visit_GPart")
		return None
	
	def visit_Immediate_MemExpr(s,op,a):
		"""For ImmEnc AOTDL elements whose *archetype* members are of type 
		:class:`.MemExpr`, ensure that the operand *op* is indeed a 
		:class:`.MemExpr` object that consists solely of a displacement 
		(:attr:`~.MemExpr.Disp` member) -- in particular, that :attr:`.BaseReg` and
		:attr:`.IndexReg` are ``None``.  As for all :class:`.MemExpr` operands,
		check for address-size and segment-override prefixes.
		
		:param `.Operand` op:  X86 operand
		:param `.ImmEnc` a: :class:`ImmEnc` with :class:`.MemExpr` *archetype*
		:rtype: TypeCheckInfo
		"""
		# Check for immediate only
		if isinstance(op,MemExpr) and op.BaseReg == None and op.IndexReg == None:
			# Check that the sizes match
			if a.archetype.size == op.size:
				# Check the segment and address size prefix requirements, identically
				# to the RegOrMem memory case.
				s_tc = None
				a_tc = None
				raise ExerciseError("X86TypeChecker::visit_Immediate_MemExpr")

				return a_tc
		return None

	def visit_Immediate_FarTarget(s,op,a):
		"""For ImmEnc AOTDL elements whose *archetype* members are of type 
		:class:`.FarTarget`, ensure that the operand *op* has the same type as
		*archetype*.
		
		:param `.Operand` op:  X86 operand
		:param `.ImmEnc` a: :class:`ImmEnc` with :class:`.AP16` or :class:`.AP32`
			*archetype*
		:rtype: TypeCheckInfo
		"""
		if type(op) == type(a.archetype):
			raise ExerciseError("X86TypeChecker::visit_Immediate_FarTarget")
		return None

	def visit_Immediate_JccTarget(s,op,a):
		"""For ImmEnc AOTDL elements whose *archetype* members are of type 
		:class:`.JccTarget`, ensure that the operand *op* also has type 
		:class:`.JccTarget`.
		
		:param `.Operand` op:  X86 operand
		:param `.ImmEnc` a: :class:`ImmEnc` with :class:`.JccTarget` *archetype*
		:rtype: TypeCheckInfo
		"""
		if isinstance(op,JccTarget): 
			raise ExerciseError("X86TypeChecker::visit_Immediate_JccTarget")
		return None

	def visit_Immediate_Immediate(s,op,a):
		"""For ImmEnc AOTDL elements whose *archetype* members are of type 
		:class:`.ImmEnc`, ensure that the operand *op* has the same type as 
		*archetype*.
		
		:param `.Operand` op:  X86 operand
		:param `.ImmEnc` a: :class:`ImmEnc` with :class:`.Immediate` *archetype*
		:rtype: TypeCheckInfo
		"""
		if type(op) == type(a.archetype):
			raise ExerciseError("X86TypeChecker::visit_Immediate_Immediate")
		return None
	
	def visit_SignExtImm_Iw(s,op,a):
		"""For SignedImm AOTDL elements whose *archetype* members are of type 
		:class:`~.Iw`, ensure that the operand *op* is an :class:`~.Immediate` with
		a *value* that fits into 8-bits and can be sign-extended to the same 16-bit
		constant.
		
		:param `.Operand` op:  X86 operand
		:param `.SignedImm` a: :class:`~.SignedImm` with :class:`~.Iw` *archetype*
		:rtype: TypeCheckInfo
		"""
		if isinstance(op,Iw) and (op.value < 0x80 or op.value >= 0xFF80):
			raise ExerciseError("X86TypeChecker::visit_SignExtImm_Iw")
		return None
		
	def visit_SignExtImm_Id(s,op,a):
		"""For SignedImm AOTDL elements whose *archetype* members are of type 
		:class:`~.Id`, ensure that the operand *op* is an :class:`~.Immediate` with
		a *value* that fits into 8-bits and can be sign-extended to the same 32-bit
		constant.
		
		:param `.Operand` op:  X86 operand
		:param `.SignedImm` a: :class:`~.SignedImm` with :class:`~.Id` *archetype*
		:rtype: TypeCheckInfo
		"""
		if isinstance(op,Id) and (op.value < 0x80 or op.value >= 0xFFFFFF80):
			raise ExerciseError("X86TypeChecker::visit_SignExtImm_Id")
		return None
