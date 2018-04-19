"""This module implements the encoder for X86 instructions, in the 
:class:`X86Encoder` class."""

from X86 import *
from X86InternalOperand import *
from X86InternalOperandDescriptions import *
import X86EncodeTable
from X86TypeChecker import X86TypeChecker
from X86ModRM import ModRM16, ModRM32, little_endian_bytes
from Pandemic.Util.Visitor import Visitor2
from Pandemic.Util.ExerciseError import ExerciseError

#: Mapping from segments to their appropriate prefix bytes.
PrefixOfSeg=dict()
PrefixOfSeg[CS] = 0x2E
PrefixOfSeg[SS] = 0x36
PrefixOfSeg[DS] = 0x3E
PrefixOfSeg[ES] = 0x26
PrefixOfSeg[FS] = 0x64
PrefixOfSeg[GS] = 0x65

class X86Encoder(Visitor2):
	"""This :class:`~.Visitor2` class is responsible for turning X86 
	:class:`~.Instruction` objects into their encoded binary representation, 
	i.e., lists of bytes.  All of its variables are internal; users of this class
	should only interact with it through the :meth:`EncodeInstruction` and
	:meth:`EncodeInstructions` methods.
	
	:ivar `.X86TypeChecker.X86TypeChecker` tc: A type-checker object
	:ivar `.PF1Elt` group1pfx: A group #1 prefix or ``None``
	:ivar stem: Instruction stem
	:type stem: integer list
	:ivar `.SegElt` segpfx: A segment prefix or ``None``
	:ivar bool sizepfx: Whether an OPSIZE operand size prefix is required
	:ivar bool addrpfx: Whether an ADDRSIZE address size prefix is required
	:ivar immediates: Any operands that are encoded as bytes after the prefixes,
		stem, and optional ModRM
	:type immediates: integer list
	"""
	# We will need to type-check the instructions before we encode them, as well 
	# as consult some other type-checker functionality.
	def __init__(self):
		self.tc = X86TypeChecker()
		self.Reset()
		self.addr = 0
	
	def Reset(self):
		"""Clear all held state within the encoder object."""
		self.group1pfx = None
		self.stem = []
		self.segpfx = None
		self.addrpfx = False
		self.sizepfx = False
		self.immediates = []
		self._modrm = None
	
	@property
	def ModRM(self):
		"""A ModR/M object.  Using a property makes this very slick:  we initialize
		the object to ``None``, where a :class:`.ModRM16` or :class:`.ModRM32` 
		object is created on-the-fly the first time this member is accessed."""
		if self._modrm == None:
			self._modrm = ModRM16() if self.addrpfx else ModRM32()
		return self._modrm

	def EncodeInstruction(self,instr,addr=0):
		"""Given an instruction, look up its mnemonic in :data:`mnem_to_encodings`.
		Using the type-checker member *tc*, try to find a suitable encoding.  
		Encode the instruction with that encoding, and return the byte list.
		
		:param `.Instruction` instr: The x86 instruction to encode
		:param integer addr: The address at which to encode
		:rtype: integer list
		"""
		self.Reset()
		self.addr = addr

		# For every encoding for the instruction's mnemonic:
		for enc in X86EncodeTable.mnem_to_encodings[instr.mnem.IntValue()]:
			# See if the encoding matches, i.e. if the operands type-check.
			val = self.tc.TypeCheckInstruction_opt(instr,enc.ops)
			if val == None: 
				continue
			
			# If it matched, store the information about size, address size, and 
			# segment prefixes into the context.
			self.sizepfx = val[0]
			self.addrpfx = val[1]
			self.segpfx  = val[2]
			
			# Copy the stem bytes.
			self.stem = enc.bytes
			
			# Attend to anything special that the encoding method requires.
			enc.Encode(self)
			
			# Encode the operands by invoking self.visit on the operand and its
			# X86AOTDL object.
			for i in xrange(len(enc.ops)):
				self.visit(instr.GetOp(i),AOTtoAOTDL[enc.ops[i].IntValue()])
			
			# Start with an empty byte list.
			enc = []

			# Collect any necessary prefixes.
			if self.segpfx != None:    enc.append(PrefixOfSeg[self.segpfx])
			if self.addrpfx:           enc.append(0x67)
			if self.sizepfx:           enc.append(0x66)
			if self.group1pfx != None: enc.append(self.group1pfx)
			
			# Append the stem.
			enc += self.stem
			
			# Collect the ModRM, if present.
			if self._modrm != None:    enc += self.ModRM.Encode()
			
			# Collect the immediates, if present.
			if self.immediates != []:  enc += self.immediates
			
			# That's the entire instruction.  Return it.
			return enc

		# Otherwise, the instruction did not match any valid encoding.  Throw an
		# InvalidInstruction() exception.
		print "Couldn't encode %s" % instr
		raise InvalidInstruction()
	
	# Encode more than one instruction, updating the address as we go.
	def EncodeInstructions(self,instrs,addr=0):
		"""Encode one or more instruction using the :meth:`EncodeInstruction` 
		method.  Call it in a loop, updating the address after each instruction
		is encoded.
		
		:param instr: The list of x86 instructions to encode
		:type instr: :class:`.Instruction` list
		:param integer addr: The address at which to encode
		:rtype: integer list
		:returns: The bytes of all instructions in a single list.
		"""
		res,curraddr = [],addr
		for instr in instrs:
			enc = self.EncodeInstruction(instr,curraddr)
			curraddr += len(enc)
			res.extend(enc)
		return res

	def MakeMethodName(s,op1,enc):
		"""We override this method from the :class:`~.Visitor.Visitor` class to
		simplify the design.  Since the :class:`~.ImmEnc` can hold different types
		of operands in its *archetype* field, we separate them out into one method
		per type.  :class:`~.SignedImm` is similar.  For :class:`~.RegOrMem`, we
		have different methods depending upon whether *op1* is a 
		:class:`~.Register` object or a :class:`~.MemExpr`.
		
		:param `.Operand` op1:
		:param `.X86AOTDL` enc:
		"""
		# For immediates, append the X86 Operand class name.
		if isinstance(enc,ImmEnc):
			op = enc.archetype
			if isinstance(op,MemExpr):   return "visit_Immediate_MemExpr"
			if isinstance(op,FarTarget): return "visit_Immediate_FarTarget"
			return "visit_Immediate_%s" % op.__class__.__name__

		# For ModRM, if op1 is a Register, route it to a dedicated method.  
		# Otherwise, if op1 is a MemExpr, route it to a method named after op1's 
		# class name.
		if isinstance(enc,RegOrMem):
			suffix = "Register" if isinstance(op1,Register) else op1.__class__.__name__
			return "visit_RegOrMem_%s" % suffix
		
		# For SignExtImm, these are encoded as bytes.  Route the Immediate and
		# JccTarget operand to specialized methods.
		if isinstance(enc,SignedImm):
			op = enc.archetype
			if isinstance(op,JccTarget): return "visit_Immediate_JccTarget"
			return "visit_Immediate_Ib"

		# Otherwise, use a generic name based on the X86TypeLang class name.
		return "visit_" + enc.__class__.__name__

	def AppendImmediate(self,imm,n):
		"""Append an *n*-byte immediate *imm* to the *immediates* class member,
		as a little-endian list of bytes.
		
		:param integer imm:
		:param integer n:
		"""
		self.immediates.extend(little_endian_bytes(imm,n))

	def visit_Exact(self,op,i):            
		"""Exact operands do not need to be encoded.

		:param `.Operand` op:
		:param `.Exact` i:		
		"""		
		raise ExerciseError("X86Encoder::visit_Exact")

	def visit_ExactSeg(self,op,i): 
		"""For ExactSeg operands, we already know if a segment prefix is required
		due to type-checking.  Therefore, we do not need to do anything.

		:param `.Operand` op:
		:param `.ExactSeg` i:		
		"""		
		raise ExerciseError("X86Encoder::visit_ExactSeg")

	def visit_GPart(self,op,g):               
		"""For GPart operands, store the :class:`~.Register` object *op* 
		:meth:`~.Register.IntValue` in the *ModRM* field :attr:`.GGG`.

		:param `.Register` op:
		:param `.GPart` g:		
		"""		
		raise ExerciseError("X86Encoder::visit_GPart")

	def visit_RegOrMem_Register(self,op,m):      
		"""For RegOrMem where the *op* a :class:`~.Register`, set the ModRM field
		:attr:`.MOD` to ``3``, and field :attr:`.RM` to the :class:`~.Register` 
		object *op*'s :meth:`~.Register.IntValue`.

		:param `.Register` op:
		:param `.RegOrMem` m:		
		"""		
		raise ExerciseError("X86Encoder::visit_RegOrMem_Register")

	def visit_RegOrMem_Mem16(self,mem,m):
		"""For RegOrMem where the *op* a :class:`~.Mem16`, invoke the 
		:meth:`~.ModRM16.EncodeFromParts` method using the parts of the memory
		expression *mem*.

		:param `.Mem16` mem:
		:param `.RegOrMem` m:		
		"""		
		raise ExerciseError("X86Encoder::visit_RegOrMem_Mem16")

	def visit_RegOrMem_Mem32(self,mem,m):
		"""For RegOrMem where the *op* a :class:`~.Mem32`, invoke the 
		:meth:`~.ModRM32.EncodeFromParts` method using the parts of the memory
		expression *mem*.

		:param `.Mem32` mem:
		:param `.RegOrMem` m:		
		"""		
		raise ExerciseError("X86Encoder::visit_RegOrMem_Mem32")
		
	def visit_Immediate_MemExpr(self,op,i): 
		"""For ImmEnc where the *op* is a :class:`~.MemExpr`, write its *Disp*
		member as an immediate (``2`` bytes for :class:`~.Mem16`, ``4`` bytes for
		:class:`~.Mem32`.

		:param `.MemExpr` op:
		:param `.ImmEnc` i:		
		"""		
		raise ExerciseError("X86Encoder::visit_Immediate_MemExpr")

	def visit_Immediate_FarTarget(self,op,i):
		"""For ImmEnc where the *op* is a :class:`~.FarTarget`, write its 
		:attr:`Off` member (``2`` bytes for :class:`~.AP16`, ``4`` bytes for
		:class:`~.AP32`), followed by its ``2``-byte :attr:`Seg`.

		:param `.FarTarget` op:
		:param `.ImmEnc` i:		
		"""		
		raise ExerciseError("X86Encoder::visit_Immediate_FarTarget")

	def visit_Immediate_Ib(self,op,i): 
		"""For ImmEnc where the *op* is an :class:`~.Ib`, write its *value* member
		as an 8-bit immediate.

		:param `.Ib` op:
		:param `.ImmEnc` i:		
		"""		
		raise ExerciseError("X86Encoder::visit_Immediate_Ib")

	def visit_Immediate_Iw(self,op,i): 
		"""For ImmEnc where the *op* is an :class:`~.Iw`, write its *value* member
		as a 16-bit immediate.

		:param `.Iw` op:
		:param `.ImmEnc` i:		
		"""		
		raise ExerciseError("X86Encoder::visit_Immediate_Iw")

	def visit_Immediate_Id(self,op,i): 
		"""For ImmEnc where the *op* is an :class:`~.Id`, write its *value* member
		as a 32-bit immediate.

		:param `.Id` op:
		:param `.ImmEnc` i:		
		"""		
		raise ExerciseError("X86Encoder::visit_Immediate_Id")
		
	def visit_Immediate_JccTarget(self,op,i):
		"""For JccTargets, we treat them all as long jumps.  These are "relatively-
		addressed", meaning dependent upon the location at which it is encoded.
		The beginning of this instruction is held in the *addr* member.  We add up
		the size of the prefixes and stem so far to decide where the instruction
		ends, then subtract that from the destination address.  We use full-sized
		displacements to avoid some headaches.

		:param `.JccTarget` op:
		:param `.ImmEnc` i:		
		"""		
		# Get the address of the destination.
		dest = op._taken.value

		# If there was an address-size prefix and the destination was not 16-bit,
		# we can't encode this instruction, so throw an error.
		if self.addrpfx and dest > 0xFFFF:
			raise X86EncoderError("%s: had address prefix with 32-bit dest" % jcc)

		# Compute the length of the instruction, and the displacement.  
		# We just use the long-form (4-byte Jz) to avoid complications.
		instrlen =  (self.segpfx  != None) + (self.sizepfx == True)
		instrlen += (self.addrpfx == True) + len(self.stem) + 4
		displacement = (dest - (self.addr + instrlen)) & 0xFFFFFFFF
		self.AppendImmediate(displacement,2 if self.addrpfx else 4)

	def visit_SizePrefix(self,op,z): 
		"""Visit the appropriate child depending upon whether a size prefix is 
		present.
		
		:param `.Operand` op:
		:param `.SizePrefix` z:		
		"""
		raise ExerciseError("X86Encoder::visit_SizePrefix")

	def visit_AddrPrefix(self,op,a): 
		"""Visit the appropriate child depending upon whether an address prefix is
		present.
		
		:param `.Operand` op:
		:param `.AddrPrefix` a:		
		"""
		raise ExerciseError("X86Encoder::visit_AddrPrefix")

