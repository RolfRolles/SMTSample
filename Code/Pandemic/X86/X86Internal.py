from X86MetaData import *
from Pandemic.Util.Guarded import *
from Pandemic.Util.HashFunctions import unary_hash, binary_hash

def X86Hexify(value):
	"""Function to make an X86-style hexadecimal string.  I.e., it should end in
	``h``, should not begin with ``0x``, and should begin with a ``0`` if the 
	first nibble is ``A-F``.
	
	:param integer value:
	:rtype: string
	"""
	hstr = hex(value)
	
	hstr = hstr[0:-1] if hstr[-1] == 'l' or hstr[-1] == 'L' else hstr
	hstr = "0"+hstr[2:] if hstr[2] >= 'a' and hstr[2] <= 'f' else hstr[2:]
	return "%sh" % str.upper(hstr)

class Operand(object):
	"""Base class for X86 operands, containing some of the Python glue."""
	def __eq__(self,other):
		return type(self) == type(other) and self.value == other.value
	
	def __ne__(self,other):
		return not(self.__eq__(other))

	def __hash__(self):
		return unary_hash(hash(self.value),self._hashcode)

# Registers are held in GuardedEnumeration elements.  This allows us to ensure
# that they are valid at all times, as well as simplfying the process of 
# printing and setting them, as well as creating them from 0-indexed values.
# The Register class also supports retrieving the register as a 0-indexed 
# value (its IntValue() method).
class Register(Operand):
	"""The base class for all registers in X86 assembly language.  The 
	constructor takes two parameters: *value* and *adjust_value*.  If
	*adjust_value* is ``False``, *value* is interpreted as an enumeration 
	element, i.e. some object that is a derivative of :class:`~.EnumElt`,
	which must have the same type as the *regtype* member.  If *adjust_value* is
	``True``, then *value* is interpreted as an integer, and it is used to
	construct an :class:`~.EnumElt` of type *regtype*.
	
	:ivar `~.EnumElt` value: an enumeration element corresponding to the 
		particular register being represented
	:ivar `~.EnumElt` regtype: a derivative of :class:`~.EnumElt` corresponding
		to the type of register a derived class represents
	"""
	def init(self,value,hashcode,regtype,adjust_value=False):
		self.value = regtype(value) if adjust_value else value
		if not adjust_value:
			if not isinstance(value,regtype):
				print "Register:  value %s requires type %s" % (value,regtype)
				raise TypeError
		self._hashcode = hashcode
	
	
	def IntValue(self):
		"""Retrieve the integer value ``0-7`` from the held *value*.
		
		:rtype: integer
		"""
		return self.value.IntValue()
	
	def __call__(self,value):
		"""Create a new :class:`.Register` object, of the same type as *self*,
		using the integer value *value*.
		
		:ivar integer value: the register number for the new :class:`.Register` 
			object
		:rtype: Register
		:returns: The new :class:`Register` object corresponding to integer 
			*value*.
		"""
		return type(self)(value,True)

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__,self.value)
	
	def __str__(self):
		return "%s" % self.value
	
class GeneralReg(Register):
	"""GeneralReg gets its own class in the hierarchy, so we can distinguish them
	from other types of registers."""
	pass

class Immediate(Operand):
	"""Immediates are held in guarded integers, so that they never exceed their
	bounds (i.e., 8-bit values are always 0 <= value <= 0xFF)."""
	def init(self,hashcode,value,mask):
		self._hashcode = hashcode
		self.held = GuardedInteger(value,mask)	

	# This property allows us to access the GuardedInteger's value transparently.
	@property
	def value(self):
		"""The integer value of an immediate constant."""
		return self.held.value
	@value.setter
	def value(self,val):
		self.held.value = val

	def __call__(self,value):
		"""Create a new :class:`.Immediate` object, of the same type as *self*,
		using the integer value *value*.
		
		:ivar integer value: the value for the new :class:`.Immediate` object
		:rtype: Immediate
		:returns: The new :class:`Immediate` object with integer value *value*.
		"""
		return type(self)(value)

	def __repr__(self):
		return "%s(%#x)" % (self.__class__.__name__,self.held.value)
	def __str__(self):
		return X86Hexify(self.held.value)
	
