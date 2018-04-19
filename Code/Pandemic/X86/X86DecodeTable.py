"""This module defines the classes for the Decoder Description Language, all of
which derive from :class:`X86DECDL`.  The actual decoding table for X86 
instructions is exported in the variable :data:`decoding_table`."""

from X86MetaData import *
from X86InternalOperand import *
from X86 import *
from Pandemic.Util.ExerciseError import ExerciseError

class X86DECDL(object):
	"""X86 Decoder Description Language (X86DECDL) base class."""
	pass

class Fatal(X86DECDL):
	"""Decoder entry corresponding to a fatal error.  The elements of 
	:data:`decoding_table` that correspond to prefix bytes have these objects
	in their place, as we should have decoded all prefix bytes prior to decoding
	the instruction itself."""
	def decode(self,decoder):
		"""Raises an error.
		
		:param `.X86Decoder.X86Decoder` decoder:
		:rtype: (:class:`~.MnemElt`, :class:`~.AOTElt` list) 
		:raises Exception: Every time it is invoked.
		"""
		print "Fatal: tried to consume prefix byte during decoding"
		raise RuntimeError

class InvalidEntry(X86DECDL):
	"""Decoder entry corresponding to an undefined instruction, of which there
	are many in the X86 instruction set."""
	def decode(self,decoder):
		"""Raises an exception.
		
		:param `.X86Decoder.X86Decoder` decoder:
		:rtype: (:class:`~.MnemElt`, :class:`~.AOTElt` list) 
		:raises: :exc:`~.InvalidInstruction` every time it is invoked.
		"""
		raise InvalidInstruction()

class Direct(X86DECDL):
	"""Decoder entry corresponding to a actual instruction.
	
	:ivar `.MnemElt` mnem: Instruction's mnemonic
	:ivar opl: List of abstract operand types (:class:`~.AOTElt`)
	:type opl: :class:`~.AOTElt` list
	"""
	def __init__(self,mnem,opl):
		self.mnem = mnem
		self.opl  = opl

	def decode(self,decoder):
		"""Return the mnemonic *mnem* and abstract operand list *opl* as a pair.
		
		:param `.X86Decoder.X86Decoder` decoder:
		:rtype: (:class:`~.MnemElt`, :class:`~.AOTElt` list) 
		"""
		return (self.mnem,self.opl)
		
class Group(X86DECDL):
	"""Decoder entry corresponding to a ModRM group.  I.e., it selects another
	decoder entry depending upon the ModRM :attr:`~.GGG` field.
	
	:ivar group: List of eight :class:`X86DECDL` objects, one for each value of
		the ModRM :attr:`~.GGG` field.
	:type group: :class:`~.X86DECDL` list
	"""
	def __init__(self,group):
		self.group = group

	def decode(self,decoder):
		"""Select one of the entries from member *group*, based upon the 
		:attr:`.GGG` member of the ModRM object held in *decoder*, and call its
		:meth:`decode` method.
		
		:param `.X86Decoder.X86Decoder` decoder:
		:rtype: (:class:`~.MnemElt`, :class:`~.AOTElt` list) 
		"""
		raise ExerciseError("X86DecodeTable::Group::Decode")
		
class RMGroup(X86DECDL):
	"""Decoder entry corresponding to an "RM group".  I.e., it selects another
	decoder entry depending upon the ModRM :attr:`~.RM` field.
	
	:ivar group: List of eight :class:`X86DECDL` objects, one for each value of
		the ModRM :attr:`~.RM` field.
	:type group: :class:`~.X86DECDL` list
	"""
	def __init__(self,group):
		self.group = group

	def decode(self,decoder):
		"""Select one of the entries from member *group*, based upon the 
		:attr:`.RM` member of the ModRM object held in *decoder*, and call its
		:meth:`decode` method.
		
		:param `.X86Decoder.X86Decoder` decoder:
		:rtype: (:class:`~.MnemElt`, :class:`~.AOTElt` list) 
		"""
		raise ExerciseError("X86DecodeTable::RMGroup::Decode")

class SSE(X86DECDL):
	"""Decoder entry for SSE instructions.  It selects one of four decoder 
	entries depending upon the REP, REPNZ, and OPSIZE prefixes.
	
	:ivar `X86DECDL` no: Entry to use with no prefixes
	:ivar `X86DECDL` rep: Entry to use with the REP prefix
	:ivar `X86DECDL` size: Entry to use with the OPSIZE prefix
	:ivar `X86DECDL` repne: Entry to use with the REPNE prefix
	"""
	def __init__(self,no,rep,size,repne):
		self.no = no
		self.rep = rep
		self.size = size
		self.repne = repne
	
		"""Select one of the entries based upon complex decoding logic, and call 
		its :meth:`decode` method.
		
		:param `.X86Decoder.X86Decoder` decoder:
		:rtype: (:class:`~.MnemElt`, :class:`~.AOTElt` list) 
		"""
	def decode(self,decoder):
		# If REP/REPNE is present, try to use them before the OPSIZE prefix.
		pfx = decoder.group1pfx
		if len(pfx) != 0:
			decoder.group1pfx = []
			try:
				# Loop until a prefix is found.
				while True:
					# Get the prefix closest to the instruction stem.
					curpfx = pfx.pop()

					# Was it REP? And is there a valid entry for REP?
					if curpfx == REP and not isinstance(self.rep,InvalidEntry):
						# If yes, decode the REP entry.
						return self.rep.decode(decoder)

					# Was it REPNE? And is there a valid entry for REPNE?
					if curpfx == REPNE and not isinstance(self.repne,InvalidEntry):
						# If yes, decode the REPNE entry.
						return self.repne.decode(decoder)

			except e,Exception:
				pass
		# If there were no Group 1 prefixes, or they didn't correspond to a
		# valid decoder entry, try the OPSIZE prefix.
		if decoder.sizepfx and not isinstance(self.size,InvalidEntry):
			return self.size.decode(decoder)
		
		# If none of that worked, decode the non-prefixed entry.
		return self.no.decode(decoder)
		
class Predicated(X86DECDL):
	"""This class of decoder entries selects between two different possibilities,
	depending upon the :meth:`cond` method.  I.e., :meth:`cond` is responsible
	for checking the state of the decoder to determine which entry -- either
	*overridden* or *regular* -- should be invoked.
	
	:ivar `X86DECDL` overridden: Entry to use when :meth:`cond` returns ``True``
	:ivar `X86DECDL` regular: Entry to use when :meth:`cond` returns ``False``
	"""
	def __init__(self,orr,reg):
		self.overridden = orr
		self.regular = reg

	def cond(self,decoder):
		"""This method is overridden in derived classes to customize which decoder
		entry is selected.
		
		:param `.X86Decoder.X86Decoder` decoder:
		:rtype: bool
		:returns: A `bool` dictating which :class:`X86DECDL` entry to use.
		"""
		print "Derived class must define"
		raise NotImplementedError
	
	def decode(self,decoder):
		"""Calls the :meth:`decode` method of either *overridden* or *regular*,
		depending upon the return value of :meth:`cond`.
		
		:param `.X86Decoder.X86Decoder` decoder:
		:rtype: (:class:`~.MnemElt`, :class:`~.AOTElt` list) 
		"""
		if self.cond(decoder): 
			return self.overridden.decode(decoder)
		return self.regular.decode(decoder)

# Predicated upon the OPSIZE prefix.
class PredOpSize(Predicated):
	"""Selects one of two decoder entries, depending upon the value of the OPSIZE
	prefix."""
	def cond(self,decoder): 
		"""Return *decoder*'s *sizepfx* field.
		
		:param `.X86Decoder.X86Decoder` decoder:
		:rtype: bool
		"""
		raise ExerciseError("X86DecodeTable::PredOpSize::cond")

# Predicated upon the ADDRSIZE prefix.
class PredAddrSize(Predicated):
	"""Selects one of two decoder entries, depending upon the value of the
	ADDRSIZE prefix."""
	def cond(self,decoder): 
		"""Return *decoder*'s *addrpfx* field.
		
		:param `.X86Decoder.X86Decoder` decoder:
		:rtype: bool
		"""
		raise ExerciseError("X86DecodeTable::PredAddrSize::cond")

