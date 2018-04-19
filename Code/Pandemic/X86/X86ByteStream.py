"""Byte stream interface.  To support any form of input, derive a class from 
:class:`StreamObj` and override :meth:`GetByteInternal`.
"""

from X86 import InvalidInstruction

class StreamObj(object):
	"""Class for acquiring bytes from a source."""	
	def __init__(self,bytes):
		self.bytes = bytes
		self.Init()
	
	def Init(self):
		"""Initializes position variables."""
		self.pos = 0
		self.origpos = 0

	def GetByteInternal(self):
		"""Consume a byte from the stream and return it.  This function shall be
		the only one needed to override in derived classes, when changing the 
		source from which a byte is consumed.
		
		:rtype: 8-bit integer
		"""
		return self.bytes[self.pos]
	
	def Byte(self):
		"""Check to ensure that we have not consumed more than 16 bytes (for that
		would signal an illegal instruction).  If not, invoke 
		:meth:`GetByteInternal` and return the result.
		
		:rtype: 8-bit integer
		:raises: :exc:`.InvalidInstruction` if more than 16 bytes have been 
			consumed since the last call to :meth:`SetPos`.
		"""
		# X86/32 instructions are at most 15 bytes in length
		if self.pos-self.origpos >= 16:
			raise InvalidInstruction()
		
		b = self.GetByteInternal()
		self.pos = self.pos + 1
		return b

	def Word(self):
		"""Consume a word from the stream and return it.
		
		:rtype: 16-bit integer
		:raises: :exc:`.InvalidInstruction` if more than 16 bytes have been 
			consumed since the last call to :meth:`SetPos`.
		"""
		b0 = self.Byte()
		b1 = self.Byte()
		return (b1 << 8) | b0

	def Dword(self):
		"""Consume a dword from the stream and return it.
		
		:rtype: 32-bit integer
		:raises: :exc:`.InvalidInstruction` if more than 16 bytes have been 
			consumed since the last call to :meth:`SetPos`.
		"""
		w0 = self.Word()
		w1 = self.Word()
		return (w1 << 16) | w0
	
	def Pos(self):
		"""Return the current position of the stream.
		
		:rtype: integer
		"""
		return self.pos
	
	def SetPos(self,ea):
		"""Set the current position of the stream to *ea*.
		
		:param integer ea:
		"""
		self.pos,self.origpos = ea,ea
		