class MemExpr(Operand):
	"""Base class for memory operands.
	
	:ivar `.SegElt` Seg: the segment in which the access takes place
	"""
	def __init__(self,seg,size):
		self.Seg = seg
		self.size = size
	
	def init(self,hashcode,seg,size,regtype,basereg,indexreg,disp,mask,adjust_values):
		self._hashcode = hashcode
		self.Seg = seg
		self.size = size
		self.BaseReg  = regtype( basereg) if adjust_values else  basereg
		self.IndexReg = regtype(indexreg) if adjust_values else indexreg
		if not adjust_values:
			if basereg is not None and not isinstance(basereg,regtype):
				print "MemExpr:  basereg %s requires type %s"  % (basereg,regtype)
				raise TypeError
			if indexreg is not None and not isinstance(indexreg,regtype):
				print "MemExpr:  indexreg %s requires type %s" % (indexreg,regtype)
				raise TypeError
		self._disp = GuardedInteger(None if disp == None or disp == 0 else disp,mask)
	
	@property
	def Disp(self): 
		"""Integer displacement; may be ``None``.  16-bit for :class:`Mem16`, 
		32-bit for :class:`Mem32`."""
		return self._disp.value
	@Disp.setter
	def Disp(self,value): 
		self._disp.value = value

	def __str__(self):
		segstr = "" if self.Seg == self.DefaultSeg() else "%s:" % self.Seg
		return "%s ptr %s[%s]" % (self.size,segstr,self.String())

	def MakeString(self,parts):
		"""Returns a string based on those in *parts*, with ``+`` between the 
		non-empty strings contained therein.
		
		:param parts: string parts (some may be ``""``)
		:type parts: string list
		:rtype: string
		"""
		return "+".join(filter(lambda o: o != "",parts))
	
	def HashIndex(self):
		"""Used internally for hashing the index component.  Differs in 
		:class:`.Mem16` and :class:`.Mem32` objects."""
		return hash(self.IndexReg)
	
	def __hash__(self):
		h1 = binary_hash(hash(self.BaseReg),self.HashIndex(),self._hashcode+1)
		h2 = binary_hash(hash(self.size),h1,self._hashcode+3)
		return binary_hash(h2,hash(self.Disp),self._hashcode)
	
class FarTarget(Operand):
	"""Base class for memory operands specified as segment:offset pairs."""
	def init(self,hashcode,seg,off,mask):
		self._hashcode = hashcode
		self._seg = GuardedInteger(seg,0xFFFF)
		self._off = GuardedInteger(off,mask)
	
	# Properties that allow us to access the integer values from the 
	# GuardedInteger representations that we store internally.
	@property
	def Seg(self):
		"""16-bit integer value for the segment."""
		return self._seg.value
	@Seg.setter
	def Seg(self,value):
		self._seg.value = value
	
	@property
	def Off(self):
		"""Integer value for the offset.  16-bits in :class:`.AP16`, 32-bits in 
		:class:`.AP32`."""
		return self._off.value
	@Off.setter
	def Off(self,value):
		self._off.value = value

	# Boilerplate
	def __repr__(self):
		return "%s(%r,%r)" % (self.__class__.__name__,self._seg,self._off)

	def __str__(self):
		return "%s:%s" % (X86Hexify(self._seg.value),X86Hexify(self._off.value))

	def __eq__(self,other):
		return type(self)==type(other) and self.Seg == other.Seg and self.Off == other.Off
	
	def __hash__(self):
		return binary_hash(hash(self._seg),hash(self._off),self._hashcode)