# Predicated upon ModRM.MOD.
class PredMOD(Predicated):
	"""Selects one of two decoder entries, depending upon whether the ModRM
	refers to memory."""
	def cond(self,decoder): 
		"""Return ``True`` if *decoder*'s :attr:`~.X86Decoder.ModRM` refers to
		memory.
		
		:param `.X86Decoder.X86Decoder` decoder:
		:rtype: bool
		"""
		raise ExerciseError("X86DecodeTable::PredMOD::cond")

Fatal = Fatal()
Invalid = InvalidEntry()

def SSENo(no):      
	"""Shortcut to use for SSE when only the non-prefixed entry is valid."""
	return SSE(no,Invalid,Invalid,Invalid)
def SSE66(se):      
	"""Shortcut to use for SSE when only the OPSIZE prefix entry is valid."""
	return SSE(Invalid,Invalid,se,Invalid)
def SSENo66(no,se): 
	"""Shortcut to use for SSE when only the OPSIZE prefix and non-prefixed 
	entries are valid."""
	return SSE(no,Invalid,se,Invalid)

decoding_table = [
Direct(Add,[OEb,OGb]), # 0x00 *)
Direct(Add,[OEv,OGv]),
Direct(Add,[OGb,OEb]),
Direct(Add,[OGv,OEv]),
Direct(Add,[OAL,OIb]),
Direct(Add,[OrAX,OIz]),
Direct(Push,[OES]),
Direct(Pop,[OES]),
Direct(Or,[OEb,OGb]),
Direct(Or,[OEv,OGv]),
Direct(Or,[OGb,OEb]),
Direct(Or,[OGv,OEv]),
Direct(Or,[OAL,OIb]),
Direct(Or,[OrAX,OIz]),
Direct(Push,[OCS]),
Fatal,
Direct(Adc,[OEb,OGb]), # 0x10 *)
Direct(Adc,[OEv,OGv]),
Direct(Adc,[OGb,OEb]),
Direct(Adc,[OGv,OEv]),
Direct(Adc,[OAL,OIb]),
Direct(Adc,[OrAX,OIz]),
Direct(Push,[OSS]),
Direct(Pop,[OSS]),
Direct(Sbb,[OEb,OGb]),
Direct(Sbb,[OEv,OGv]),
Direct(Sbb,[OGb,OEb]),
Direct(Sbb,[OGv,OEv]),
Direct(Sbb,[OAL,OIb]),
Direct(Sbb,[OrAX,OIz]),
Direct(Push,[ODS]),
Direct(Pop,[ODS]),
Direct(And,[OEb,OGb]), # 0x20 *)
Direct(And,[OEv,OGv]),
Direct(And,[OGb,OEb]),
Direct(And,[OGv,OEv]),
Direct(And,[OAL,OIb]),
Direct(And,[OrAX,OIz]),
Fatal,
Direct(Daa,[]),
Direct(Sub,[OEb,OGb]),
Direct(Sub,[OEv,OGv]),
Direct(Sub,[OGb,OEb]),
Direct(Sub,[OGv,OEv]),
Direct(Sub,[OAL,OIb]),
Direct(Sub,[OrAX,OIz]),
Fatal,
Direct(Das,[]),
Direct(Xor,[OEb,OGb]), # 0x30 *)
Direct(Xor,[OEv,OGv]),
Direct(Xor,[OGb,OEb]),
Direct(Xor,[OGv,OEv]),
Direct(Xor,[OAL,OIb]),
Direct(Xor,[OrAX,OIz]),
Fatal,
Direct(Aaa,[]),
Direct(Cmp,[OEb,OGb]),
Direct(Cmp,[OEv,OGv]),
Direct(Cmp,[OGb,OEb]),
Direct(Cmp,[OGv,OEv]),
Direct(Cmp,[OAL,OIb]),
Direct(Cmp,[OrAX,OIz]),
Fatal,
Direct(Aas,[]),
Direct(Inc,[OeAX]),    # 0x40 *)
Direct(Inc,[OeCX]),
Direct(Inc,[OeDX]),
Direct(Inc,[OeBX]),
Direct(Inc,[OeSP]),
Direct(Inc,[OeBP]),
Direct(Inc,[OeSI]),
Direct(Inc,[OeDI]),
Direct(Dec,[OeAX]),
Direct(Dec,[OeCX]),
Direct(Dec,[OeDX]),
Direct(Dec,[OeBX]),
Direct(Dec,[OeSP]),
Direct(Dec,[OeBP]),
Direct(Dec,[OeSI]),
Direct(Dec,[OeDI]),
Direct(Push,[OrAXr8]),    # 0x50 *)
Direct(Push,[OrCXr9]),
Direct(Push,[OrDXr10]),
Direct(Push,[OrBXr11]),
Direct(Push,[OrSPr12]),
Direct(Push,[OrBPr13]),
Direct(Push,[OrSIr14]),
Direct(Push,[OrDIr15]),
Direct(Pop,[OrAXr8]),
Direct(Pop,[OrCXr9]),
Direct(Pop,[OrDXr10]),
Direct(Pop,[OrBXr11]),
Direct(Pop,[OrSPr12]),
Direct(Pop,[OrBPr13]),
Direct(Pop,[OrSIr14]),
Direct(Pop,[OrDIr15]),
PredOpSize(Direct(Pushaw,[]),Direct(Pushad,[])), # 0x60 *)
PredOpSize(Direct(Popaw,[]), Direct(Popad,[])),
Direct(Bound,[OGv,OMa]),
Direct(Arpl,[OEw,OGw]),
Fatal,
Fatal,
Fatal,
Fatal,
Direct(Push,[OIz]),
Direct(Imul,[OGv,OEv,OIz]),
Direct(Push,[OIbv]),
Direct(Imul,[OGv,OEv,OIb]),
Direct(Insb,[OYb,ODX]),
PredOpSize(Direct(Insw,[OYz,ODX]),Direct(Insd,[OYz,ODX])), # Insw /Insd, [OYz,ODX] -- Mnem changes, given a mode *)
Direct(Outsb,[ODX,OXb]),
PredOpSize(Direct(Outsw,[ODX,OXz]),Direct(Outsd,[ODX,OXz])), # Outsw /Outsd, [ODX,OXz] -- Mnem changes, given a mode *)
Direct(Jo ,[OJb]), # 0x70 *)
Direct(Jno,[OJb]),
Direct(Jb ,[OJb]),
Direct(Jae,[OJb]),
Direct(Jz ,[OJb]),
Direct(Jnz,[OJb]),
Direct(Jbe,[OJb]),
Direct(Ja ,[OJb]),
Direct(Js ,[OJb]),
Direct(Jns,[OJb]),
Direct(Jp ,[OJb]),
Direct(Jnp,[OJb]),
Direct(Jl ,[OJb]),
Direct(Jge,[OJb]),
Direct(Jle,[OJb]),
Direct(Jg ,[OJb]),
Group([Direct(Add,[OEb,OIb]), Direct(Or,[OEb,OIb]), Direct(Adc,[OEb,OIb]), Direct(Sbb,[OEb,OIb]), Direct(And,[OEb,OIb]), Direct(Sub,[OEb,OIb]), Direct(Xor,[OEb,OIb]), Direct(Cmp,[OEb,OIb])]), # 0x80 *)
Group([Direct(Add,[OEv,OIz]), Direct(Or,[OEv,OIz]), Direct(Adc,[OEv,OIz]), Direct(Sbb,[OEv,OIz]), Direct(And,[OEv,OIz]), Direct(Sub,[OEv,OIz]), Direct(Xor,[OEv,OIz]), Direct(Cmp,[OEv,OIz])]),
Group([Direct(Add,[OEb,OIb]), Direct(Or,[OEb,OIb]), Direct(Adc,[OEb,OIb]), Direct(Sbb,[OEb,OIb]), Direct(And,[OEb,OIb]), Direct(Sub,[OEb,OIb]), Direct(Xor,[OEb,OIb]), Direct(Cmp,[OEb,OIb])]),
Group([Direct(Add,[OEv,OIbv]),Direct(Or,[OEv,OIbv]),Direct(Adc,[OEv,OIbv]),Direct(Sbb,[OEv,OIbv]),Direct(And,[OEv,OIbv]),Direct(Sub,[OEv,OIbv]),Direct(Xor,[OEv,OIbv]),Direct(Cmp,[OEv,OIbv])]),
Direct(Test,[OEb,OGb]),
Direct(Test,[OEv,OGv]),
Direct(Xchg,[OEb,OGb]),
Direct(Xchg,[OEv,OGv]),
Direct(Mov,[OEb,OGb]),
Direct(Mov,[OEv,OGv]),
Direct(Mov,[OGb,OEb]),
Direct(Mov,[OGv,OEv]),
Direct(Mov,[OEv,OSw]),
Direct(Lea,[OGv,OM]),
Direct(Mov,[OSw,OEw]),
Group([Direct(Pop,[OEv]),Invalid,Invalid,Invalid,Invalid,Invalid,Invalid,Invalid]),
SSE(Direct(Nop,[]),Direct(Pause,[]),Direct(Nop,[]),Direct(Nop,[])), # 0x90 *)
Direct(Xchg,[OrAX,OrCXr9]),
Direct(Xchg,[OrAX,OrDXr10]),
Direct(Xchg,[OrAX,OrBXr11]),
Direct(Xchg,[OrAX,OrSPr12]),
Direct(Xchg,[OrAX,OrBPr13]),
Direct(Xchg,[OrAX,OrSIr14]),
Direct(Xchg,[OrAX,OrDIr15]),
PredOpSize(Direct(Cbw,[]),Direct(Cwde,[])), # CBW/CWDE/CDQE *)
PredOpSize(Direct(Cwd,[]),Direct(Cdq,[])),  # CWD/CDQ/CQO *)
Direct(CallF,[OAp]),
Direct(Wait,[]),
PredOpSize(Direct(Pushfw,[]),Direct(Pushfd,[])), # PUSHF/D/Q *)
PredOpSize(Direct(Popfw,[]), Direct(Popfd,[])), # POPF/D/Q *)
Direct(Sahf,[]),
Direct(Lahf,[]),
Direct(Mov,[OAL,OOb]),  # 0xA0 *)
Direct(Mov,[OrAX,OOv]),
Direct(Mov,[OOb,OAL]),
Direct(Mov,[OOv,OrAX]),
Direct(Movsb,[OXb,OYb]),
PredOpSize(Direct(Movsw,[OXv,OYv]),Direct(Movsd,[OXv,OYv])), # MOVS/W/D/Q *)
Direct(Cmpsb,[OXb,OYb]),
PredOpSize(Direct(Cmpsw,[OXv,OYv]),Direct(Cmpsd,[OXv,OYv])), # CMPS/W/D/Q *)
Direct(Test,[OAL,OIb]),
Direct(Test,[OrAX,OIz]),
Direct(Stosb,[OYb]),
PredOpSize(Direct(Stosw,[OYv]),Direct(Stosd,[OYv])), # STOS/W/D/Q *)
Direct(Lodsb,[OXb]),
PredOpSize(Direct(Lodsw,[OXv]),Direct(Lodsd,[OXv])), # LODS/W/D/Q *)
Direct(Scasb,[OYb]),
PredOpSize(Direct(Scasw,[OYv]),Direct(Scasd,[OYv])), # SCAS/W/D/Q *)
Direct(Mov,[OALR8L,OIb]), # 0xB0 *)
Direct(Mov,[OCLR9L,OIb]),
Direct(Mov,[ODLR10L,OIb]),
Direct(Mov,[OBLR11L,OIb]),
Direct(Mov,[OAHR12L,OIb]),
Direct(Mov,[OCHR13L,OIb]),
Direct(Mov,[ODHR14L,OIb]),
Direct(Mov,[OBHR15L,OIb]),
Direct(Mov,[OrAXr8,OIv]),
Direct(Mov,[OrCXr9,OIv]),
Direct(Mov,[OrDXr10,OIv]),
Direct(Mov,[OrBXr11,OIv]),
Direct(Mov,[OrSPr12,OIv]),
Direct(Mov,[OrBPr13,OIv]),
Direct(Mov,[OrSIr14,OIv]),
Direct(Mov,[OrDIr15,OIv]),
Group([Direct(Rol,[OEb,OIb]),Direct(Ror,[OEb,OIb]),Direct(Rcl,[OEb,OIb]),Direct(Rcr,[OEb,OIb]),Direct(Shl,[OEb,OIb]),Direct(Shr,[OEb,OIb]),Direct(Sal,[OEb,OIb]),Direct(Sar,[OEb,OIb])]), # 0xC0 *)
Group([Direct(Rol,[OEv,OIb]),Direct(Ror,[OEv,OIb]),Direct(Rcl,[OEv,OIb]),Direct(Rcr,[OEv,OIb]),Direct(Shl,[OEv,OIb]),Direct(Shr,[OEv,OIb]),Direct(Sal,[OEv,OIb]),Direct(Sar,[OEv,OIb])]),
Direct(Ret,[OIw]),
Direct(Ret,[]),
Direct(Les,[OGz,OMp]),
Direct(Lds,[OGz,OMp]),
Group([Direct(Mov,[OEb,OIb]),Invalid,Invalid,Invalid,Invalid,Invalid,Invalid,Invalid]),
Group([Direct(Mov,[OEv,OIz]),Invalid,Invalid,Invalid,Invalid,Invalid,Invalid,Invalid]),
Direct(Enter,[OIw,OIb]),
Direct(Leave,[]),
Direct(Retf,[OIw]),
Direct(Retf,[]),
Direct(Int3,[]),
Direct(Int,[OIb]),
Direct(Into,[]),
PredOpSize(Direct(Iretw,[]),Direct(Iretd,[])), # Revisit for 64-bit *)
Group([Direct(Rol,[OEb,O1 ]),Direct(Ror,[OEb,O1 ]),Direct(Rcl,[OEb,O1 ]),Direct(Rcr,[OEb,O1 ]),Direct(Shl,[OEb,O1 ]),Direct(Shr,[OEb,O1 ]),Direct(Sal,[OEb,O1 ]),Direct(Sar,[OEb,O1 ])]), # 0xD0 *)
Group([Direct(Rol,[OEv,O1 ]),Direct(Ror,[OEv,O1 ]),Direct(Rcl,[OEv,O1 ]),Direct(Rcr,[OEv,O1 ]),Direct(Shl,[OEv,O1 ]),Direct(Shr,[OEv,O1 ]),Direct(Sal,[OEv,O1 ]),Direct(Sar,[OEv,O1 ])]),
Group([Direct(Rol,[OEb,OCL]),Direct(Ror,[OEb,OCL]),Direct(Rcl,[OEb,OCL]),Direct(Rcr,[OEb,OCL]),Direct(Shl,[OEb,OCL]),Direct(Shr,[OEb,OCL]),Direct(Sal,[OEb,OCL]),Direct(Sar,[OEb,OCL])]),
Group([Direct(Rol,[OEv,OCL]),Direct(Ror,[OEv,OCL]),Direct(Rcl,[OEv,OCL]),Direct(Rcr,[OEv,OCL]),Direct(Shl,[OEv,OCL]),Direct(Shr,[OEv,OCL]),Direct(Sal,[OEv,OCL]),Direct(Sar,[OEv,OCL])]),
Direct(Aam,[OIb]),
Direct(Aad,[OIb]),
Direct(Salc,[]),
PredAddrSize(Direct(Xlat,[OMbBx]),Direct(Xlat,[OMbEbx])),

#
#   High-level viewpoint on FPU encoding:
#   * All FPU encodings are broken down into two cases:  those where the Mod/RM 
#     specifies a:
#   * * Memory location
#   * * Register
#   * When there's a memory location, the register field of the mod/rm specifies
#     an instruction in a sparsely-populated (but normally completely full) array,
#     which takes at least one of its arguments as specified by the memory 
#     expression dictated by the rest of the mod/rm encoding.
#   * When there's a register, the Intel manuals divide the outcome up into eight 
#     octants, specified by the register field of the mod/rm byte.  These octants 
#     are either monolithic blocks of instructions that operate on the FPU 
#     registers (where the eight ST(N) registers are selected by the low three bits 
#     of the mod/rm byte), or are sparsely-populated ranges of instructions that
#     take no operands.

# 0xD8 *)
PredMOD(
  Group([
    Direct(Fadd, [OSt0,OReal4]),
    Direct(Fmul, [OSt0,OReal4]),
    Direct(Fcom, [OSt0,OReal4]),
    Direct(Fcomp,[OSt0,OReal4]),
    Direct(Fsub, [OSt0,OReal4]),
    Direct(Fsubr,[OSt0,OReal4]),
    Direct(Fdiv, [OSt0,OReal4]),
    Direct(Fdivr,[OSt0,OReal4])]),
  Group([
    Direct(Fadd, [OSt0,OStN]),
    Direct(Fmul, [OSt0,OStN]),
    Direct(Fcom, [OSt0,OStN]),
    Direct(Fcomp,[OSt0,OStN]),
    Direct(Fsub, [OSt0,OStN]),
    Direct(Fsubr,[OSt0,OStN]),
    Direct(Fdiv, [OSt0,OStN]),
    Direct(Fdivr,[OSt0,OStN])])),
    
# 0xD9 *)
PredMOD(
  Group([
    Direct(Fld,   [OReal4]),
    Invalid,
    Direct(Fst,   [OReal4]),
    Direct(Fstp,  [OReal4]),
    Direct(Fldenv,[OFPEnvLow]),
    Direct(Fldcw, [OMw]),
    Direct(Fstenv,[OFPEnvLow]),
    Direct(Fstcw, [OMw])]),
  Group([
    Direct(Fld, [OSt0,OStN]),
    Direct(Fxch,[OSt0,OStN]),
    RMGroup([Direct(Fnop,[]),Invalid,Invalid,Invalid,Invalid,Invalid,Invalid,Invalid]),
    Invalid,
    RMGroup([Direct(Fchs,[]),Direct(Fabs,[]),Invalid,Invalid,Direct(Ftst,[]),Direct(Fxam,[]),Invalid,Invalid]),
    RMGroup([
      Direct(Fld1,[]),
      Direct(Fldl2t,[]),
      Direct(Fldl2e,[]),
      Direct(Fldpi,[]),
      Direct(Fldlg2,[]),
      Direct(Fldln2,[]),
      Direct(Fldz,[]),
      Invalid]),
    RMGroup([
      Direct(F2xm1,[]),
      Direct(Fyl2x,[]),
      Direct(Fptan,[]),
      Direct(Fpatan,[]),
      Direct(Fxtract,[]),
      Direct(Fprem1,[]),
      Direct(Fdecstp,[]),
      Direct(Fincstp,[])]),
    RMGroup([
      Direct(Fprem,[]),
      Direct(Fyl2xp1,[]),
      Direct(Fsqrt,[]),
      Direct(Fsincos,[]),
      Direct(Frndint,[]),
      Direct(Fscale,[]),
      Direct(Fsin,[]),
      Direct(Fcos,[])])])),

# 0xDA *)
PredMOD(
  Group([
    Direct(Fiadd, [OMd]),
    Direct(Fimul, [OMd]),
    Direct(Ficom, [OMd]),
    Direct(Ficomp,[OMd]),
    Direct(Fisub, [OMd]),
    Direct(Fisubr,[OMd]),
    Direct(Fidiv, [OMd]),
    Direct(Fidivr,[OMd])]),
  Group([
    Direct(Fcmovb, [OSt0,OStN]),
    Direct(Fcmove, [OSt0,OStN]),
    Direct(Fcmovbe,[OSt0,OStN]),
    Direct(Fcmovu, [OSt0,OStN]),
    Invalid,
    RMGroup([Invalid,Direct(Fucompp,[]),Invalid,Invalid,Invalid,Invalid,Invalid,Invalid]),
    Invalid,
    Invalid])),

# 0xDB *)
PredMOD(
  Group([
    Direct(Fild,  [OMd]),
    Direct(Fisttp,[OMd]),
    Direct(Fist,  [OMd]),
    Direct(Fistp, [OMd]),
    Invalid,
    Direct(Fld,   [OReal10]),
    Invalid,
    Direct(Fstp,  [OReal10])]),
  Group([
    Direct(Fcmovnb, [OSt0,OStN]),
    Direct(Fcmovne, [OSt0,OStN]),
    Direct(Fcmovnbe,[OSt0,OStN]),
    Direct(Fcmovnu, [OSt0,OStN]),
    RMGroup([Invalid,Invalid,Direct(Fclex,[]),Direct(Finit,[]),Invalid,Invalid,Invalid,Invalid]),
    Direct(Fucomi,[OSt0,OStN]),
    Direct(Fcomi, [OSt0,OStN]),
    Invalid
    ])),

PredMOD(
  Group([
    Direct(Fadd, [OSt0,OReal8]),
    Direct(Fmul, [OSt0,OReal8]),
    Direct(Fcom, [OSt0,OReal8]),
    Direct(Fcomp,[OSt0,OReal8]),
    Direct(Fsub, [OSt0,OReal8]),
    Direct(Fsubr,[OSt0,OReal8]),
    Direct(Fdiv, [OSt0,OReal8]),
    Direct(Fdivr,[OSt0,OReal8])]),
  Group([
    Direct(Fadd, [OStN,OSt0]),
    Direct(Fmul, [OStN,OSt0]),
    Invalid,
    Invalid,
    Direct(Fsub, [OStN,OSt0]),
    Direct(Fsubr,[OStN,OSt0]),
    Direct(Fdiv, [OStN,OSt0]),
    Direct(Fdivr,[OStN,OSt0])])),

PredMOD(
  Group([
    Direct(Fld,   [OReal8]),
    Direct(Fisttp,[OMq]),
    Direct(Fst,   [OReal8]),
    Direct(Fstp,  [OReal8]),
    Direct(Frstor,[OFPEnv]),
    Invalid,
    Direct(Fsave ,[OFPEnv]),
    Direct(Fstsw, [OMw])]),
  Group([
    Direct(Ffree, [OStN]),
    Invalid,
    Direct(Fst,   [OStN]),
    Direct(Fstp,  [OStN]),
    Direct(Fucom, [OStN]),
    Direct(Fucomp,[OStN]),
    Invalid,
    Invalid])),

PredMOD(
  Group([
    Direct(Fiadd, [OMw]),
    Direct(Fimul, [OMw]),
    Direct(Ficom, [OMw]),
    Direct(Ficomp,[OMw]),
    Direct(Fisub, [OMw]),
    Direct(Fisubr,[OMw]),
    Direct(Fidiv, [OMw]),
    Direct(Fidivr,[OMw])]),
  Group([
    Direct(Faddp, [OStN,OSt0]),
    Direct(Fmulp, [OStN,OSt0]),
    Invalid,
    RMGroup([Invalid,Direct(Fcompp,[]),Invalid,Invalid,Invalid,Invalid,Invalid,Invalid]),
    Direct(Fsubrp,[OStN,OSt0]),
    Direct(Fsubp, [OStN,OSt0]),
    Direct(Fdivrp,[OStN,OSt0]),
    Direct(Fdivp, [OStN,OSt0])])),
    
PredMOD(
  Group([
    Direct(Fild,  [OMw]),
    Direct(Fisttp,[OMw]),
    Direct(Fist,  [OMw]),
    Direct(Fistp, [OMw]),
    Direct(Fbld,  [OReal10]),
    Direct(Fild,  [OReal8]),
    Direct(Fbstp, [OReal10]),
    Direct(Fistp, [OReal8])]),
  Group([
    Invalid,
    Invalid,
    Invalid,
    Invalid,
    RMGroup([Direct(Fstsw,[OAX]),Invalid,Invalid,Invalid,Invalid,Invalid,Invalid,Invalid]),
    Direct(Fucomip,[OSt0,OStN]),
    Direct(Fcomip, [OSt0,OStN]),
    Invalid])),

Direct(Loopnz,[OJb]), # 0xE0 *)
Direct(Loopz,[OJb]),
Direct(Loop,[OJb]),
PredAddrSize(Direct(Jcxz,[OJb]),Direct(Jecxz,[OJb])),
Direct(In,[OAL,OIb]),
Direct(In,[OeAX,OIb]),
Direct(Out,[OIb,OAL]),
Direct(Out,[OIb,OeAX]),
Direct(Call,[OJz]),
Direct(Jmp,[OJz]),
Direct(JmpF,[OAp]),
Direct(Jmp,[OJb]),
Direct(In,[OAL,ODX]),
Direct(In,[OeAX,ODX]),
Direct(Out,[ODX,OAL]),
Direct(Out,[ODX,OeAX]),
Fatal, # 0xF0 *)
Direct(Icebp,[]),
Fatal,
Fatal,
Direct(Hlt,[]),
Direct(Cmc,[]),
Group([Direct(Test,[OEb,OIb]),Invalid,Direct(Not,[OEb]),Direct(Neg,[OEb]),Direct(Mul,[OEb]),Direct(Imul,[OEb]),Direct(Div,[OEb]),Direct(Idiv,[OEb])]),
Group([Direct(Test,[OEv,OIz]),Invalid,Direct(Not,[OEv]),Direct(Neg,[OEv]),Direct(Mul,[OEv]),Direct(Imul,[OEv]),Direct(Div,[OEv]),Direct(Idiv,[OEv])]),
Direct(Clc,[]),
Direct(Stc,[]),
Direct(Cli,[]),
Direct(Sti,[]),
Direct(Cld,[]),
Direct(Std,[]),
Group([Direct(Inc,[OEb]),Direct(Dec,[OEb]),Invalid,Invalid,Invalid,Invalid,Invalid,Invalid]),
Group([Direct(Inc,[OEv]),Direct(Dec,[OEv]),Direct(Call,[OEv]),Direct(CallF,[OEv]),Direct(Jmp,[OEv]),Direct(JmpF,[OEv]),Direct(Push,[OEv]),Invalid]),

Group([ # 0x100 *)
  PredMOD(Direct(Sldt,[OMw]),Direct(Sldt,[ORv])),
  PredMOD(Direct(Str ,[OMw]),Direct(Str ,[ORv])),
  Direct(Lldt,[OEw]),
  Direct(Ltr ,[OEw]),
  Direct(Verr,[OEw]),
  Direct(Verw,[OEw]),
  Invalid,
  Invalid]),

PredMOD(
  Group([
    Direct(Sgdt,[OMs]),
    Direct(Sidt,[OMs]),
    Direct(Lgdt,[OMs]),
    Direct(Lidt,[OMs]),
    Direct(Smsw,[OMw]),
    Invalid,
    Direct(Lmsw,[OMw]),
    Direct(Invlpg,[OMb])]),
  Group([
    RMGroup([
      Invalid,
      Direct(Vmcall,[]),
      Direct(Vmlaunch,[]),
      Direct(Vmresume,[]),
      Direct(Vmxoff,[]),
      Invalid,
      Invalid,
      Invalid]),
    RMGroup([Direct(Monitor,[]),Direct(Mwait,[]),Invalid,Invalid,Invalid,Invalid,Invalid,Invalid]),
    Invalid,
    Invalid,
    Direct(Smsw,[ORv]),
    Invalid,
    Direct(Lmsw,[ORw]),
    Invalid, # Revisit for 64-bit (swapgs) *)
    ])),

Direct(Lar,[OGv,OEw]),
Direct(Lsl,[OGv,OEw]),
Invalid,
Direct(Syscall,[]),
Direct(Clts,[]),
Direct(Sysret,[]),
Direct(Invd,[]),
Direct(Wbinvd,[]),
Invalid,
Direct(Ud2,[]),
Invalid,
Direct(Nop,[OEv]),
Invalid,
Invalid,
SSE(Direct(Movups,[OVps,OWps]),Direct(Movss, [OVss,OWss]),Direct(Movupd,[OVpd,OWpd]),Direct(Movsd, [OVsd,OWsd])), # 0x110 *)
SSE(Direct(Movups,[OWps,OVps]),Direct(Movss, [OWss,OVss]),Direct(Movupd,[OWpd,OVpd]),Direct(Movsd, [OWsd,OVsd])),
SSE(PredMOD(Direct(Movlps,[OVq,OMq]),Direct(Movhlps,[OVq,OUq])),Direct(Movsldup,[OVq,OWq]),Direct(Movlpd,[OVq,OMq]),Direct(Movddup,[OVq,OWq])),
SSENo66(Direct(Movlps,[OMq,OVq]),Direct(Movlpd,[OMq,OVq])),
SSENo66(Direct(Unpcklpd,[OVpd,OWq]),Direct(Unpcklps,[OVps,OWq])),
SSENo66(Direct(Unpckhpd,[OVpd,OWq]),Direct(Unpckhps,[OVps,OWq])),
SSE(PredMOD(Direct(Movhps,[OVq,OMq]),Direct(Movlhps,[OVq,OUq])),Direct(Movshdup,[OVq,OWq]),Direct(Movhpd,[OVq,OMq]),Invalid),
SSENo66(Direct(Movhps,[OMq,OVq]),Direct(Movhpd,[OMq,OVq])),
PredMOD(Group([Direct(Prefetchnta,[OMb]),Direct(Prefetcht0,[OMb]),Direct(Prefetcht1,[OMb]),Direct(Prefetcht2,[OMb]),Invalid,Invalid,Invalid,Invalid]),Invalid),
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Direct(Nop,[OEv]),
Direct(Mov,[ORd,OCd]), # 0x120 *)
Direct(Mov,[ORd,ODd]),
Direct(Mov,[OCd,ORd]),
Direct(Mov,[ODd,ORd]),
Invalid,
Invalid,
Invalid,
Invalid,
SSENo66(Direct(Movaps,[OVpd,OWpd]),Direct(Movapd,[OVps,OWps])),
SSENo66(Direct(Movaps,[OWpd,OVpd]),Direct(Movapd,[OWps,OVps])),
SSE(Direct(Cvtpi2ps,[OVps,OQpi]),Direct(Cvtsi2ss,[OVss,OEd_q]),Direct(Cvtpi2pd,[OVpd,OQpi]),Direct(Cvtsi2sd,[OVsd,OEd_q])),
SSENo66(Direct(Movntps,[OMpd,OVpd]),Direct(Movntpd,[OMps,OVps])),
SSE(Direct(Cvttps2pi,[OPpi,OWps]),Direct(Cvttss2si,[OGd,OWss]),Direct(Cvttpd2pi,[OPpi,OWpd]),Direct(Cvttsd2si,[OGd,OWsd])),
SSE(Direct(Cvtps2pi,[OPpi,OWps]),Direct(Cvtss2si,[OGd_q,OWss]),Direct(Cvtpd2pi,[OPpi,OWpd]),Direct(Cvtsd2si,[OGd_q,OWsd])),
SSENo66(Direct(Ucomiss,[OVsd,OWsd]),Direct(Ucomisd,[OVss,OWss])),
SSENo66(Direct(Comiss, [OVsd,OWsd]),Direct(Comisd, [OVss,OWss])),
Direct(Wrmsr,[]), # 0x130 *) 
Direct(Rdtsc,[]),
Direct(Rdmsr,[]),
Direct(Rdpmc,[]),
Direct(Sysenter,[]),
Direct(Sysexit,[]),
Invalid,
Direct(Getsec,[]),
Fatal, 
Invalid,
Fatal,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Direct(Cmovo ,[OGv,OEv]), # 0x140 *)
Direct(Cmovno,[OGv,OEv]),
Direct(Cmovb ,[OGv,OEv]),
Direct(Cmovae,[OGv,OEv]),
Direct(Cmovz ,[OGv,OEv]),
Direct(Cmovnz,[OGv,OEv]),
Direct(Cmovbe,[OGv,OEv]),
Direct(Cmova ,[OGv,OEv]),
Direct(Cmovs ,[OGv,OEv]),
Direct(Cmovns,[OGv,OEv]),
Direct(Cmovp ,[OGv,OEv]),
Direct(Cmovnp,[OGv,OEv]),
Direct(Cmovl ,[OGv,OEv]),
Direct(Cmovge,[OGv,OEv]),
Direct(Cmovle,[OGv,OEv]),
Direct(Cmovg ,[OGv,OEv]),
SSENo66(Direct(Movmskps,[OGd,OUps]),Direct(Movmskpd,[OGd,OUpd])), # 0x150 *)
SSE(Direct(Sqrtps,    [OVps,OWps]),Direct(Sqrtss,   [OVss,OWss]),Direct(Sqrtpd,    [OVpd,OWpd]),Direct(Sqrtsd,  [OVsd,OWsd])),
SSE(Direct(Rsqrtps,   [OVps,OWps]),Direct(Rsqrtss,  [OVss,OWss]),Invalid,                       Invalid),
SSE(Direct(Rcpps,     [OVps,OWps]),Direct(Rcpss,    [OVss,OWss]),Invalid,                       Invalid),
SSENo66(Direct(Andps, [OVps,OWps]),Direct(Andpd,    [OVpd,OWpd])),
SSENo66(Direct(Andnps,[OVps,OWps]),Direct(Andnpd,   [OVpd,OWpd])),
SSENo66(Direct(Orps,  [OVps,OWps]),Direct(Orpd,     [OVpd,OWpd])),
SSENo66(Direct(Xorps, [OVps,OWps]),Direct(Xorpd,    [OVpd,OWpd])),
SSE(Direct(Addps,     [OVps,OWps]),Direct(Addss,    [OVss,OWss]),Direct(Addpd,     [OVpd,OWpd]),Direct(Addsd,   [OVsd,OWsd])),
SSE(Direct(Mulps,     [OVps,OWps]),Direct(Mulss,    [OVss,OWss]),Direct(Mulpd,     [OVpd,OWpd]),Direct(Mulsd,   [OVsd,OWsd])),
SSE(Direct(Cvtps2pd,  [OVpd,OWps]),Direct(Cvtss2sd, [OVss,OWss]),Direct(Cvtpd2ps,  [OVps,OWpd]),Direct(Cvtsd2ss,[OVsd,OWsd])),
SSE(Direct(Cvtdq2ps,  [OVps,OWps]),Direct(Cvttps2dq,[OVdq,OWps]),Direct(Cvtps2dq,  [OVdq,OWps]),Invalid),
SSE(Direct(Subps,     [OVps,OWps]),Direct(Subss,    [OVss,OWss]),Direct(Subpd,     [OVpd,OWpd]),Direct(Subsd,   [OVsd,OWsd])),
SSE(Direct(Minps,     [OVps,OWps]),Direct(Minss,    [OVss,OWss]),Direct(Minpd,     [OVpd,OWpd]),Direct(Minsd,   [OVsd,OWsd])),
SSE(Direct(Divps,     [OVps,OWps]),Direct(Divss,    [OVss,OWss]),Direct(Divpd,     [OVpd,OWpd]),Direct(Divsd,   [OVsd,OWsd])),
SSE(Direct(Maxps,     [OVps,OWps]),Direct(Maxss,    [OVss,OWss]),Direct(Maxpd,     [OVpd,OWpd]),Direct(Maxsd,   [OVsd,OWsd])),
SSENo66(Direct(Punpcklbw,[OPq,OQd]),Direct(Punpcklbw,[OVdq,OWdq])), # 0x160 *)
SSENo66(Direct(Punpcklwd,[OPq,OQd]),Direct(Punpcklwd,[OVdq,OWdq])),
SSENo66(Direct(Punpckldq,[OPq,OQd]),Direct(Punpckldq,[OVdq,OWdq])),
SSENo66(Direct(Packsswb, [OPq,OQd]),Direct(Packsswb, [OVdq,OWdq])),
SSENo66(Direct(Pcmpgtb,  [OPq,OQd]),Direct(Pcmpgtb,  [OVdq,OWdq])),
SSENo66(Direct(Pcmpgtw,  [OPq,OQd]),Direct(Pcmpgtw,  [OVdq,OWdq])),
SSENo66(Direct(Pcmpgtd,  [OPq,OQd]),Direct(Pcmpgtd,  [OVdq,OWdq])),
SSENo66(Direct(Packuswb, [OPq,OQd]),Direct(Packuswb, [OVdq,OWdq])),
SSENo66(Direct(Punpckhbw,[OPq,OQd]),Direct(Punpckhbw,[OVdq,OWdq])),
SSENo66(Direct(Punpckhwd,[OPq,OQd]),Direct(Punpckhwd,[OVdq,OWdq])),
SSENo66(Direct(Punpckhdq,[OPq,OQd]),Direct(Punpckhdq,[OVdq,OWdq])),
SSENo66(Direct(Packssdw, [OPq,OQd]),Direct(Packssdw, [OVdq,OWdq])),
SSE66(Direct(Punpcklqdq,[OVdq,OWdq])),
SSE66(Direct(Punpckhqdq,[OVdq,OWdq])),
SSENo66(Direct(Movd,[OPd,OEd_q]),Direct(Movd,[OVdq,OEd_q])),  # Revisit on 64-bit *)
SSE(Direct(Movq,     [OPq ,OQq ]),Direct(Movdqu,   [OVdq,OWdq]),Direct(Movdqa,    [OVdq,OWdq]),Invalid),
SSE(Direct(Pshufw,   [OPq,OQq,OIb]),Direct(Pshufhw,[OVdq,OWdq,OIb]),Direct(Pshufd,[OVdq,OWdq,OIb]),Direct(Pshuflw,[OVdq,OWdq,OIb])),# 0x170 *)

PredMOD(
  Invalid,
  Group([
    Invalid,
    Invalid,
    SSENo66(Direct(Psrlw,[ONq,OIb]),Direct(Psrlw,[OUdq,OIb])),
    Invalid,
    SSENo66(Direct(Psraw,[ONq,OIb]),Direct(Psraw,[OUdq,OIb])),
    Invalid,
    SSENo66(Direct(Psllw,[ONq,OIb]),Direct(Psllw,[OUdq,OIb])),
    Invalid])),

PredMOD(
  Invalid,
  Group([
    Invalid,
    Invalid,
    SSENo66(Direct(Psrld,[ONq,OIb]),Direct(Psrld,[OUdq,OIb])),
    Invalid,
    SSENo66(Direct(Psrad,[ONq,OIb]),Direct(Psrad,[OUdq,OIb])),
    Invalid,
    SSENo66(Direct(Pslld,[ONq,OIb]),Direct(Pslld,[OUdq,OIb])),
    Invalid])),

PredMOD(
  Invalid,
  Group([
    Invalid,
    Invalid,
    SSENo66(Direct(Psrlq,[ONq,OIb]),Direct(Psrlq,[OUdq,OIb])),
    SSE66(Direct(Psrldq,[OUdq,OIb])),
    Invalid,
    Invalid,
    SSENo66(Direct(Psllq,[ONq,OIb]),Direct(Psllq,[OUdq,OIb])),
    SSE66(Direct(Pslldq,[OUdq,OIb]))])),

SSENo66(Direct(Pcmpeqb,[OPq,OQq]),Direct(Pcmpeqb,[OVdq,OWdq])),
SSENo66(Direct(Pcmpeqw,[OPq,OQq]),Direct(Pcmpeqw,[OVdq,OWdq])),
SSENo66(Direct(Pcmpeqd,[OPq,OQq]),Direct(Pcmpeqd,[OVdq,OWdq])),
Direct(Emms,[]),
Direct(Vmread,[OEd,OGd]),  # revisit for 64-bit *)
Direct(Vmwrite,[OEd,OGd]), # revisit for 64-bit *)
Invalid,
Invalid,
SSE(Invalid,Invalid,Direct(Haddpd,[OVpd,OWpd]),Direct(Haddps,[OVps,OWps])),
SSE(Invalid,Invalid,Direct(Hsubpd,[OVpd,OWpd]),Direct(Hsubps,[OVps,OWps])),
SSE(Direct(Movd,[OEd_q,OPd]),Direct(Movq,[OVq,OWq]),Direct(Movd,[OEd_q,OVdq]),Invalid), # Revisit on 64-bit *)
SSE(Direct(Movq,[OQq,OPq]),Direct(Movdqu,[OWdq,OVdq]),Direct(Movdqa,[OWdq,OVdq]),Invalid),
Direct(Jo ,[OJz]), # 0x180 *)
Direct(Jno,[OJz]),
Direct(Jb ,[OJz]),
Direct(Jae,[OJz]),
Direct(Jz ,[OJz]),
Direct(Jnz,[OJz]),
Direct(Jbe,[OJz]),
Direct(Ja ,[OJz]),
Direct(Js ,[OJz]),
Direct(Jns,[OJz]),
Direct(Jp ,[OJz]),
Direct(Jnp,[OJz]),
Direct(Jl ,[OJz]),
Direct(Jge,[OJz]),
Direct(Jle,[OJz]),
Direct(Jg ,[OJz]),
Direct(Seto ,[OEb]), # 0x190 *)
Direct(Setno,[OEb]),
Direct(Setb ,[OEb]),
Direct(Setae,[OEb]),
Direct(Setz ,[OEb]),
Direct(Setnz,[OEb]),
Direct(Setbe,[OEb]),
Direct(Seta ,[OEb]),
Direct(Sets ,[OEb]),
Direct(Setns,[OEb]),
Direct(Setp ,[OEb]),
Direct(Setnp,[OEb]),
Direct(Setl ,[OEb]),
Direct(Setge,[OEb]),
Direct(Setle,[OEb]),
Direct(Setg ,[OEb]),
Direct(Push,[OFS]), # 0x1A0 *)
Direct(Pop,[OFS]),
Direct(Cpuid,[]),
Direct(Bt,[OEv,OGv]),
Direct(Shld,[OEv,OGv,OIb]),
Direct(Shld,[OEv,OGv,OCL]),
Invalid,
Invalid,
Direct(Push,[OGS]),
Direct(Pop,[OGS]),
Direct(Rsm,[]),
Direct(Bts,[OEv,OGv]),
Direct(Shrd,[OEv,OGv,OIb]),
Direct(Shrd,[OEv,OGv,OCL]),
PredMOD(
  Group([
    Direct(Fxsave,[OSimdState]),
    Direct(Fxrstor,[OSimdState]),
    Direct(Ldmxcsr,[OMd]),
    Direct(Stmxcsr,[OMd]),
    Invalid,
    Invalid,
    Invalid,
    Direct(Clflush,[OMb])]),
  Group([
    Invalid,
    Invalid,
    Invalid,
    Invalid,
    Invalid,
    Direct(Lfence,[]),
    Direct(Mfence,[]),
    Direct(Sfence,[])])
  ),
Direct(Imul,[OGv,OEv]),
Direct(Cmpxchg,[OEb,OGb]), # 0x1B0 *)
Direct(Cmpxchg,[OEv,OGv]),
Direct(Lss,[OGv,OMp]),
Direct(Btr,[OEv,OGv]),
Direct(Lfs,[OGv,OMp]),
Direct(Lgs,[OGv,OMp]),
Direct(Movzx,[OGv,OEb]),
Direct(Movzx,[OGv,OEw]),
SSE(Invalid,Direct(Popcnt,[OGv,OEv]),Invalid,Invalid),
Invalid, # Group 10, all invalid *)
Group([Invalid,Invalid,Invalid,Invalid,Direct(Bt ,[OEv,OIb]),Direct(Bts,[OEv,OIb]),Direct(Btr,[OEv,OIb]),Direct(Btc,[OEv,OIb])]),
Direct(Btc,[OEv,OGv]),
Direct(Bsf,[OGv,OEv]),
Direct(Bsr,[OGv,OEv]),
Direct(Movsx,[OGv,OEb]),
Direct(Movsx,[OGv,OEw]),
Direct(Xadd,[OEb,OGb]),  # 0x1C0 *)
Direct(Xadd,[OEv,OGv]),
SSE(Direct(Cmpps,[OVps,OWps,OIb]),Direct(Cmpss,[OVss,OWss,OIb]),Direct(Cmppd,[OVpd,OWpd,OIb]),Direct(Cmpsd,[OVsd,OWsd,OIb])),
SSENo(Direct(Movnti,[OMd_q,OGd_q])),
SSENo66(Direct(Pinsrw,[OPq,OEw,OIb]),  Direct(Pinsrw,[OVdq,OEw,OIb])),
SSENo66(Direct(Pextrw,[OGd,ONq,OIb]),  Direct(Pextrw,[OGd,OUdq,OIb])),
SSENo66(Direct(Shufps,[OVps,OWps,OIb]),Direct(Shufpd,[OVps,OWps,OIb])),
PredMOD(
  Group([
    Invalid,
    Direct(Cmpxchg8b,[OMq]), # Revisit on 64-bit *)
    Invalid,
    Invalid,
    Invalid,
    Invalid,
    SSE(Direct(Vmptrld,[OMq]),Direct(Vmxon,[OMq]),Direct(Vmclear,[OMq]),Invalid),
    SSENo(Direct(Vmptrst,[OMq]))]),
  Invalid),
Direct(Bswap,[OeAX]),
Direct(Bswap,[OeCX]),
Direct(Bswap,[OeDX]),
Direct(Bswap,[OeBX]),
Direct(Bswap,[OeSP]),
Direct(Bswap,[OeBP]),
Direct(Bswap,[OeSI]),
Direct(Bswap,[OeDI]),
SSE(Invalid,Invalid,Direct(Addsubpd,[OVpd,OWpd]),Direct(Addsubps,[OVps,OWps])), # 0x1D0 *)
SSENo66(Direct(Psrlw, [OPq,OQq]),Direct(Psrlw,  [OVdq,OWdq])),
SSENo66(Direct(Psrld, [OPq,OQq]),Direct(Psrld,  [OVdq,OWdq])),
SSENo66(Direct(Psrlq, [OPq,OQq]),Direct(Psrlq,  [OVdq,OWdq])),
SSENo66(Direct(Paddq, [OPq,OQq]),Direct(Paddq,  [OVdq,OWdq])),
SSENo66(Direct(Pmullw,[OPq,OQq]),Direct(Pmullw, [OVdq,OWdq])),
SSE(Invalid,Direct(Movq2dq,[OVdq,ONq]),Direct(Movq,   [OVdq,OWdq]),Direct(Movdq2q,[OPq,OUq])),
SSENo66(Direct(Pmovmskb,[OGd,ONq]),Direct(Pmovmskb,[OGd,OUdq])),
SSENo66(Direct(Psubusb,[OPq,OQq]), Direct(Psubusb,[OVdq,OWdq])),
SSENo66(Direct(Psubusw,[OPq,OQq]), Direct(Psubusw,[OVdq,OWdq])),
SSENo66(Direct(Pminub, [OPq,OQq]), Direct(Pminub, [OVdq,OWdq])),
SSENo66(Direct(Pand,   [OPq,OQq]), Direct(Pand,   [OVdq,OWdq])),
SSENo66(Direct(Paddusb,[OPq,OQq]), Direct(Paddusb,[OVdq,OWdq])),
SSENo66(Direct(Paddusw,[OPq,OQq]), Direct(Paddusw,[OVdq,OWdq])),
SSENo66(Direct(Pmaxub, [OPq,OQq]), Direct(Pmaxub, [OVdq,OWdq])),
SSENo66(Direct(Pandn,  [OPq,OQq]), Direct(Pandn,  [OVdq,OWdq])),
SSENo66(Direct(Pavgb,  [OPq,OQq]), Direct(Pavgb,  [OVdq,OWdq])), # 0x1E0 *)
SSENo66(Direct(Psraw,  [OPq,OQq]), Direct(Psraw,  [OVdq,OWdq])),
SSENo66(Direct(Psrad,  [OPq,OQq]), Direct(Psrad,  [OVdq,OWdq])),
SSENo66(Direct(Pavgw,  [OPq,OQq]), Direct(Pavgw,  [OVdq,OWdq])),
SSENo66(Direct(Pmulhuw,[OPq,OQq]), Direct(Pmulhuw,[OVdq,OWdq])),
SSENo66(Direct(Pmulhw, [OPq,OQq]), Direct(Pmulhw, [OVdq,OWdq])),
SSE(Invalid,Direct(Cvtdq2pd,[OVpd,OWdq]),Direct(Cvttpd2dq,[OVdq,OWpd]),Direct(Cvtpd2dq,[OVdq,OWpd])),
SSENo66(Direct(Movntq,[OMq,OPq]),  Direct(Movntdq,[OMdq,OVdq])),
SSENo66(Direct(Psubsb, [OPq,OQq]), Direct(Psubsb, [OVdq,OWdq])),
SSENo66(Direct(Psubsw, [OPq,OQq]), Direct(Psubsw, [OVdq,OWdq])),
SSENo66(Direct(Pminsw, [OPq,OQq]), Direct(Pminsw, [OVdq,OWdq])),
SSENo66(Direct(Por,    [OPq,OQq]), Direct(Por,    [OVdq,OWdq])),
SSENo66(Direct(Paddsb, [OPq,OQq]), Direct(Paddsb, [OVdq,OWdq])),
SSENo66(Direct(Paddsw, [OPq,OQq]), Direct(Paddsw, [OVdq,OWdq])),
SSENo66(Direct(Pmaxsw, [OPq,OQq]), Direct(Pmaxsw, [OVdq,OWdq])),
SSENo66(Direct(Pxor,   [OPq,OQq]), Direct(Pxor,   [OVdq,OWdq])),
SSE(Invalid,Invalid,Invalid,Direct(Lddqu,[OVdq,OMdq])), # 0x1F0 *)
SSENo66(Direct(Psllw,   [OPq,OQq]),Direct(Psllw,     [OVdq,OWdq])),
SSENo66(Direct(Pslld,   [OPq,OQq]),Direct(Pslld,     [OVdq,OWdq])),
SSENo66(Direct(Psllq,   [OPq,OQq]),Direct(Psllq,     [OVdq,OWdq])),
SSENo66(Direct(Pmuludq, [OPq,OQq]),Direct(Pmuludq,   [OVdq,OWdq])),
SSENo66(Direct(Pmaddwd, [OPq,OQq]),Direct(Pmaddwd,   [OVdq,OWdq])),
SSENo66(Direct(Psadbw,  [OPq,OQq]),Direct(Psadbw,    [OVdq,OWdq])),
SSENo66(Direct(Maskmovq,[OPq,ONq]),Direct(Maskmovdqu,[OVdq,OUdq])),
SSENo66(Direct(Psubb,   [OPq,OQq]),Direct(Psubb,     [OVdq,OWdq])),
SSENo66(Direct(Psubw,   [OPq,OQq]),Direct(Psubw,     [OVdq,OWdq])),
SSENo66(Direct(Psubd,   [OPq,OQq]),Direct(Psubd,     [OVdq,OWdq])),
SSENo66(Direct(Psubq,   [OPq,OQq]),Direct(Psubq,     [OVdq,OWdq])),
SSENo66(Direct(Paddb,   [OPq,OQq]),Direct(Paddb,     [OVdq,OWdq])),
SSENo66(Direct(Paddw,   [OPq,OQq]),Direct(Paddw,     [OVdq,OWdq])),
SSENo66(Direct(Paddd,   [OPq,OQq]),Direct(Paddd,     [OVdq,OWdq])),
Invalid,
SSENo66(Direct(Pshufb,   [OPq,OQq]),Direct(Pshufb,   [OVdq,OWdq])), # 0x200 *)
SSENo66(Direct(Phaddw,   [OPq,OQq]),Direct(Phaddw,   [OVdq,OWdq])),
SSENo66(Direct(Phaddd,   [OPq,OQq]),Direct(Phaddd,   [OVdq,OWdq])),
SSENo66(Direct(Phaddsw,  [OPq,OQq]),Direct(Phaddsw,  [OVdq,OWdq])),
SSENo66(Direct(Pmaddubsw,[OPq,OQq]),Direct(Pmaddubsw,[OVdq,OWdq])),
SSENo66(Direct(Phsubw,   [OPq,OQq]),Direct(Phsubw,   [OVdq,OWdq])),
SSENo66(Direct(Phsubd,   [OPq,OQq]),Direct(Phsubd,   [OVdq,OWdq])),
SSENo66(Direct(Phsubsw,  [OPq,OQq]),Direct(Phsubsw,  [OVdq,OWdq])),
SSENo66(Direct(Psignb,   [OPq,OQq]),Direct(Psignb,   [OVdq,OWdq])),
SSENo66(Direct(Psignw,   [OPq,OQq]),Direct(Psignw,   [OVdq,OWdq])),
SSENo66(Direct(Psignd,   [OPq,OQq]),Direct(Psignd,   [OVdq,OWdq])),
SSENo66(Direct(Pmulhrsw, [OPq,OQq]),Direct(Pmulhrsw, [OVdq,OWdq])),
Invalid,
Invalid,
Invalid,
Invalid,
SSE66(Direct(Pblendvb,[OVdq,OWdq])), # 0x210 *)
Invalid,
Invalid,
Invalid,
SSE66(Direct(Blendvps,[OVdq,OWdq])),
SSE66(Direct(Blendvpd,[OVdq,OWdq])),
Invalid,
SSE66(Direct(Ptest,[OVdq,OWdq])),
Invalid,
Invalid,
Invalid,
Invalid,
SSENo66(Direct(Pabsb,[OPq,OQq]),Direct(Pabsb,[OVdq,OWdq])),
SSENo66(Direct(Pabsw,[OPq,OQq]),Direct(Pabsw,[OVdq,OWdq])),
SSENo66(Direct(Pabsd,[OPq,OQq]),Direct(Pabsd,[OVdq,OWdq])),
Invalid,
SSE66(Direct(Pmovsxbw,[OVdq,OUdq_Mq])), # 0x220 *)
SSE66(Direct(Pmovsxbd,[OVdq,OUdq_Md])),
SSE66(Direct(Pmovsxbq,[OVdq,OUdq_Mw])),
SSE66(Direct(Pmovsxwd,[OVdq,OUdq_Mq])),
SSE66(Direct(Pmovsxwq,[OVdq,OUdq_Md])),
SSE66(Direct(Pmovsxdq,[OVdq,OUdq_Mq])),
Invalid,
Invalid,
SSE66(Direct(Pmuldq,  [OVdq,OWdq])),
SSE66(Direct(Pcmpeqq, [OVdq,OWdq])),
SSE66(Direct(Movntdqa,[OVdq,OMdq])),
SSE66(Direct(Packusdw,[OVdq,OWdq])),
Invalid,
Invalid,
Invalid,
Invalid,
SSE66(Direct(Pmovzxbw,[OVdq,OUdq_Mq])), # 0x230 *)
SSE66(Direct(Pmovzxbd,[OVdq,OUdq_Md])),
SSE66(Direct(Pmovzxbq,[OVdq,OUdq_Mw])),
SSE66(Direct(Pmovzxwd,[OVdq,OUdq_Mq])),
SSE66(Direct(Pmovzxwq,[OVdq,OUdq_Md])),
SSE66(Direct(Pmovzxdq,[OVdq,OUdq_Mq])),
Invalid,
SSE66(Direct(Pcmpgtq,   [OVdq,OWdq])),
SSE66(Direct(Pminsb,    [OVdq,OWdq])),
SSE66(Direct(Pminsd,    [OVdq,OWdq])),
SSE66(Direct(Pminuw,    [OVdq,OWdq])),
SSE66(Direct(Pminud,    [OVdq,OWdq])),
SSE66(Direct(Pmaxsb,    [OVdq,OWdq])),
SSE66(Direct(Pmaxsd,    [OVdq,OWdq])),
SSE66(Direct(Pmaxuw,    [OVdq,OWdq])),
SSE66(Direct(Pmaxud,    [OVdq,OWdq])),
SSE66(Direct(Pmulld,    [OVdq,OWdq])), # 0x240 *)
SSE66(Direct(Phminposuw,[OVdq,OWdq])),
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x250 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x260 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x270 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x280 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x290 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x2A0 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x2B0 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x2C0 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x2D0 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x2E0 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Direct(Crc32,[OGd,OEb]), # 0x2F0 *)
Direct(Crc32,[OGd,OEv]),
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x300 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
SSE66(Direct(Roundps,[OVdq,OWdq,OIb])),
SSE66(Direct(Roundpd,[OVdq,OWdq,OIb])),
SSE66(Direct(Roundss,[OVss,OWss,OIb])),
SSE66(Direct(Roundsd,[OVsd,OWsd,OIb])),
SSE66(Direct(Blendps,[OVdq,OWdq,OIb])),
SSE66(Direct(Blendpd,[OVdq,OWdq,OIb])),
SSE66(Direct(Pblendw,[OVdq,OWdq,OIb])),
SSENo66(Direct(Palignr,[OPq,OQq,OIb]),Direct(Palignr,[OVdq,OWdq,OIb])),
Invalid, # 0x310 *)
Invalid,
Invalid,
Invalid,
SSE66(Direct(Pextrb,   [ORd_Mb,OVdq,OIb])),
SSE66(Direct(Pextrw,   [ORd_Mw,OVdq,OIb])),
SSE66(Direct(Pextrd,   [OEd,OVdq,OIb])), # Revisit for 64-bit *)
SSE66(Direct(Extractps,[OEd,OVdq,OIb])),
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
SSE66(Direct(Pinsrb,  [OVdq,OEd,OIb])), # 0x320 *)
SSE66(Direct(Insertps,[OVdq,OUdq_Md,OIb])),
SSE66(Direct(Pinsrd,  [OVdq,OEd,OIb])), # Revisit for 64-bit *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x330 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
SSE66(Direct(Dpps,   [OVdq,OWdq,OIb])), # 0x340 *)
SSE66(Direct(Dppd,   [OVdq,OWdq,OIb])),
SSE66(Direct(Mpsadbw,[OVdq,OWdq,OIb])),
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x350 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
SSE66(Direct(Pcmpestrm,[OVdq,OWdq,OIb])), # 0x360 *)
SSE66(Direct(Pcmpestri,[OVdq,OWdq,OIb])),
SSE66(Direct(Pcmpistrm,[OVdq,OWdq,OIb])),
SSE66(Direct(Pcmpistri,[OVdq,OWdq,OIb])),
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x370 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x380 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x390 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x3A0 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x3B0 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x3C0 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x3D0 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x3E0 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid, # 0x3F0 *)
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid,
Invalid
]
