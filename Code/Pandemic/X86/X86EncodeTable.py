"""X86 instructions have "encodings" associated with them.  Encodings are 
represented as classes that derive from :class:`X86Enc`.  Encodings describe 
the types of the operands, as well as whether they require any special 
treatment while converting the instructions into bytes:

* :class:`Ordinary` requires no special treatment.
* :class:`Native16` encodings require size prefixes.
* :class:`ModRMGroup` encodings set the Ordinary's :attr:`.GGG` member.
"""

from X86InternalOperand import *
from X86MetaData import *
from Pandemic.Util.ExerciseError import ExerciseError

class X86Enc(object):
	"""The base class for all X86 instruction encodings.
	
	:ivar bytes: instruction stem bytes
	:type bytes: integer list
	:ivar ops: list of abstract operand types
	:type ops: :class:`.AOTElt` list
	"""
	def __init__(self,bytes,ops):
		self.bytes = bytes
		self.ops   = ops

	# encoder is an X86Encoder object
	def Encode(self,encoder):
		"""This method is responsible for modifying the *encoder* object if the
		encoding method requires that.
		
		:param `.X86Encoder.X86Encoder` encoder: Encoder object
		"""
		pass

class Ordinary(X86Enc):
	"""The encoding method class for most X86 instruction encodings."""
	def Encode(self,encoder):
		"""Ordinary instruction encodings don't modify *encoder*.

		:param `.X86Encoder.X86Encoder` encoder: Encoder object
		"""
		raise ExerciseError("X86EncodeTable::Ordinary")

class Native16(X86Enc):
	"""The encoding method class for X86 instructions that require an opsize
	prefix in order to be encoded."""
	def Encode(self,encoder): 
		"""Native16 instruction encodings must set the *sizepfx* member of 
		*encoder*.

		:param `.X86Encoder.X86Encoder` encoder: Encoder object
		"""
		raise ExerciseError("X86EncodeTable::Native16")

class ModRMGroup(X86Enc): 
	"""The encoding method class for X86 instructions that are part of a ModRM
	group, and thus require that the encoder's ModRM member :attr:`.GGG` be set
	to a specific value.
	
	:ivar integer ggg: The group entry number (:attr:`.GGG` value).
	"""
	def __init__(self,ggg,bytes,ops):
		self.bytes = bytes
		self.ops   = ops
		self.ggg   = ggg

	def Encode(self,encoder):  
		"""Native16 instruction encodings must set the :attr:`.GGG` member of 
		*encoder*.

		:param `.X86Encoder.X86Encoder` encoder: Encoder object
		"""
		raise ExerciseError("X86EncodeTable::ModRMGroup")

# Since many of the same operand types are used repeatedly in instruction 
# encodings, we create lists for them to simplify the table below.
eGvEvIz    = [OGv,OEv,OIz]
eEvGvIb    = [OEv,OGv,OIb]
eEvGv      = [OEv,OGv]
eGvEv      = [OGv,OEv]
erAXIz     = [OrAX,OIz]
eEvIz      = [OEv,OIz]
eGvEvIb    = [OGv,OEv,OIb]
eEvGvCL    = [OEv,OGv,OCL]
eeAXEv     = [OeAX,OEv]
erAXOv     = [OrAX,OOv]
eOvrAX     = [OOv,OrAX]
erAXr8Iv   = [OrAXr8,OIv]
erCXr9Iv   = [OrCXr9,OIv]
erDXr10Iv  = [OrDXr10,OIv]
erBXr11Iv  = [OrBXr11,OIv]
erSPr12Iv  = [OrSPr12,OIv]
erBPr13Iv  = [OrBPr13,OIv]
erSIr14Iv  = [OrSIr14,OIv]
erDIr15Iv  = [OrDIr15,OIv]
erAXrCXr9  = [OrAX,OrCXr9]
erAXrDXr10 = [OrAX,OrDXr10]
erAXrBXr11 = [OrAX,OrBXr11]
erAXrSPr12 = [OrAX,OrSPr12]
erAXrBPr13 = [OrAX,OrBPr13]
erAXrSIr14 = [OrAX,OrSIr14]
erAXrDIr15 = [OrAX,OrDIr15]
eGvM       = [OGv,OM]
eGvMa      = [OGv,OMa]
eGvMp      = [OGv,OMp]
eGzMp      = [OGz,OMp]
eXwYw      = [OXw,OYw]
eXdYd      = [OXd,OYd]
eGdEv      = [OGd,OEv]
eEbGb      = [OEb,OGb]
eEdGd      = [OEd,OGd]
eGvEb      = [OGv,OEb]
eGdEb      = [OGd,OEb]
eGbEb      = [OGb,OEb]
eGvEw      = [OGv,OEw]
eALIb      = [OAL,OIb]
eEbIb      = [OEb,OIb]
eEvIb      = [OEv,OIb]
eEvIbv     = [OEv,OIbv]
eStNSt0    = [OStN,OSt0]
eSt0StN    = [OSt0,OStN]
eEwGw      = [OEw,OGw]
eEb1       = [OEb,O1 ]
eEv1       = [OEv,O1 ]
eEbCL      = [OEb,OCL]
eEvCL      = [OEv,OCL]
eSt0Real4  = [OSt0,OReal4]
eYbDX      = [OYb,ODX]
eYwDX      = [OYw,ODX]
eYdDX      = [OYd,ODX]
eDXXb      = [ODX,OXb]
eDXXw      = [ODX,OXw]
eDXXd      = [ODX,OXd]
eALEb      = [OAL,OEb]
eEvSw      = [OEv,OSw]
eSwEw      = [OSw,OEw]
eALOb      = [OAL,OOb]
eObAL      = [OOb,OAL]
eALR8LIb   = [OALR8L,OIb]
eCLR9LIb   = [OCLR9L,OIb]
eDLR10LIb  = [ODLR10L,OIb]
eBLR11LIb  = [OBLR11L,OIb]
eAHR12LIb  = [OAHR12L,OIb]
eCHR13LIb  = [OCHR13L,OIb]
eDHR14LIb  = [ODHR14L,OIb]
eBHR15LIb  = [OBHR15L,OIb]
eSt0Real8  = [OSt0,OReal8]
eXbYb      = [OXb,OYb]
eIwIb      = [OIw,OIb] 
eeAXIb     = [OeAX,OIb]
eALDX      = [OAL,ODX] 
eeAXDX     = [OeAX,ODX]
eIbAL      = [OIb,OAL] 
eIbeAX     = [OIb,OeAX]
eDXAL      = [ODX,OAL] 
eDXeAX     = [ODX,OeAX]
eRdCd      = [ORd,OCd]
eRdDd      = [ORd,ODd]
eCdRd      = [OCd,ORd]
eDdRd      = [ODd,ORd]
eSimdState = [OSimdState]
eVpsWps      = [OVps,OWps]
eWpsVps      = [OWps,OVps]
eVssWss      = [OVss,OWss]
eWssVss      = [OWss,OVss]
eVpdWpd      = [OVpd,OWpd]
eWpdVpd      = [OWpd,OVpd]
eVsdWsd      = [OVsd,OWsd]
eWsdVsd      = [OWsd,OVsd]
eVqMq        = [OVq,OMq]
eMqVq        = [OMq,OVq]
eVqUq        = [OVq,OUq]
eVqWq        = [OVq,OWq]
eVpdWq       = [OVpd,OWq]
eVpsWq       = [OVps,OWq]
eVpsQpi      = [OVps,OQpi]
eVssEd_q     = [OVss,OEd_q]
eVpdQpi      = [OVpd,OQpi]
eVsdEd_q     = [OVsd,OEd_q]
eMpsVps      = [OMps,OVps]
eMpdVpd      = [OMpd,OVps]
ePpiWps      = [OPpi,OWps]
eGdWss       = [OGd,OWss]
ePpiWpd      = [OPpi,OWpd]
eGdWsd       = [OGd,OWsd]
eGd_qWsd     = [OGd_q,OWsd]
eGd_qWss     = [OGd_q,OWss]
eGdUps       = [OGd,OUps]
eGdUpd       = [OGd,OUpd]
eVpdWps      = [OVpd,OWps]
eVpsWpd      = [OVps,OWpd]
eVdqWps      = [OVdq,OWps]
ePqQd        = [OPq,OQd]
eVdqWdq      = [OVdq,OWdq]
ePdEd_q      = [OPd,OEd_q]
eVdqEd_q     = [OVdq,OEd_q]
eEd_qPd      = [OEd_q,OPd]
eEd_qVdq     = [OEd_q,OVdq]
ePqQq        = [OPq,OQq]
eQqPq        = [OQq,OPq]
eWdqVdq      = [OWdq,OVdq]
ePqQqIb      = [OPq,OQq,OIb]
eVdqWdqIb    = [OVdq,OWdq,OIb]
eNqIb        = [ONq,OIb]
eUdqIb       = [OUdq,OIb]
eVpsWpsIb    = [OVps,OWps,OIb]
eVssWssIb    = [OVss,OWss,OIb]
eVpdWpdIb    = [OVpd,OWpd,OIb]
eVsdWsdIb    = [OVsd,OWsd,OIb]
eMd_qGd_q    = [OMd_q,OGd_q]
ePqEwIb      = [OPq,OEw,OIb]
eVdqEwIb     = [OVdq,OEw,OIb]
eGdNqIb      = [OGd,ONq,OIb]
eGdUdqIb     = [OGd,OUdq,OIb]
eVdqNq       = [OVdq,ONq]
ePqUq        = [OPq,OUq]
eGdNq        = [OGd,ONq]
eGdUdq       = [OGd,OUdq]
eVpdWdq      = [OVpd,OWdq]
eVdqWpd      = [OVdq,OWpd]
eMqPq        = [OMq,OPq]
eMdqVdq      = [OMdq,OVdq]
eVdqMdq      = [OVdq,OMdq]
ePqNq        = [OPq,ONq]
eVdqUdq      = [OVdq,OUdq]
eVdqUdq_Mw   = [OVdq,OUdq_Mw]
eVdqUdq_Md   = [OVdq,OUdq_Md]
eVdqUdq_Mq   = [OVdq,OUdq_Mq]
eRd_MbVdqIb  = [ORd_Mb,OVdq,OIb]
eRd_MwVdqIb  = [ORd_Mw,OVdq,OIb]
eEdVdqIb     = [OEd,OVdq,OIb]
eVdqEdIb     = [OVdq,OEd,OIb]
eVdqUdq_MdIb = [OVdq,OUdq_Md,OIb]
eMbEbx       = [OMbEbx]
eeAX      = [OeAX]
eeCX      = [OeCX]
eeDX      = [OeDX]
eeBX      = [OeBX]
eeSP      = [OeSP]
eeBP      = [OeBP]
eeSI      = [OeSI]
eeDI      = [OeDI]
eEb       = [OEb]
eEw       = [OEw]
eEd       = [OEd]
eEv       = [OEv]
eRv       = [ORv]
erAXr8    = [OrAXr8] 
erCXr9    = [OrCXr9] 
erDXr10   = [OrDXr10]
erBXr11   = [OrBXr11]
erSPr12   = [OrSPr12]
erBPr13   = [OrBPr13]
erSIr14   = [OrSIr14]
erDIr15   = [OrDIr15]
eES       = [OES]
eCS       = [OCS]
eSS       = [OSS]
eDS       = [ODS]
eFS       = [OFS]
eGS       = [OGS]
eIz       = [OIz]
eReal4    = [OReal4]
eReal8    = [OReal8]
eReal10   = [OReal10]
eYb       = [OYb]
eXb       = [OXb]
eYv       = [OYv]
eYz       = [OYz]
eXv       = [OXv]
eXz       = [OXz]
eStN      = [OStN]
eFPEnv    = [OFPEnv]
eFPEnvLow = [OFPEnvLow]
eIw       = [OIw]
eIb       = [OIb]
eMb       = [OMb]
eMw       = [OMw]
eMd       = [OMd]
eMs       = [OMs]
eMq       = [OMq]
eAX       = [OAX]
eYw       = [OYw]
eXw       = [OXw]
eYd       = [OYd]
eXd       = [OXd]
eRw       = [ORw]
eAp       = [OAp]
eNone     = []

mnem_to_encodings = [None]*(X86_LAST_MNEMONIC+1)

def v(m): return m.IntValue()

mnem_to_encodings[v(Daa)]    = [Ordinary([0x27],eNone)]
mnem_to_encodings[v(Das)]    = [Ordinary([0x2F],eNone)]
mnem_to_encodings[v(Aaa)]    = [Ordinary([0x37],eNone)]
mnem_to_encodings[v(Aas)]    = [Ordinary([0x3F],eNone)]
mnem_to_encodings[v(Add)]    = [
  Ordinary([0x00],eEbGb),
  Ordinary([0x01],eEvGv),
  Ordinary([0x02],eGbEb), 
  Ordinary([0x03],eGvEv), 
  Ordinary([0x04],eALIb), 
  Ordinary([0x05],erAXIz), 
  ModRMGroup(0,[0x80],eEbIb), 
  ModRMGroup(0,[0x81],eEvIz), 
  ModRMGroup(0,[0x83],eEvIbv), 
  ]
mnem_to_encodings[v(Or)]     = [
  Ordinary([0x08],eEbGb),
  Ordinary([0x09],eEvGv),
  Ordinary([0x0A],eGbEb), 
  Ordinary([0x0B],eGvEv), 
  Ordinary([0x0C],eALIb), 
  Ordinary([0x0D],erAXIz), 
  ModRMGroup(1,[0x80],eEbIb), 
  ModRMGroup(1,[0x81],eEvIz), 
  ModRMGroup(1,[0x83],eEvIbv), 
  ]
mnem_to_encodings[v(Adc)]    = [
  Ordinary([0x10],eEbGb),
  Ordinary([0x11],eEvGv),
  Ordinary([0x12],eGbEb), 
  Ordinary([0x13],eGvEv), 
  Ordinary([0x14],eALIb), 
  Ordinary([0x15],erAXIz), 
  ModRMGroup(2,[0x80],eEbIb), 
  ModRMGroup(2,[0x81],eEvIz), 
  ModRMGroup(2,[0x83],eEvIbv), 
  ]
mnem_to_encodings[v(Sbb)]    = [
  Ordinary([0x18],eEbGb),
  Ordinary([0x19],eEvGv),
  Ordinary([0x1A],eGbEb), 
  Ordinary([0x1B],eGvEv), 
  Ordinary([0x1C],eALIb), 
  Ordinary([0x1D],erAXIz), 
  ModRMGroup(3,[0x80],eEbIb), 
  ModRMGroup(3,[0x81],eEvIz), 
  ModRMGroup(3,[0x83],eEvIbv), 
  ]
mnem_to_encodings[v(And)]    = [
  Ordinary([0x20],eEbGb),
  Ordinary([0x21],eEvGv),
  Ordinary([0x22],eGbEb), 
  Ordinary([0x23],eGvEv), 
  Ordinary([0x24],eALIb), 
  Ordinary([0x25],erAXIz), 
  ModRMGroup(4,[0x80],eEbIb), 
  ModRMGroup(4,[0x81],eEvIz), 
  ModRMGroup(4,[0x83],eEvIbv), 
  ]
mnem_to_encodings[v(Sub)]    = [
  Ordinary([0x28],eEbGb),
  Ordinary([0x29],eEvGv),
  Ordinary([0x2A],eGbEb), 
  Ordinary([0x2B],eGvEv), 
  Ordinary([0x2C],eALIb), 
  Ordinary([0x2D],erAXIz), 
  ModRMGroup(5,[0x80],eEbIb), 
  ModRMGroup(5,[0x81],eEvIz), 
  ModRMGroup(5,[0x83],eEvIbv), 
  ]
mnem_to_encodings[v(Xor)]    = [
  Ordinary([0x30],eEbGb),
  Ordinary([0x31],eEvGv),
  Ordinary([0x32],eGbEb), 
  Ordinary([0x33],eGvEv), 
  Ordinary([0x34],eALIb), 
  Ordinary([0x35],erAXIz), 
  ModRMGroup(6,[0x80],eEbIb), 
  ModRMGroup(6,[0x81],eEvIz), 
  ModRMGroup(6,[0x83],eEvIbv), 
  ]
mnem_to_encodings[v(Cmp)]    = [
  Ordinary([0x38],eEbGb),
  Ordinary([0x39],eEvGv),
  Ordinary([0x3A],eGbEb), 
  Ordinary([0x3B],eGvEv), 
  Ordinary([0x3C],eALIb), 
  Ordinary([0x3D],erAXIz), 
  ModRMGroup(7,[0x80],eEbIb), 
  ModRMGroup(7,[0x81],eEvIz), 
  ModRMGroup(7,[0x83],eEvIbv), 
  ]
mnem_to_encodings[v(Inc)]    = [
  Ordinary([0x40],eeAX),
  Ordinary([0x41],eeCX),
  Ordinary([0x42],eeDX),
  Ordinary([0x43],eeBX),
  Ordinary([0x44],eeSP),
  Ordinary([0x45],eeBP),
  Ordinary([0x46],eeSI),
  Ordinary([0x47],eeDI),
  ModRMGroup(0,[0xFE],eEb),
  ModRMGroup(0,[0xFF],eEv),
  ]
mnem_to_encodings[v(Dec)]    = [
  Ordinary([0x48],eeAX),
  Ordinary([0x49],eeCX),
  Ordinary([0x4A],eeDX),
  Ordinary([0x4B],eeBX),
  Ordinary([0x4C],eeSP),
  Ordinary([0x4D],eeBP),
  Ordinary([0x4E],eeSI),
  Ordinary([0x4F],eeDI),
  ModRMGroup(1,[0xFE],eEb),
  ModRMGroup(1,[0xFF],eEv),
  ]
mnem_to_encodings[v(Push)]   = [
  Ordinary([0x06],eES),
  Ordinary([0x0E],eCS),
  Ordinary([0x16],eSS),
  Ordinary([0x1E],eDS),
  Ordinary([0x50],erAXr8),
  Ordinary([0x51],erCXr9),
  Ordinary([0x52],erDXr10),
  Ordinary([0x53],erBXr11),
  Ordinary([0x54],erSPr12),
  Ordinary([0x55],erBPr13),
  Ordinary([0x56],erSIr14),
  Ordinary([0x57],erDIr15),
  Ordinary([0x68],eIz),
  ModRMGroup(6,[0xFF],eEv),
  Ordinary([0x0F,0xA0],eFS),
  Ordinary([0x0F,0xA8],eGS),
  ]
mnem_to_encodings[v(Pop)]    = [
  Ordinary([0x07],eES),
  Ordinary([0x17],eSS),
  Ordinary([0x1F],eDS),
  Ordinary([0x58],erAXr8),
  Ordinary([0x59],erCXr9),
  Ordinary([0x5A],erDXr10),
  Ordinary([0x5B],erBXr11),
  Ordinary([0x5C],erSPr12),
  Ordinary([0x5D],erBPr13),
  Ordinary([0x5E],erSIr14),
  Ordinary([0x5F],erDIr15),
  ModRMGroup(0,[0x8F],eEv),
  Ordinary([0x0F,0xA1],eFS),
  Ordinary([0x0F,0xA9],eGS),
  ]
mnem_to_encodings[v(Pushaw)] = [Native16([0x60],eNone)]
mnem_to_encodings[v(Pushad)] = [Ordinary([0x60],eNone)]
mnem_to_encodings[v(Popaw)]  = [Native16([0x61],eNone)]
mnem_to_encodings[v(Popad)]  = [Ordinary([0x61],eNone)]
mnem_to_encodings[v(Bound)]  = [Ordinary([0x62],eGvMa)]
mnem_to_encodings[v(Arpl)]   = [Ordinary([0x63],eEwGw)]
mnem_to_encodings[v(Imul)]   = [
  Ordinary([0x69],eGvEvIz),
  Ordinary([0x6B],eGvEvIb),
  ModRMGroup(5,[0xF6],eEb),
  ModRMGroup(5,[0xF7],eEv),
  Ordinary([0x0F,0xAF],eGvEv),
  ]
mnem_to_encodings[v(Insb)]   = [Ordinary([0x6C],eYbDX)]
mnem_to_encodings[v(Insw)]   = [Native16([0x6D],eYwDX)]
mnem_to_encodings[v(Insd)]   = [Ordinary([0x6D],eYdDX)]
mnem_to_encodings[v(Outsb)]  = [Ordinary([0x6E],eDXXb)]
mnem_to_encodings[v(Outsw)]  = [Native16([0x6F],eDXXw)]
mnem_to_encodings[v(Outsd)]  = [Ordinary([0x6F],eDXXd)]
mnem_to_encodings[v(Test)]   = [
  Ordinary([0x84],eEbGb),
  Ordinary([0x85],eEvGv),
  Ordinary([0xA8],eALIb),
  Ordinary([0xA9],erAXIz),
  ModRMGroup(0,[0xF6],eEbIb),
  ModRMGroup(0,[0xF7],eEvIz),
  ]
mnem_to_encodings[v(Xchg)]   = [
  Ordinary([0x86],eEbGb),
#*Ordinary([0x86],eGbEb), ROLFAUTOMATE *)
  Ordinary([0x87],eEvGv),
#*Ordinary([0x87],eGvEv), ROLFAUTOMATE *)
  Ordinary([0x91],erAXrCXr9),
  Ordinary([0x92],erAXrDXr10),
  Ordinary([0x93],erAXrBXr11),
  Ordinary([0x94],erAXrSPr12),
  Ordinary([0x95],erAXrBPr13),
  Ordinary([0x96],erAXrSIr14),
  Ordinary([0x97],erAXrDIr15),
  ]
mnem_to_encodings[v(Mov)]    = [
  Ordinary([0xA2],eObAL),
  Ordinary([0x88],eEbGb),
  Ordinary([0xA3],eOvrAX),      
  Ordinary([0x89],eEvGv),
  Ordinary([0xA0],eALOb),
  Ordinary([0x8A],eGbEb),
  Ordinary([0xA1],erAXOv),
  Ordinary([0x8B],eGvEv),
  Ordinary([0x8C],eEvSw),
  Ordinary([0x8E],eSwEw),
  Ordinary([0xB0],eALR8LIb),
  Ordinary([0xB1],eCLR9LIb),
  Ordinary([0xB2],eDLR10LIb),
  Ordinary([0xB3],eBLR11LIb),
  Ordinary([0xB4],eAHR12LIb),
  Ordinary([0xB5],eCHR13LIb),
  Ordinary([0xB6],eDHR14LIb),
  Ordinary([0xB7],eBHR15LIb),
  Ordinary([0xB8],erAXr8Iv),
  Ordinary([0xB9],erCXr9Iv),
  Ordinary([0xBA],erDXr10Iv),
  Ordinary([0xBB],erBXr11Iv),
  Ordinary([0xBC],erSPr12Iv),
  Ordinary([0xBD],erBPr13Iv),
  Ordinary([0xBE],erSIr14Iv),
  Ordinary([0xBF],erDIr15Iv),
  ModRMGroup(0,[0xC6],eEbIb),
  ModRMGroup(0,[0xC7],eEvIz),
  Ordinary([0x0F,0x20],eRdCd),
  Ordinary([0x0F,0x21],eRdDd),
  Ordinary([0x0F,0x22],eCdRd),
  Ordinary([0x0F,0x23],eDdRd),
  ]
mnem_to_encodings[v(Lea)]    = [Ordinary([0x8D],eGvM)]
mnem_to_encodings[v(Nop)]    = [
  Ordinary([0x90],eNone),
  ModRMGroup(0,[0x0F,0x0D],eEv),
  ModRMGroup(0,[0x0F,0x1F],eEv),
  ]
mnem_to_encodings[v(Pause)]  = [Ordinary([0xF3,0x90],eNone)]
mnem_to_encodings[v(Cbw)]    = [Native16([0x98],eNone)]
mnem_to_encodings[v(Cwde)]   = [Ordinary([0x98],eNone)]
mnem_to_encodings[v(Cwd)]    = [Native16([0x99],eNone)]
mnem_to_encodings[v(Cdq)]    = [Ordinary([0x99],eNone)]
mnem_to_encodings[v(Wait)]   = [Ordinary([0x9B],eNone)]
mnem_to_encodings[v(Pushfw)] = [Native16([0x9C],eNone)]
mnem_to_encodings[v(Pushfd)] = [Ordinary([0x9C],eNone)]
mnem_to_encodings[v(Popfw)]  = [Native16([0x9D],eNone)]
mnem_to_encodings[v(Popfd)]  = [Ordinary([0x9D],eNone)]
mnem_to_encodings[v(Sahf)]   = [Ordinary([0x9E],eNone)]
mnem_to_encodings[v(Lahf)]   = [Ordinary([0x9F],eNone)]
mnem_to_encodings[v(Movsb)]  = [Ordinary([0xA4],eNone),Ordinary([0xA4],eXbYb)]
mnem_to_encodings[v(Movsw)]  = [Native16([0xA5],eNone),Native16([0xA5],eXwYw)]
mnem_to_encodings[v(Movsd)]  = [
  Ordinary([0xA5],eNone),
  Ordinary([0xA5],eXdYd),
  Ordinary([0xF2,0x0F,0x10],eVsdWsd),
  Ordinary([0xF2,0x0F,0x11],eWsdVsd),  
  ]
mnem_to_encodings[v(Cmpsb)]  = [Ordinary([0xA6],eNone),Ordinary([0xA6],eXbYb)]
mnem_to_encodings[v(Cmpsw)]  = [Native16([0xA7],eNone),Native16([0xA7],eXwYw)]
mnem_to_encodings[v(Cmpsd)]  = [
  Ordinary([0xA7],eNone),
  Ordinary([0xA7],eXdYd),
  Ordinary([0xF2,0x0F,0xC2],eVsdWsdIb),
  ]
mnem_to_encodings[v(Stosb)]  = [Ordinary([0xAA],eNone),Ordinary([0xAA],eYb)]
mnem_to_encodings[v(Stosw)]  = [Native16([0xAB],eNone),Native16([0xAB],eYw)]
mnem_to_encodings[v(Stosd)]  = [Ordinary([0xAB],eNone),Ordinary([0xAB],eYd)]
mnem_to_encodings[v(Lodsb)]  = [Ordinary([0xAC],eNone),Ordinary([0xAC],eXb)]
mnem_to_encodings[v(Lodsw)]  = [Native16([0xAD],eNone),Native16([0xAD],eXw)]
mnem_to_encodings[v(Lodsd)]  = [Ordinary([0xAD],eNone),Ordinary([0xAD],eXd)]
mnem_to_encodings[v(Scasb)]  = [Ordinary([0xAE],eNone),Ordinary([0xAE],eYb)]
mnem_to_encodings[v(Scasw)]  = [Native16([0xAF],eNone),Native16([0xAF],eYw)]
mnem_to_encodings[v(Scasd)]  = [Ordinary([0xAF],eNone),Ordinary([0xAF],eYd)]
mnem_to_encodings[v(Rol)]    = [
  ModRMGroup(0,[0xC0],eEbIb),
  ModRMGroup(0,[0xC1],eEvIb),
  ModRMGroup(0,[0xD0],eEb1),
  ModRMGroup(0,[0xD1],eEv1),
  ModRMGroup(0,[0xD2],eEbCL),
  ModRMGroup(0,[0xD3],eEvCL),
  ]
mnem_to_encodings[v(Ror)]    = [
  ModRMGroup(1,[0xC0],eEbIb),
  ModRMGroup(1,[0xC1],eEvIb),
  ModRMGroup(1,[0xD0],eEb1),
  ModRMGroup(1,[0xD1],eEv1),
  ModRMGroup(1,[0xD2],eEbCL),
  ModRMGroup(1,[0xD3],eEvCL),
  ]
mnem_to_encodings[v(Rcl)]    = [
  ModRMGroup(2,[0xC0],eEbIb),
  ModRMGroup(2,[0xC1],eEvIb),
  ModRMGroup(2,[0xD0],eEb1),
  ModRMGroup(2,[0xD1],eEv1),
  ModRMGroup(2,[0xD2],eEbCL),
  ModRMGroup(2,[0xD3],eEvCL),
  ]
mnem_to_encodings[v(Rcr)]    = [
  ModRMGroup(3,[0xC0],eEbIb),
  ModRMGroup(3,[0xC1],eEvIb),
  ModRMGroup(3,[0xD0],eEb1),
  ModRMGroup(3,[0xD1],eEv1),
  ModRMGroup(3,[0xD2],eEbCL),
  ModRMGroup(3,[0xD3],eEvCL),
  ]
mnem_to_encodings[v(Shl)]    = [
  ModRMGroup(4,[0xC0],eEbIb),
  ModRMGroup(4,[0xC1],eEvIb),
  ModRMGroup(4,[0xD0],eEb1),
  ModRMGroup(4,[0xD1],eEv1),
  ModRMGroup(4,[0xD2],eEbCL),
  ModRMGroup(4,[0xD3],eEvCL),
  ]
mnem_to_encodings[v(Shr)]    = [
  ModRMGroup(5,[0xC0],eEbIb),
  ModRMGroup(5,[0xC1],eEvIb),
  ModRMGroup(5,[0xD0],eEb1),
  ModRMGroup(5,[0xD1],eEv1),
  ModRMGroup(5,[0xD2],eEbCL),
  ModRMGroup(5,[0xD3],eEvCL),
  ]
mnem_to_encodings[v(Sal)]    = [
  ModRMGroup(6,[0xC0],eEbIb),
  ModRMGroup(6,[0xC1],eEvIb),
  ModRMGroup(6,[0xD0],eEb1),
  ModRMGroup(6,[0xD1],eEv1),
  ModRMGroup(6,[0xD2],eEbCL),
  ModRMGroup(6,[0xD3],eEvCL),
  ]
mnem_to_encodings[v(Sar)]    = [
  ModRMGroup(7,[0xC0],eEbIb),
  ModRMGroup(7,[0xC1],eEvIb),
  ModRMGroup(7,[0xD0],eEb1),
  ModRMGroup(7,[0xD1],eEv1),
  ModRMGroup(7,[0xD2],eEbCL),
  ModRMGroup(7,[0xD3],eEvCL),
  ]
mnem_to_encodings[v(Ret)]    = [
  Ordinary([0xC2],eIw),
  Ordinary([0xC3],eNone),
  ]
mnem_to_encodings[v(Les)]    = [Ordinary([0xC4],eGzMp)]
mnem_to_encodings[v(Lds)]    = [Ordinary([0xC5],eGzMp)]
mnem_to_encodings[v(Enter)]  = [Ordinary([0xC8],eIwIb)]
mnem_to_encodings[v(Leave)]  = [Ordinary([0xC9],eNone)]
mnem_to_encodings[v(Retf)]   = [
  Ordinary([0xCA],eIw),
  Ordinary([0xCB],eNone),
  ]
mnem_to_encodings[v(Int3)]   = [Ordinary([0xCC],eNone)]
mnem_to_encodings[v(Int)]    = [Ordinary([0xCD],eIb)]
mnem_to_encodings[v(Into)]   = [Ordinary([0xCE],eNone)]
mnem_to_encodings[v(Iretw)]  = [Native16([0xCF],eNone)]
mnem_to_encodings[v(Iretd)]  = [Ordinary([0xCF],eNone)]
mnem_to_encodings[v(Aam)]    = [
  Ordinary([0xD4,0x0A],eNone),
  Ordinary([0xD4],eIb),
  ]
mnem_to_encodings[v(Aad)]    = [
  Ordinary([0xD5,0x0A],eNone),
  Ordinary([0xD5],eIb)
  ]
mnem_to_encodings[v(Salc)]   = [Ordinary([0xD6],eNone)]
mnem_to_encodings[v(Xlat)]   = [Ordinary([0xD7],eMbEbx)]
mnem_to_encodings[v(In)]     = [
  Ordinary([0xE4],eALIb),
  Ordinary([0xE5],eeAXIb),
  Ordinary([0xEC],eALDX),
  Ordinary([0xED],eeAXDX),
  ]
mnem_to_encodings[v(Out)]    = [
  Ordinary([0xE6],eIbAL),
  Ordinary([0xE7],eIbeAX),
  Ordinary([0xEE],eDXAL),
  Ordinary([0xEF],eDXeAX),
  ]
mnem_to_encodings[v(Icebp)]  = [Ordinary([0xF1],eNone)]
mnem_to_encodings[v(Hlt)]    = [Ordinary([0xF4],eNone)]
mnem_to_encodings[v(Cmc)]    = [Ordinary([0xF5],eNone)]
mnem_to_encodings[v(Clc)]    = [Ordinary([0xF8],eNone)]
mnem_to_encodings[v(Stc)]    = [Ordinary([0xF9],eNone)]
mnem_to_encodings[v(Cli)]    = [Ordinary([0xFA],eNone)]
mnem_to_encodings[v(Sti)]    = [Ordinary([0xFB],eNone)]
mnem_to_encodings[v(Cld)]    = [Ordinary([0xFC],eNone)]
mnem_to_encodings[v(Std)]    = [Ordinary([0xFD],eNone)]
mnem_to_encodings[v(Not)]    = [
  ModRMGroup(2,[0xF6],eEb),
  ModRMGroup(2,[0xF7],eEv),
  ]
mnem_to_encodings[v(Neg)]    = [
  ModRMGroup(3,[0xF6],eEb),
  ModRMGroup(3,[0xF7],eEv),
  ]
mnem_to_encodings[v(Mul)]    = [
  ModRMGroup(4,[0xF6],eEb),
  ModRMGroup(4,[0xF7],eEv),
  ]
mnem_to_encodings[v(Div)]    = [
  ModRMGroup(6,[0xF6],eEb),
  ModRMGroup(6,[0xF7],eEv),
  ]
mnem_to_encodings[v(Idiv)]   = [
  ModRMGroup(7,[0xF6],eEb),
  ModRMGroup(7,[0xF7],eEv),
  ]
mnem_to_encodings[v(Call)]   = [
  ModRMGroup(2,[0xFF],eEv),
  ]
mnem_to_encodings[v(CallF)]  = [
  Ordinary([0x9A],eAp),
  ModRMGroup(3,[0xFF],eEv),
  ]
mnem_to_encodings[v(Jmp)]    = [
  Ordinary([0xE9],[OJz]),
  ModRMGroup(4,[0xFF],eEv),
  ]
mnem_to_encodings[v(JmpF)]   = [
  ModRMGroup(5,[0xFF],eEv),
  ]

mnem_to_encodings[v(Fadd)]    = [
  ModRMGroup(0,[0xD8],eSt0Real4),
  ModRMGroup(0,[0xD8],eSt0StN),
  ModRMGroup(0,[0xDC],eSt0Real8),
  ModRMGroup(0,[0xDC],eStNSt0),
  ]
mnem_to_encodings[v(Fmul)]    = [
  ModRMGroup(1,[0xD8],eSt0Real4),
  ModRMGroup(1,[0xD8],eSt0StN),
  ModRMGroup(1,[0xDC],eSt0Real8),
  ModRMGroup(1,[0xDC],eStNSt0),
  ]
mnem_to_encodings[v(Fcom)]    = [
  ModRMGroup(2,[0xD8],eSt0Real4),
  ModRMGroup(2,[0xD8],eSt0StN),
  ModRMGroup(2,[0xDC],eSt0Real8),
  ]
mnem_to_encodings[v(Fcomp)]   = [
  ModRMGroup(3,[0xD8],eSt0Real4),
  ModRMGroup(3,[0xD8],eSt0StN),
  ModRMGroup(3,[0xDC],eSt0Real8),
  ]
mnem_to_encodings[v(Fsub)]    = [
  ModRMGroup(4,[0xD8],eSt0Real4),
  ModRMGroup(4,[0xD8],eSt0StN),
  ModRMGroup(4,[0xDC],eSt0Real8),
  ModRMGroup(4,[0xDC],eStNSt0),
  ]
mnem_to_encodings[v(Fsubr)]   = [
  ModRMGroup(5,[0xD8],eSt0Real4),
  ModRMGroup(5,[0xD8],eSt0StN),
  ModRMGroup(5,[0xDC],eSt0Real8),
  ModRMGroup(5,[0xDC],eStNSt0),
  ]
mnem_to_encodings[v(Fdiv)]    = [
  ModRMGroup(6,[0xD8],eSt0Real4),
  ModRMGroup(6,[0xD8],eSt0StN),
  ModRMGroup(6,[0xDC],eSt0Real8),
  ModRMGroup(6,[0xDC],eStNSt0),
  ]
mnem_to_encodings[v(Fdivr)]   = [
  ModRMGroup(7,[0xD8],eSt0Real4),
  ModRMGroup(7,[0xD8],eSt0StN),
  ModRMGroup(7,[0xDC],eSt0Real8),
  ModRMGroup(7,[0xDC],eStNSt0),
  ]
mnem_to_encodings[v(Fld)]     = [
  ModRMGroup(0,[0xD9],eReal4),
  ModRMGroup(0,[0xD9],eSt0StN),
  ModRMGroup(5,[0xDB],eReal10),
  ModRMGroup(0,[0xDD],eReal8),
  ]
mnem_to_encodings[v(Fxch)]     = [ModRMGroup(1,[0xD9],eSt0StN)]
mnem_to_encodings[v(Fnop)]     = [Ordinary([0xD9,0xD0],eNone)]
mnem_to_encodings[v(Fchs)]     = [Ordinary([0xD9,0xE0],eNone)]
mnem_to_encodings[v(Fabs)]     = [Ordinary([0xD9,0xE1],eNone)]
mnem_to_encodings[v(Ftst)]     = [Ordinary([0xD9,0xE4],eNone)]
mnem_to_encodings[v(Fxam)]     = [Ordinary([0xD9,0xE5],eNone)]
mnem_to_encodings[v(Fld1)]     = [Ordinary([0xD9,0xE8],eNone)]
mnem_to_encodings[v(Fldl2t)]   = [Ordinary([0xD9,0xE9],eNone)]
mnem_to_encodings[v(Fldl2e)]   = [Ordinary([0xD9,0xEA],eNone)]
mnem_to_encodings[v(Fldpi)]    = [Ordinary([0xD9,0xEB],eNone)]
mnem_to_encodings[v(Fldlg2)]   = [Ordinary([0xD9,0xEC],eNone)]
mnem_to_encodings[v(Fldln2)]   = [Ordinary([0xD9,0xED],eNone)]
mnem_to_encodings[v(Fldz)]     = [Ordinary([0xD9,0xEE],eNone)]
mnem_to_encodings[v(F2xm1)]    = [Ordinary([0xD9,0xF0],eNone)]
mnem_to_encodings[v(Fyl2x)]    = [Ordinary([0xD9,0xF1],eNone)]
mnem_to_encodings[v(Fptan)]    = [Ordinary([0xD9,0xF2],eNone)]
mnem_to_encodings[v(Fpatan)]   = [Ordinary([0xD9,0xF3],eNone)]
mnem_to_encodings[v(Fxtract)]  = [Ordinary([0xD9,0xF4],eNone)]
mnem_to_encodings[v(Fprem1)]   = [Ordinary([0xD9,0xF5],eNone)]
mnem_to_encodings[v(Fdecstp)]  = [Ordinary([0xD9,0xF6],eNone)]
mnem_to_encodings[v(Fincstp)]  = [Ordinary([0xD9,0xF7],eNone)]
mnem_to_encodings[v(Fprem)]    = [Ordinary([0xD9,0xF8],eNone)]
mnem_to_encodings[v(Fyl2xp1)]  = [Ordinary([0xD9,0xF9],eNone)]
mnem_to_encodings[v(Fsqrt)]    = [Ordinary([0xD9,0xFA],eNone)]
mnem_to_encodings[v(Fsincos)]  = [Ordinary([0xD9,0xFB],eNone)]
mnem_to_encodings[v(Frndint)]  = [Ordinary([0xD9,0xFC],eNone)]
mnem_to_encodings[v(Fscale)]   = [Ordinary([0xD9,0xFD],eNone)]
mnem_to_encodings[v(Fsin)]     = [Ordinary([0xD9,0xFE],eNone)]
mnem_to_encodings[v(Fcos)]     = [Ordinary([0xD9,0xFF],eNone)]
mnem_to_encodings[v(Fst)]      = [
  ModRMGroup(2,[0xD9],eReal4),
  ModRMGroup(2,[0xDD],eReal8),
  ModRMGroup(2,[0xDD],eStN),
  ]
mnem_to_encodings[v(Fstp)]     = [
  ModRMGroup(3,[0xD9],eReal4),
  ModRMGroup(7,[0xDB],eReal10),
  ModRMGroup(3,[0xDD],eReal8),
  ModRMGroup(3,[0xDD],eStN),
  ]
mnem_to_encodings[v(Fldenv)]   = [ModRMGroup(4,[0xD9],eFPEnvLow)]
mnem_to_encodings[v(Fldcw)]    = [ModRMGroup(5,[0xD9],eMw)]
mnem_to_encodings[v(Fstenv)]   = [ModRMGroup(6,[0xD9],eFPEnvLow)]
mnem_to_encodings[v(Fstcw)]    = [ModRMGroup(7,[0xD9],eMw)]
mnem_to_encodings[v(Fiadd)]    = [
  ModRMGroup(0,[0xDA],eMd),
  ModRMGroup(0,[0xDE],eMw),
  ]
mnem_to_encodings[v(Fimul)]    = [
  ModRMGroup(1,[0xDA],eMd),
  ModRMGroup(1,[0xDE],eMw),
  ]
mnem_to_encodings[v(Ficom)]    = [
  ModRMGroup(2,[0xDA],eMd),
  ModRMGroup(2,[0xDE],eMw),
  ]
mnem_to_encodings[v(Ficomp)]   = [
  ModRMGroup(3,[0xDA],eMd),
  ModRMGroup(3,[0xDE],eMw),
  ]
mnem_to_encodings[v(Fisub)]    = [
  ModRMGroup(4,[0xDA],eMd),
  ModRMGroup(4,[0xDE],eMw),
  ]
mnem_to_encodings[v(Fisubr)]   = [
  ModRMGroup(5,[0xDA],eMd),
  ModRMGroup(5,[0xDE],eMw),
  ]
mnem_to_encodings[v(Fidiv)]    = [
  ModRMGroup(6,[0xDA],eMd),
  ModRMGroup(6,[0xDE],eMw),
  ]
mnem_to_encodings[v(Fidivr)]   = [
  ModRMGroup(7,[0xDA],eMd),
  ModRMGroup(7,[0xDE],eMw),
  ]
mnem_to_encodings[v(Fcmovb)]   = [ModRMGroup(0,[0xDA],eSt0StN)]
mnem_to_encodings[v(Fcmove)]   = [ModRMGroup(1,[0xDA],eSt0StN)]
mnem_to_encodings[v(Fcmovbe)]  = [ModRMGroup(2,[0xDA],eSt0StN)]
mnem_to_encodings[v(Fcmovu)]   = [ModRMGroup(3,[0xDA],eSt0StN)]
mnem_to_encodings[v(Fucompp)]  = [Ordinary([0xDA,0xE9],eNone)]
mnem_to_encodings[v(Fcmovnb)]  = [ModRMGroup(0,[0xDB],eSt0StN)]
mnem_to_encodings[v(Fcmovne)]  = [ModRMGroup(1,[0xDB],eSt0StN)]
mnem_to_encodings[v(Fcmovnbe)] = [ModRMGroup(2,[0xDB],eSt0StN)]
mnem_to_encodings[v(Fcmovnu)]  = [ModRMGroup(3,[0xDB],eSt0StN)]
mnem_to_encodings[v(Fclex)]    = [Ordinary([0xDB,0xE2],eNone)]
mnem_to_encodings[v(Finit)]    = [Ordinary([0xDB,0xE3],eNone)]
mnem_to_encodings[v(Fucomi)]   = [ModRMGroup(5,[0xDB],eSt0StN)]
mnem_to_encodings[v(Fcomi)]    = [ModRMGroup(6,[0xDB],eSt0StN)]
mnem_to_encodings[v(Fild)]     = [
  ModRMGroup(0,[0xDB],eMd),
  ModRMGroup(0,[0xDF],eMw),
  ModRMGroup(5,[0xDF],eReal8),
  ]
mnem_to_encodings[v(Fisttp)]   = [
  ModRMGroup(1,[0xDB],eMd),
  ModRMGroup(1,[0xDD],eMq),
  ModRMGroup(1,[0xDF],eMw),
  ]
mnem_to_encodings[v(Fist)]     = [
  ModRMGroup(2,[0xDB],eMd),
  ModRMGroup(2,[0xDF],eMw),
  ]
mnem_to_encodings[v(Fistp)]    = [
  ModRMGroup(3,[0xDB],eMd),
  ModRMGroup(3,[0xDF],eMw),
  ModRMGroup(7,[0xDF],eReal8),
  ]
mnem_to_encodings[v(Frstor)]   = [ModRMGroup(4,[0xDD],eFPEnv)]
mnem_to_encodings[v(Fsave)]    = [ModRMGroup(6,[0xDD],eFPEnv)]
mnem_to_encodings[v(Fstsw)]    = [
  ModRMGroup(7,[0xDD],eMw),
  Ordinary([0xDF,0xE0],eAX),
  ]
mnem_to_encodings[v(Ffree)]    = [ModRMGroup(0,[0xDD],eStN)]
mnem_to_encodings[v(Fucom)]    = [ModRMGroup(4,[0xDD],eStN)]
mnem_to_encodings[v(Fucomp)]   = [ModRMGroup(5,[0xDD],eStN)]
mnem_to_encodings[v(Faddp)]    = [ModRMGroup(0,[0xDE],eStNSt0)]
mnem_to_encodings[v(Fmulp)]    = [ModRMGroup(1,[0xDE],eStNSt0)]
mnem_to_encodings[v(Fcompp)]   = [Ordinary([0xDE,0xD9],eNone)]
mnem_to_encodings[v(Fsubrp)]   = [ModRMGroup(4,[0xDE],eStNSt0)]
mnem_to_encodings[v(Fsubp)]    = [ModRMGroup(5,[0xDE],eStNSt0)]
mnem_to_encodings[v(Fdivrp)]   = [ModRMGroup(6,[0xDE],eStNSt0)]
mnem_to_encodings[v(Fdivp)]    = [ModRMGroup(7,[0xDE],eStNSt0)]
mnem_to_encodings[v(Fbld)]     = [ModRMGroup(4,[0xDF],eReal10)]
mnem_to_encodings[v(Fbstp)]    = [ModRMGroup(6,[0xDF],eReal10)]
mnem_to_encodings[v(Fucomip)]  = [ModRMGroup(5,[0xDF],eSt0StN)]
mnem_to_encodings[v(Fcomip)]   = [ModRMGroup(6,[0xDF],eSt0StN)]
mnem_to_encodings[v(Sldt)]     = [
  ModRMGroup(0,[0x0F,0x00],eMw),
  ModRMGroup(0,[0x0F,0x00],eRv),
  ]
mnem_to_encodings[v(Str)]      = [
  ModRMGroup(1,[0x0F,0x00],eMw),
  ModRMGroup(1,[0x0F,0x00],eRv),
  ]
mnem_to_encodings[v(Lldt)]     = [ModRMGroup(2,[0x0F,0x00],eEw)]
mnem_to_encodings[v(Ltr)]      = [ModRMGroup(3,[0x0F,0x00],eEw)]
mnem_to_encodings[v(Verr)]     = [ModRMGroup(4,[0x0F,0x00],eEw)]
mnem_to_encodings[v(Verw)]     = [ModRMGroup(5,[0x0F,0x00],eEw)]
mnem_to_encodings[v(Sgdt)]     = [ModRMGroup(0,[0x0F,0x01],eMs)]
mnem_to_encodings[v(Sidt)]     = [ModRMGroup(1,[0x0F,0x01],eMs)]
mnem_to_encodings[v(Lgdt)]     = [ModRMGroup(2,[0x0F,0x01],eMs)]
mnem_to_encodings[v(Lidt)]     = [ModRMGroup(3,[0x0F,0x01],eMs)]
mnem_to_encodings[v(Smsw)]     = [
  ModRMGroup(4,[0x0F,0x01],eMw),
  ModRMGroup(4,[0x0F,0x01],eRv),
  ]
mnem_to_encodings[v(Lmsw)]     = [
  ModRMGroup(6,[0x0F,0x01],eMw),
  ModRMGroup(6,[0x0F,0x01],eRw)
  ]
mnem_to_encodings[v(Invlpg)]   = [ModRMGroup(7,[0x0F,0x01],eMb)]
mnem_to_encodings[v(Vmcall)]   = [Ordinary([0x0F,0x01,0xC1],eNone)]
mnem_to_encodings[v(Vmlaunch)] = [Ordinary([0x0F,0x01,0xC2],eNone)]
mnem_to_encodings[v(Vmresume)] = [Ordinary([0x0F,0x01,0xC3],eNone)]
mnem_to_encodings[v(Vmxoff)]   = [Ordinary([0x0F,0x01,0xC4],eNone)]
mnem_to_encodings[v(Monitor)]  = [Ordinary([0x0F,0x01,0xC8],eNone)]
mnem_to_encodings[v(Mwait)]    = [Ordinary([0x0F,0x01,0xC9],eNone)]
mnem_to_encodings[v(Lar)]      = [Ordinary([0x0F,0x02],eGvEw)]
mnem_to_encodings[v(Lsl)]      = [Ordinary([0x0F,0x03],eGvEw)]
mnem_to_encodings[v(Syscall)]  = [Ordinary([0x0F,0x05],eNone)]
mnem_to_encodings[v(Clts)]     = [Ordinary([0x0F,0x06],eNone)]
mnem_to_encodings[v(Sysret)]   = [Ordinary([0x0F,0x07],eNone)]
mnem_to_encodings[v(Invd)]     = [Ordinary([0x0F,0x08],eNone)]
mnem_to_encodings[v(Wbinvd)]   = [Ordinary([0x0F,0x09],eNone)]
mnem_to_encodings[v(Ud2)]      = [Ordinary([0x0F,0x0B],eNone)]
mnem_to_encodings[v(Movups)] = [
  Ordinary([0x0F,0x10],eVpsWps),
  Ordinary([0x0F,0x11],eWpsVps),
  ]
mnem_to_encodings[v(Movss)] = [
  Ordinary([0xF3,0x0F,0x10],eVssWss),
  Ordinary([0xF3,0x0F,0x11],eWssVss),
  ]
mnem_to_encodings[v(Movupd)] = [
  Ordinary([0x66,0x0F,0x10],eVpdWpd),
  Ordinary([0x66,0x0F,0x11],eWpdVpd),
  ]
mnem_to_encodings[v(Movlps)] = [
  Ordinary([0x0F,0x12],eVqMq),
  Ordinary([0x0F,0x13],eMqVq),
  ]
mnem_to_encodings[v(Movhlps)] = [Ordinary([0x0F,0x12],eVqUq)]
mnem_to_encodings[v(Movsldup)] = [Ordinary([0xF3,0x0F,0x12],eVqWq)]
mnem_to_encodings[v(Movlpd)] = [
  Ordinary([0x66,0x0F,0x12],eVqMq),
  Ordinary([0x66,0x0F,0x13],eMqVq),
  ]
mnem_to_encodings[v(Movddup)]  = [Ordinary([0xF2,0x0F,0x12],eVqWq)]
mnem_to_encodings[v(Unpcklpd)] = [Ordinary([0x0F,0x14],eVpdWq)]
mnem_to_encodings[v(Unpcklps)] = [Ordinary([0x66,0x0F,0x14],eVpsWq)]
mnem_to_encodings[v(Unpckhpd)] = [Ordinary([0x0F,0x15],eVpdWq)]
mnem_to_encodings[v(Unpckhps)] = [Ordinary([0x66,0x0F,0x15],eVpsWq)]
mnem_to_encodings[v(Movhps)] = [
  Ordinary([0x0F,0x16],eVqMq),
  Ordinary([0x0F,0x17],eMqVq),
  ]
mnem_to_encodings[v(Movlhps)]  = [Ordinary([0x0F,0x16],eVqUq)]
mnem_to_encodings[v(Movshdup)] = [Ordinary([0xF3,0x0F,0x16],eVqWq)]
mnem_to_encodings[v(Movhpd)] = [
  Ordinary([0x66,0x0F,0x16],eVqMq),
  Ordinary([0x66,0x0F,0x17],eMqVq),
  ]
mnem_to_encodings[v(Prefetchnta)] = [ModRMGroup(0,[0x0F,0x18],eMb),]
mnem_to_encodings[v(Prefetcht0)]  = [ModRMGroup(1,[0x0F,0x18],eMb),]
mnem_to_encodings[v(Prefetcht1)]  = [ModRMGroup(2,[0x0F,0x18],eMb),]
mnem_to_encodings[v(Prefetcht2)]  = [ModRMGroup(3,[0x0F,0x18],eMb),]
mnem_to_encodings[v(Movaps)] = [
  Ordinary([0x0F,0x28],eVpdWpd),
  Ordinary([0x0F,0x29],eWpdVpd),
  ]
mnem_to_encodings[v(Movapd)] = [
  Ordinary([0x66,0x0F,0x28],eVpsWps),
  Ordinary([0x66,0x0F,0x29],eWpsVps),
  ]
mnem_to_encodings[v(Cvtpi2ps)]  = [Ordinary([0x0F,0x2A],eVpsQpi)]
mnem_to_encodings[v(Cvtsi2ss)]  = [Ordinary([0xF3,0x0F,0x2A],eVssEd_q)]
mnem_to_encodings[v(Cvtpi2pd)]  = [Ordinary([0x66,0x0F,0x2A],eVpdQpi)]
mnem_to_encodings[v(Cvtsi2sd)]  = [Ordinary([0xF2,0x0F,0x2A],eVsdEd_q)]
mnem_to_encodings[v(Movntps)]   = [Ordinary([0x0F,0x2B],eMpsVps)]
mnem_to_encodings[v(Movntpd)]   = [Ordinary([0x66,0x0F,0x2B],eMpdVpd)]
mnem_to_encodings[v(Cvttps2pi)] = [Ordinary([0x0F,0x2C],ePpiWps)]
mnem_to_encodings[v(Cvttss2si)] = [Ordinary([0xF3,0x0F,0x2C],eGdWss)]
mnem_to_encodings[v(Cvttpd2pi)] = [Ordinary([0x66,0x0F,0x2C],ePpiWpd)]
mnem_to_encodings[v(Cvttsd2si)] = [Ordinary([0xF2,0x0F,0x2C],eGdWsd)]
mnem_to_encodings[v(Cvtps2pi)]  = [Ordinary([0x0F,0x2D],ePpiWps)]
mnem_to_encodings[v(Cvtss2si)]  = [Ordinary([0xF3,0x0F,0x2D],eGd_qWss)]
mnem_to_encodings[v(Cvtpd2pi)]  = [Ordinary([0x66,0x0F,0x2D],ePpiWpd)]
mnem_to_encodings[v(Cvtsd2si)]  = [Ordinary([0xF2,0x0F,0x2D],eGd_qWsd)]
mnem_to_encodings[v(Ucomiss)]   = [Ordinary([0x0F,0x2E],eVsdWsd)]
mnem_to_encodings[v(Ucomisd)]   = [Ordinary([0x66,0x0F,0x2E],eVssWss)]
mnem_to_encodings[v(Comiss)]    = [Ordinary([0x0F,0x2F],eVsdWsd)]      
mnem_to_encodings[v(Comisd)]    = [Ordinary([0x66,0x0F,0x2F],eVssWss)]
mnem_to_encodings[v(Wrmsr)]     = [Ordinary([0x0F,0x30],eNone)]
mnem_to_encodings[v(Rdtsc)]     = [Ordinary([0x0F,0x31],eNone)]
mnem_to_encodings[v(Rdmsr)]     = [Ordinary([0x0F,0x32],eNone)]
mnem_to_encodings[v(Rdpmc)]     = [Ordinary([0x0F,0x33],eNone)]
mnem_to_encodings[v(Sysenter)]  = [Ordinary([0x0F,0x34],eNone)]
mnem_to_encodings[v(Sysexit)]   = [Ordinary([0x0F,0x35],eNone)]
mnem_to_encodings[v(Getsec)]    = [Ordinary([0x0F,0x37],eNone)]
mnem_to_encodings[v(Cmovo)]     = [Ordinary([0x0F,0x40],eGvEv)]
mnem_to_encodings[v(Cmovno)]    = [Ordinary([0x0F,0x41],eGvEv)]
mnem_to_encodings[v(Cmovb)]     = [Ordinary([0x0F,0x42],eGvEv)]
mnem_to_encodings[v(Cmovae)]    = [Ordinary([0x0F,0x43],eGvEv)]
mnem_to_encodings[v(Cmovz)]     = [Ordinary([0x0F,0x44],eGvEv)]
mnem_to_encodings[v(Cmovnz)]    = [Ordinary([0x0F,0x45],eGvEv)]
mnem_to_encodings[v(Cmovbe)]    = [Ordinary([0x0F,0x46],eGvEv)]
mnem_to_encodings[v(Cmova)]     = [Ordinary([0x0F,0x47],eGvEv)]
mnem_to_encodings[v(Cmovs)]     = [Ordinary([0x0F,0x48],eGvEv)]
mnem_to_encodings[v(Cmovns)]    = [Ordinary([0x0F,0x49],eGvEv)]
mnem_to_encodings[v(Cmovp)]     = [Ordinary([0x0F,0x4A],eGvEv)]
mnem_to_encodings[v(Cmovnp)]    = [Ordinary([0x0F,0x4B],eGvEv)]
mnem_to_encodings[v(Cmovl)]     = [Ordinary([0x0F,0x4C],eGvEv)]
mnem_to_encodings[v(Cmovge)]    = [Ordinary([0x0F,0x4D],eGvEv)]
mnem_to_encodings[v(Cmovle)]    = [Ordinary([0x0F,0x4E],eGvEv)]
mnem_to_encodings[v(Cmovg)]     = [Ordinary([0x0F,0x4F],eGvEv)]
mnem_to_encodings[v(Movmskps)]  = [Ordinary([0x0F,0x50],eGdUps)]
mnem_to_encodings[v(Movmskpd)]  = [Ordinary([0x66,0x0F,0x50],eGdUpd)]
mnem_to_encodings[v(Sqrtps)]    = [Ordinary([0x0F,0x51],eVpsWps)]
mnem_to_encodings[v(Sqrtss)]    = [Ordinary([0xF3,0x0F,0x51],eVssWss)]
mnem_to_encodings[v(Sqrtpd)]    = [Ordinary([0x66,0x0F,0x51],eVpdWpd)]
mnem_to_encodings[v(Sqrtsd)]    = [Ordinary([0xF2,0x0F,0x51],eVsdWsd)]
mnem_to_encodings[v(Rsqrtps)]   = [Ordinary([0x0F,0x52],eVpsWps)]
mnem_to_encodings[v(Rsqrtss)]   = [Ordinary([0xF3,0x0F,0x52],eVssWss)]
mnem_to_encodings[v(Rcpps)]     = [Ordinary([0x0F,0x53],eVpsWps)]
mnem_to_encodings[v(Rcpss)]     = [Ordinary([0xF3,0x0F,0x53],eVssWss)]
mnem_to_encodings[v(Andps)]     = [Ordinary([0x0F,0x54],eVpsWps)]
mnem_to_encodings[v(Andpd)]     = [Ordinary([0x66,0x0F,0x54],eVpdWpd)]
mnem_to_encodings[v(Andnps)]    = [Ordinary([0x0F,0x55],eVpsWps)]
mnem_to_encodings[v(Andnpd)]    = [Ordinary([0x66,0x0F,0x55],eVpdWpd)]
mnem_to_encodings[v(Orps)]      = [Ordinary([0x0F,0x56],eVpsWps)]
mnem_to_encodings[v(Orpd)]      = [Ordinary([0x66,0x0F,0x56],eVpdWpd)]
mnem_to_encodings[v(Xorps)]     = [Ordinary([0x0F,0x57],eVpsWps)]
mnem_to_encodings[v(Xorpd)]     = [Ordinary([0x66,0x0F,0x57],eVpdWpd)]
mnem_to_encodings[v(Addps)]     = [Ordinary([0x0F,0x58],eVpsWps)]
mnem_to_encodings[v(Addss)]     = [Ordinary([0xF3,0x0F,0x58],eVssWss)]
mnem_to_encodings[v(Addpd)]     = [Ordinary([0x66,0x0F,0x58],eVpdWpd)]
mnem_to_encodings[v(Addsd)]     = [Ordinary([0xF2,0x0F,0x58],eVsdWsd)]
mnem_to_encodings[v(Mulps)]     = [Ordinary([0x0F,0x59],eVpsWps)]
mnem_to_encodings[v(Mulss)]     = [Ordinary([0xF3,0x0F,0x59],eVssWss)]
mnem_to_encodings[v(Mulpd)]     = [Ordinary([0x66,0x0F,0x59],eVpdWpd)]
mnem_to_encodings[v(Mulsd)]     = [Ordinary([0xF2,0x0F,0x59],eVsdWsd)]
mnem_to_encodings[v(Cvtps2pd)]  = [Ordinary([0x0F,0x5A],eVpdWps)]
mnem_to_encodings[v(Cvtss2sd)]  = [Ordinary([0xF3,0x0F,0x5A],eVssWss)]
mnem_to_encodings[v(Cvtpd2ps)]  = [Ordinary([0x66,0x0F,0x5A],eVpsWpd)]
mnem_to_encodings[v(Cvtsd2ss)]  = [Ordinary([0xF2,0x0F,0x5A],eVsdWsd)]
mnem_to_encodings[v(Cvtdq2ps)]  = [Ordinary([0x0F,0x5B],eVpsWps)]      
mnem_to_encodings[v(Cvttps2dq)] = [Ordinary([0xF3,0x0F,0x5B],eVdqWps)]
mnem_to_encodings[v(Cvtps2dq)]  = [Ordinary([0x66,0x0F,0x5B],eVdqWps)]
mnem_to_encodings[v(Subps)]     = [Ordinary([0x0F,0x5C],eVpsWps)]
mnem_to_encodings[v(Subss)]     = [Ordinary([0xF3,0x0F,0x5C],eVssWss)]
mnem_to_encodings[v(Subpd)]     = [Ordinary([0x66,0x0F,0x5C],eVpdWpd)]
mnem_to_encodings[v(Subsd)]     = [Ordinary([0xF2,0x0F,0x5C],eVsdWsd)]
mnem_to_encodings[v(Minps)]     = [Ordinary([0x0F,0x5D],eVpsWps)]
mnem_to_encodings[v(Minss)]     = [Ordinary([0xF3,0x0F,0x5D],eVssWss)]
mnem_to_encodings[v(Minpd)]     = [Ordinary([0x66,0x0F,0x5D],eVpdWpd)]
mnem_to_encodings[v(Minsd)]     = [Ordinary([0xF2,0x0F,0x5D],eVsdWsd)]
mnem_to_encodings[v(Divps)]     = [Ordinary([0x0F,0x5E],eVpsWps)]
mnem_to_encodings[v(Divss)]     = [Ordinary([0xF3,0x0F,0x5E],eVssWss)]
mnem_to_encodings[v(Divpd)]     = [Ordinary([0x66,0x0F,0x5E],eVpdWpd)]
mnem_to_encodings[v(Divsd)]     = [Ordinary([0xF2,0x0F,0x5E],eVsdWsd)]
mnem_to_encodings[v(Maxps)]     = [Ordinary([0x0F,0x5F],eVpsWps)]
mnem_to_encodings[v(Maxss)]     = [Ordinary([0xF3,0x0F,0x5F],eVssWss)]
mnem_to_encodings[v(Maxpd)]     = [Ordinary([0x66,0x0F,0x5F],eVpdWpd)]
mnem_to_encodings[v(Maxsd)]     = [Ordinary([0xF2,0x0F,0x5F],eVsdWsd)]
mnem_to_encodings[v(Punpcklbw)] = [
  Ordinary([0x0F,0x60],ePqQd),
  Ordinary([0x66,0x0F,0x60],eVdqWdq),
  ]
mnem_to_encodings[v(Punpcklwd)] = [
  Ordinary([0x0F,0x61],ePqQd),
  Ordinary([0x66,0x0F,0x61],eVdqWdq),
  ]
mnem_to_encodings[v(Punpckldq)] = [
  Ordinary([0x0F,0x62],ePqQd),
  Ordinary([0x66,0x0F,0x62],eVdqWdq),
  ]
mnem_to_encodings[v(Packsswb)]  = [
  Ordinary([0x0F,0x63],ePqQd),
  Ordinary([0x66,0x0F,0x63],eVdqWdq),
  ]
mnem_to_encodings[v(Pcmpgtb)]   = [
  Ordinary([0x0F,0x64],ePqQd),
  Ordinary([0x66,0x0F,0x64],eVdqWdq),
  ]
mnem_to_encodings[v(Pcmpgtw)]   = [
  Ordinary([0x0F,0x65],ePqQd),
  Ordinary([0x66,0x0F,0x65],eVdqWdq),
  ]
mnem_to_encodings[v(Pcmpgtd)]   = [
  Ordinary([0x0F,0x66],ePqQd),
  Ordinary([0x66,0x0F,0x66],eVdqWdq),
  ]
mnem_to_encodings[v(Packuswb)]  = [
  Ordinary([0x0F,0x67],ePqQd),
  Ordinary([0x66,0x0F,0x67],eVdqWdq),
  ]
mnem_to_encodings[v(Punpckhbw)] = [
  Ordinary([0x0F,0x68],ePqQd),
  Ordinary([0x66,0x0F,0x68],eVdqWdq),
  ]
mnem_to_encodings[v(Punpckhwd)] = [
  Ordinary([0x0F,0x69],ePqQd),
  Ordinary([0x66,0x0F,0x69],eVdqWdq),
  ]
mnem_to_encodings[v(Punpckhdq)] = [
  Ordinary([0x0F,0x6A],ePqQd),
  Ordinary([0x66,0x0F,0x6A],eVdqWdq),
  ]
mnem_to_encodings[v(Packssdw)]  = [
  Ordinary([0x0F,0x6B],ePqQd),
  Ordinary([0x66,0x0F,0x6B],eVdqWdq),
  ]
mnem_to_encodings[v(Punpcklqdq)] = [Ordinary([0x66,0x0F,0x6C],eVdqWdq)]
mnem_to_encodings[v(Punpckhqdq)] = [Ordinary([0x66,0x0F,0x6D],eVdqWdq)]
mnem_to_encodings[v(Movd)] = [
  Ordinary([0x0F,0x6E],ePdEd_q),
  Ordinary([0x66,0x0F,0x6E],eVdqEd_q),
  Ordinary([0x0F,0x7E],eEd_qPd),
  Ordinary([0x66,0x0F,0x7E],eEd_qVdq),
  ]
mnem_to_encodings[v(Movq)]   = [
  Ordinary([0x0F,0x6F],ePqQq),
  Ordinary([0xF3,0x0F,0x7E],eVqWq),
  Ordinary([0x0F,0x7F],eQqPq),
  Ordinary([0x66,0x0F,0xD6],eVdqWdq),
  ]
mnem_to_encodings[v(Movdqu)] = [
  Ordinary([0xF3,0x0F,0x6F],eVdqWdq),
  Ordinary([0xF3,0x0F,0x7F],eWdqVdq),
  ]
mnem_to_encodings[v(Movdqa)] = [
  Ordinary([0x66,0x0F,0x6F],eVdqWdq),
  Ordinary([0x66,0x0F,0x7F],eWdqVdq),
  ]
mnem_to_encodings[v(Pshufw)] =  [Ordinary([0x0F,0x70],ePqQqIb)]
mnem_to_encodings[v(Pshufhw)] = [Ordinary([0xF3,0x0F,0x70],eVdqWdqIb)]
mnem_to_encodings[v(Pshufd)]  = [Ordinary([0x66,0x0F,0x70],eVdqWdqIb)]
mnem_to_encodings[v(Pshuflw)] = [Ordinary([0xF2,0x0F,0x70],eVdqWdqIb)]
mnem_to_encodings[v(Psrlw)]   = [
  ModRMGroup(2,[0x0F,0x71],eNqIb),
  ModRMGroup(2,[0x66,0x0F,0x71],eUdqIb),
  Ordinary([0x0F,0xD1],ePqQq),
  Ordinary([0x66,0x0F,0xD1],eVdqWdq),
  ]
mnem_to_encodings[v(Psraw)]   = [
  ModRMGroup(4,[0x0F,0x71],eNqIb),
  ModRMGroup(4,[0x66,0x0F,0x71],eUdqIb),
  Ordinary([0x0F,0xE1],ePqQq),
  Ordinary([0x66,0x0F,0xE1],eVdqWdq),
  ]
mnem_to_encodings[v(Psllw)]   = [
  ModRMGroup(6,[0x0F,0x71],eNqIb),
  ModRMGroup(6,[0x66,0x0F,0x71],eUdqIb),
  Ordinary([0x0F,0xF1],ePqQq),
  Ordinary([0x66,0x0F,0xF1],eVdqWdq),
  ]
mnem_to_encodings[v(Psrld)]   = [
  ModRMGroup(2,[0x0F,0x72],eNqIb),
  ModRMGroup(2,[0x66,0x0F,0x72],eUdqIb),
  Ordinary([0x0F,0xD2],ePqQq),
  Ordinary([0x66,0x0F,0xD2],eVdqWdq),
  ]
mnem_to_encodings[v(Psrad)]   = [
  ModRMGroup(4,[0x0F,0x72],eNqIb),
  ModRMGroup(4,[0x66,0x0F,0x72],eUdqIb),
  Ordinary([0x0F,0xE2],ePqQq),
  Ordinary([0x66,0x0F,0xE2],eVdqWdq),
  ]
mnem_to_encodings[v(Pslld)]   = [
  ModRMGroup(6,[0x0F,0x72],eNqIb),
  ModRMGroup(6,[0x66,0x0F,0x72],eUdqIb),
  Ordinary([0x0F,0xF2],ePqQq),
  Ordinary([0x66,0x0F,0xF2],eVdqWdq),
  ]
mnem_to_encodings[v(Psrlq)]   = [
  ModRMGroup(2,[0x0F,0x73],eNqIb),
  ModRMGroup(2,[0x66,0x0F,0x73],eUdqIb),
  Ordinary([0x0F,0xD3],ePqQq),
  Ordinary([0x66,0x0F,0xD3],eVdqWdq),  
  ]
mnem_to_encodings[v(Psrldq)]  = [ModRMGroup(3,[0x66,0x0F,0x73],eUdqIb)]
mnem_to_encodings[v(Psllq)]   = [
  ModRMGroup(6,[0x0F,0x73],eNqIb),
  ModRMGroup(6,[0x66,0x0F,0x73],eUdqIb),
  Ordinary([0x0F,0xF3],ePqQq),
  Ordinary([0x66,0x0F,0xF3],eVdqWdq),
  ]
mnem_to_encodings[v(Pslldq)]  = [ModRMGroup(7,[0x66,0x0F,0x73],eUdqIb)]
mnem_to_encodings[v(Pcmpeqb)] = [
  Ordinary([0x0F,0x74],ePqQq),
  Ordinary([0x66,0x0F,0x74],eVdqWdq),
  ]
mnem_to_encodings[v(Pcmpeqw)] = [
  Ordinary([0x0F,0x75],ePqQq),
  Ordinary([0x66,0x0F,0x75],eVdqWdq),
  ]
mnem_to_encodings[v(Pcmpeqd)] = [
  Ordinary([0x0F,0x76],ePqQq),
  Ordinary([0x66,0x0F,0x76],eVdqWdq),
  ]
mnem_to_encodings[v(Emms)]    = [Ordinary([0x0F,0x77],eNone)]
mnem_to_encodings[v(Vmread)]  = [Ordinary([0x0F,0x78],eEdGd)]
mnem_to_encodings[v(Vmwrite)] = [Ordinary([0x0F,0x79],eEdGd)]
mnem_to_encodings[v(Haddpd)]  = [Ordinary([0x66,0x0F,0x7C],eVpdWpd)]
mnem_to_encodings[v(Haddps)]  = [Ordinary([0xF2,0x0F,0x7C],eVpsWps)]
mnem_to_encodings[v(Hsubpd)]  = [Ordinary([0x66,0x0F,0x7D],eVpdWpd)]
mnem_to_encodings[v(Hsubps)]  = [Ordinary([0xF2,0x0F,0x7D],eVpsWps)]
#* TODO: JCC FROM 0x180-0x190 *)
mnem_to_encodings[v(Seto)]     = [ModRMGroup(0,[0x0F,0x90],eEb)]
mnem_to_encodings[v(Setno)]    = [ModRMGroup(0,[0x0F,0x91],eEb)]
mnem_to_encodings[v(Setb)]     = [ModRMGroup(0,[0x0F,0x92],eEb)]
mnem_to_encodings[v(Setae)]    = [ModRMGroup(0,[0x0F,0x93],eEb)]
mnem_to_encodings[v(Setz)]     = [ModRMGroup(0,[0x0F,0x94],eEb)]
mnem_to_encodings[v(Setnz)]    = [ModRMGroup(0,[0x0F,0x95],eEb)]
mnem_to_encodings[v(Setbe)]    = [ModRMGroup(0,[0x0F,0x96],eEb)]
mnem_to_encodings[v(Seta)]     = [ModRMGroup(0,[0x0F,0x97],eEb)]
mnem_to_encodings[v(Sets)]     = [ModRMGroup(0,[0x0F,0x98],eEb)]
mnem_to_encodings[v(Setns)]    = [ModRMGroup(0,[0x0F,0x99],eEb)]
mnem_to_encodings[v(Setp)]     = [ModRMGroup(0,[0x0F,0x9A],eEb)]
mnem_to_encodings[v(Setnp)]    = [ModRMGroup(0,[0x0F,0x9B],eEb)]
mnem_to_encodings[v(Setl)]     = [ModRMGroup(0,[0x0F,0x9C],eEb)]
mnem_to_encodings[v(Setge)]    = [ModRMGroup(0,[0x0F,0x9D],eEb)]
mnem_to_encodings[v(Setle)]    = [ModRMGroup(0,[0x0F,0x9E],eEb)]
mnem_to_encodings[v(Setg)]     = [ModRMGroup(0,[0x0F,0x9F],eEb)]
mnem_to_encodings[v(Cpuid)]    = [Ordinary([0x0F,0xA2],eNone)]
mnem_to_encodings[v(Bt)]       = [
  Ordinary([0x0F,0xA3],eEvGv),
  ModRMGroup(4,[0x0F,0xBA],eEvIb),
  ]
mnem_to_encodings[v(Shld)]     = [
  Ordinary([0x0F,0xA4],eEvGvIb),
  Ordinary([0x0F,0xA5],eEvGvCL),
  ]
mnem_to_encodings[v(Rsm)]      = [Ordinary([0x0F,0xAA],eNone)]
mnem_to_encodings[v(Bts)]      = [
  Ordinary([0x0F,0xAB],eEvGv),
  ModRMGroup(5,[0x0F,0xBA],eEvIb),
  ]
mnem_to_encodings[v(Shrd)]     = [
  Ordinary([0x0F,0xAC],eEvGvIb),
  Ordinary([0x0F,0xAD],eEvGvCL),
]
mnem_to_encodings[v(Fxsave)]   = [ModRMGroup(0,[0x0F,0xAE],eSimdState)]
mnem_to_encodings[v(Fxrstor)]  = [ModRMGroup(1,[0x0F,0xAE],eSimdState)]
mnem_to_encodings[v(Ldmxcsr)]  = [ModRMGroup(2,[0x0F,0xAE],eMd)]
mnem_to_encodings[v(Stmxcsr)]  = [ModRMGroup(3,[0x0F,0xAE],eMd)]
mnem_to_encodings[v(Clflush)]  = [ModRMGroup(7,[0x0F,0xAE],eMb)]
mnem_to_encodings[v(Lfence)]   = [Ordinary([0x0F,0xAE,0xE8],eNone)]
mnem_to_encodings[v(Mfence)]   = [Ordinary([0x0F,0xAE,0xF0],eNone)]
mnem_to_encodings[v(Sfence)]   = [Ordinary([0x0F,0xAE,0xF8],eNone)]
mnem_to_encodings[v(Cmpxchg)]  = [
  Ordinary([0x0F,0xB0],eEbGb),
  Ordinary([0x0F,0xB1],eEvGv),
  ]
mnem_to_encodings[v(Lss)]      = [Ordinary([0x0F,0xB2],eGvMp)]
mnem_to_encodings[v(Btr)]      = [
  Ordinary([0x0F,0xB3],eEvGv),
  ModRMGroup(6,[0x0F,0xBA],eEvIb),
  ]
mnem_to_encodings[v(Lfs)]      = [Ordinary([0x0F,0xB4],eGvMp)]
mnem_to_encodings[v(Lgs)]      = [Ordinary([0x0F,0xB5],eGvMp)]
mnem_to_encodings[v(Movzx)]    = [
  Ordinary([0x0F,0xB6],eGvEb),
  Ordinary([0x0F,0xB7],eGvEw),
  ]
mnem_to_encodings[v(Popcnt)]   = [Ordinary([0xF3,0x0F,0xB8],eGvEv)]
mnem_to_encodings[v(Btc)]      = [
  ModRMGroup(7,[0x0F,0xBA],eEvIb),
  Ordinary([0x0F,0xBB],eEvGv),
  ]
mnem_to_encodings[v(Bsf)]      = [Ordinary([0x0F,0xBC],eGvEv)]
mnem_to_encodings[v(Bsr)]      = [Ordinary([0x0F,0xBD],eGvEv)]
mnem_to_encodings[v(Movsx)]    = [
  Ordinary([0x0F,0xBE],eGvEb),
  Ordinary([0x0F,0xBF],eGvEw),
  ]
mnem_to_encodings[v(Xadd)]     = [
  Ordinary([0x0F,0xC0],eEbGb),  
  Ordinary([0x0F,0xC1],eEvGv),
  ]
mnem_to_encodings[v(Cmpps)]     = [Ordinary([0x0F,0xC2],eVpsWpsIb)]
mnem_to_encodings[v(Cmpss)]     = [Ordinary([0xF3,0x0F,0xC2],eVssWssIb)]
mnem_to_encodings[v(Cmppd)]     = [Ordinary([0x66,0x0F,0xC2],eVpdWpdIb)]
mnem_to_encodings[v(Movnti)]    = [Ordinary([0x0F,0xC3],eMd_qGd_q)]
mnem_to_encodings[v(Pinsrw)]    = [
  Ordinary([0x0F,0xC4],ePqEwIb),
  Ordinary([0x66,0x0F,0xC4],eVdqEwIb),
  ]
mnem_to_encodings[v(Pextrw)]    = [
  Ordinary([0x0F,0xC5],eGdNqIb),
  Ordinary([0x66,0x0F,0xC5],eGdUdqIb),
  Ordinary([0x66,0x0F,0x3A,0x15],eRd_MwVdqIb),
  ]
mnem_to_encodings[v(Shufps)]    = [Ordinary([0x0F,0xC6],eVpsWpsIb)]
mnem_to_encodings[v(Shufpd)]    = [Ordinary([0x66,0x0F,0xC6],eVpsWpsIb)]
mnem_to_encodings[v(Cmpxchg8b)] = [ModRMGroup(1,[0x0F,0xC7],eMq)]
mnem_to_encodings[v(Vmptrld)]   = [ModRMGroup(6,[0x0F,0xC7],eMq)]
mnem_to_encodings[v(Vmxon)]     = [ModRMGroup(6,[0xF3,0x0F,0xC7],eMq)]
mnem_to_encodings[v(Vmclear)]   = [ModRMGroup(6,[0x66,0x0F,0xC7],eMq)]
mnem_to_encodings[v(Vmptrst)]   = [ModRMGroup(7,[0x0F,0xC7],eMq)]
mnem_to_encodings[v(Bswap)]    = [
  Ordinary([0x0F,0xC8],eeAX),
  Ordinary([0x0F,0xC9],eeCX),
  Ordinary([0x0F,0xCA],eeDX),
  Ordinary([0x0F,0xCB],eeBX),
  Ordinary([0x0F,0xCC],eeSP),
  Ordinary([0x0F,0xCD],eeBP),
  Ordinary([0x0F,0xCE],eeSI),
  Ordinary([0x0F,0xCF],eeDI),
  ]
mnem_to_encodings[v(Addsubpd)] = [Ordinary([0x66,0x0F,0xD0],eVpdWpd)]
mnem_to_encodings[v(Addsubps)] = [Ordinary([0xF2,0x0F,0xD0],eVpsWps)] 
mnem_to_encodings[v(Paddq)]  = [
  Ordinary([0x0F,0xD4],ePqQq),
  Ordinary([0x66,0x0F,0xD4],eVdqWdq),
  ]
mnem_to_encodings[v(Pmullw)]  = [
  Ordinary([0x0F,0xD5],ePqQq),
  Ordinary([0x66,0x0F,0xD5],eVdqWdq),
  ]
mnem_to_encodings[v(Movq2dq)]  = [Ordinary([0xF3,0x0F,0xD6],eVdqNq)]
mnem_to_encodings[v(Movdq2q)]  = [Ordinary([0xF2,0x0F,0xD6],ePqUq)]
mnem_to_encodings[v(Pmovmskb)] = [
  Ordinary([0x0F,0xD7],eGdNq),
  Ordinary([0x66,0x0F,0xD7],eGdUdq),
  ]
mnem_to_encodings[v(Psubusb)] = [
  Ordinary([0x0F,0xD8],ePqQq),
  Ordinary([0x66,0x0F,0xD8],eVdqWdq),
  ]
mnem_to_encodings[v(Psubusw)] = [
  Ordinary([0x0F,0xD9],ePqQq),
  Ordinary([0x66,0x0F,0xD9],eVdqWdq),
  ]
mnem_to_encodings[v(Pminub)]  = [
  Ordinary([0x0F,0xDA],ePqQq),
  Ordinary([0x66,0x0F,0xDA],eVdqWdq),
  ]
mnem_to_encodings[v(Pand)]    = [
  Ordinary([0x0F,0xDB],ePqQq),
  Ordinary([0x66,0x0F,0xDB],eVdqWdq),
  ]
mnem_to_encodings[v(Paddusb)] = [
  Ordinary([0x0F,0xDC],ePqQq),
  Ordinary([0x66,0x0F,0xDC],eVdqWdq),
  ]
mnem_to_encodings[v(Paddusw)] = [
  Ordinary([0x0F,0xDD],ePqQq),
  Ordinary([0x66,0x0F,0xDD],eVdqWdq),
  ]
mnem_to_encodings[v(Pmaxub)]  = [
  Ordinary([0x0F,0xDE],ePqQq),
  Ordinary([0x66,0x0F,0xDE],eVdqWdq),
  ]
mnem_to_encodings[v(Pandn)]   = [
  Ordinary([0x0F,0xDF],ePqQq),
  Ordinary([0x66,0x0F,0xDF],eVdqWdq),
  ]
mnem_to_encodings[v(Pavgb)]   = [
  Ordinary([0x0F,0xE0],ePqQq),
  Ordinary([0x66,0x0F,0xE0],eVdqWdq),
  ]
mnem_to_encodings[v(Pavgw)]   = [
  Ordinary([0x0F,0xE3],ePqQq),
  Ordinary([0x66,0x0F,0xE3],eVdqWdq),
  ]
mnem_to_encodings[v(Pmulhuw)] = [
  Ordinary([0x0F,0xE4],ePqQq),
  Ordinary([0x66,0x0F,0xE4],eVdqWdq),
  ]
mnem_to_encodings[v(Pmulhw)]  = [
  Ordinary([0x0F,0xE5],ePqQq),
  Ordinary([0x66,0x0F,0xE5],eVdqWdq),
  ]
mnem_to_encodings[v(Cvtdq2pd)]  = [Ordinary([0xF3,0x0F,0xE6],eVpdWdq)]
mnem_to_encodings[v(Cvttpd2dq)] = [Ordinary([0x66,0x0F,0xE6],eVdqWpd)]
mnem_to_encodings[v(Cvtpd2dq)]  = [Ordinary([0xF2,0x0F,0xE6],eVdqWpd)]
mnem_to_encodings[v(Movntq)]    = [Ordinary([0x0F,0xE7],eMqPq)]
mnem_to_encodings[v(Movntdq)]   = [Ordinary([0x66,0x0F,0xE7],eMdqVdq)]
mnem_to_encodings[v(Psubsb)]    = [
  Ordinary([0x0F,0xE8],ePqQq),
  Ordinary([0x66,0x0F,0xE8],eVdqWdq),
  ]
mnem_to_encodings[v(Psubsw)]    = [
  Ordinary([0x0F,0xE9],ePqQq),
  Ordinary([0x66,0x0F,0xE9],eVdqWdq),
  ]
mnem_to_encodings[v(Pminsw)]    = [
  Ordinary([0x0F,0xEA],ePqQq),
  Ordinary([0x66,0x0F,0xEA],eVdqWdq),
  ]
mnem_to_encodings[v(Por)]       = [
  Ordinary([0x0F,0xEB],ePqQq),
  Ordinary([0x66,0x0F,0xEB],eVdqWdq),
  ]
mnem_to_encodings[v(Paddsb)]    = [
  Ordinary([0x0F,0xEC],ePqQq),
  Ordinary([0x66,0x0F,0xEC],eVdqWdq),
  ]
mnem_to_encodings[v(Paddsw)]    = [
  Ordinary([0x0F,0xED],ePqQq),
  Ordinary([0x66,0x0F,0xED],eVdqWdq),
  ]
mnem_to_encodings[v(Pmaxsw)]    = [
  Ordinary([0x0F,0xEE],ePqQq),
  Ordinary([0x66,0x0F,0xEE],eVdqWdq),
  ]
mnem_to_encodings[v(Pxor)]      = [
  Ordinary([0x0F,0xEF],ePqQq),
  Ordinary([0x66,0x0F,0xEF],eVdqWdq),
  ]
mnem_to_encodings[v(Lddqu)]     = [Ordinary([0xF2,0x0F,0xF0],eVdqMdq)]
mnem_to_encodings[v(Pmuludq)]   = [
  Ordinary([0x0F,0xF4],ePqQq),
  Ordinary([0x66,0x0F,0xF4],eVdqWdq),
  ]
mnem_to_encodings[v(Pmaddwd)]   = [
  Ordinary([0x0F,0xF5],ePqQq),
  Ordinary([0x66,0x0F,0xF5],eVdqWdq),
  ]
mnem_to_encodings[v(Psadbw)]    = [
  Ordinary([0x0F,0xF6],ePqQq),
  Ordinary([0x66,0x0F,0xF6],eVdqWdq),
  ]
mnem_to_encodings[v(Maskmovq)]    = [Ordinary([0x0F,0xF7],ePqNq)]
mnem_to_encodings[v(Maskmovdqu)]  = [Ordinary([0x66,0x0F,0xF7],eVdqUdq)]
mnem_to_encodings[v(Psubb)]     = [
  Ordinary([0x0F,0xF8],ePqQq),
  Ordinary([0x66,0x0F,0xF8],eVdqWdq),
  ]
mnem_to_encodings[v(Psubw)]     = [
  Ordinary([0x0F,0xF9],ePqQq),
  Ordinary([0x66,0x0F,0xF9],eVdqWdq),
  ]
mnem_to_encodings[v(Psubd)]     = [
  Ordinary([0x0F,0xFA],ePqQq),
  Ordinary([0x66,0x0F,0xFA],eVdqWdq),
  ]
mnem_to_encodings[v(Psubq)]     = [
  Ordinary([0x0F,0xFB],ePqQq),
  Ordinary([0x66,0x0F,0xFB],eVdqWdq),
  ]
mnem_to_encodings[v(Paddb)]     = [
  Ordinary([0x0F,0xFC],ePqQq),
  Ordinary([0x66,0x0F,0xFC],eVdqWdq),
  ]
mnem_to_encodings[v(Paddw)]     = [
  Ordinary([0x0F,0xFD],ePqQq),
  Ordinary([0x66,0x0F,0xFD],eVdqWdq),
  ]
mnem_to_encodings[v(Paddd)]     = [
  Ordinary([0x0F,0xFE],ePqQq),
  Ordinary([0x66,0x0F,0xFE],eVdqWdq),
  ]
mnem_to_encodings[v(Pshufb)]    = [
  Ordinary([0x0F,0x38,0x00],ePqQq),
  Ordinary([0x66,0x0F,0x38,0x00],eVdqWdq),
  ]
mnem_to_encodings[v(Phaddw)]    = [
  Ordinary([0x0F,0x38,0x01],ePqQq),
  Ordinary([0x66,0x0F,0x38,0x01],eVdqWdq),
  ]
mnem_to_encodings[v(Phaddd)]    = [
  Ordinary([0x0F,0x38,0x02],ePqQq),
  Ordinary([0x66,0x0F,0x38,0x02],eVdqWdq),
  ]
mnem_to_encodings[v(Phaddsw)]   = [
  Ordinary([0x0F,0x38,0x03],ePqQq),
  Ordinary([0x66,0x0F,0x38,0x03],eVdqWdq),
  ]
mnem_to_encodings[v(Pmaddubsw)] = [
  Ordinary([0x0F,0x38,0x04],ePqQq),
  Ordinary([0x66,0x0F,0x38,0x04],eVdqWdq),
  ]
mnem_to_encodings[v(Phsubw)]    = [
  Ordinary([0x0F,0x38,0x05],ePqQq),
  Ordinary([0x66,0x0F,0x38,0x05],eVdqWdq),
  ]
mnem_to_encodings[v(Phsubd)]    = [
  Ordinary([0x0F,0x38,0x06],ePqQq),
  Ordinary([0x66,0x0F,0x38,0x06],eVdqWdq),
  ]
mnem_to_encodings[v(Phsubsw)]   = [
  Ordinary([0x0F,0x38,0x07],ePqQq),
  Ordinary([0x66,0x0F,0x38,0x07],eVdqWdq),
  ]
mnem_to_encodings[v(Psignb)]    = [
  Ordinary([0x0F,0x38,0x08],ePqQq),
  Ordinary([0x66,0x0F,0x38,0x08],eVdqWdq),
  ]
mnem_to_encodings[v(Psignw)]    = [
  Ordinary([0x0F,0x38,0x09],ePqQq),
  Ordinary([0x66,0x0F,0x38,0x09],eVdqWdq),
  ]
mnem_to_encodings[v(Psignd)]    = [
  Ordinary([0x0F,0x38,0x0A],ePqQq),
  Ordinary([0x66,0x0F,0x38,0x0A],eVdqWdq),
  ]
mnem_to_encodings[v(Pmulhrsw)]  = [
  Ordinary([0x0F,0x38,0x0B],ePqQq),
  Ordinary([0x66,0x0F,0x38,0x0B],eVdqWdq),
  ]
mnem_to_encodings[v(Pblendvb)]  = [Ordinary([0x66,0x0F,0x38,0x10],eVdqWdq)]
mnem_to_encodings[v(Blendvps)]  = [Ordinary([0x66,0x0F,0x38,0x14],eVdqWdq)]
mnem_to_encodings[v(Blendvpd)]  = [Ordinary([0x66,0x0F,0x38,0x15],eVdqWdq)]
mnem_to_encodings[v(Ptest)]     = [Ordinary([0x66,0x0F,0x38,0x17],eVdqWdq)]
mnem_to_encodings[v(Pabsb)]     = [
  Ordinary([0x0F,0x38,0x1C],ePqQq),
  Ordinary([0x66,0x0F,0x38,0x1C],eVdqWdq),
  ]
mnem_to_encodings[v(Pabsw)]     = [
  Ordinary([0x0F,0x38,0x1D],ePqQq),
  Ordinary([0x66,0x0F,0x38,0x1D],eVdqWdq),
  ]
mnem_to_encodings[v(Pabsd)]     = [
  Ordinary([0x0F,0x38,0x1E],ePqQq),
  Ordinary([0x66,0x0F,0x38,0x1E],eVdqWdq),
  ]
mnem_to_encodings[v(Pmovsxbw)]    = [Ordinary([0x66,0x0F,0x38,0x20],eVdqUdq_Mq)]
mnem_to_encodings[v(Pmovsxbd)]    = [Ordinary([0x66,0x0F,0x38,0x21],eVdqUdq_Md)]
mnem_to_encodings[v(Pmovsxbq)]    = [Ordinary([0x66,0x0F,0x38,0x22],eVdqUdq_Mw)]
mnem_to_encodings[v(Pmovsxwd)]    = [Ordinary([0x66,0x0F,0x38,0x23],eVdqUdq_Mq)]
mnem_to_encodings[v(Pmovsxwq)]    = [Ordinary([0x66,0x0F,0x38,0x24],eVdqUdq_Md)]
mnem_to_encodings[v(Pmovsxdq)]    = [Ordinary([0x66,0x0F,0x38,0x25],eVdqUdq_Mq)]
mnem_to_encodings[v(Pmuldq)]      = [Ordinary([0x66,0x0F,0x38,0x28],eVdqWdq)]
mnem_to_encodings[v(Pcmpeqq)]     = [Ordinary([0x66,0x0F,0x38,0x29],eVdqWdq)]
mnem_to_encodings[v(Movntdqa)]    = [Ordinary([0x66,0x0F,0x38,0x2A],eVdqMdq)]
mnem_to_encodings[v(Packusdw)]    = [Ordinary([0x66,0x0F,0x38,0x2B],eVdqWdq)]
mnem_to_encodings[v(Pmovzxbw)]    = [Ordinary([0x66,0x0F,0x38,0x30],eVdqUdq_Mq)]
mnem_to_encodings[v(Pmovzxbd)]    = [Ordinary([0x66,0x0F,0x38,0x31],eVdqUdq_Md)]
mnem_to_encodings[v(Pmovzxbq)]    = [Ordinary([0x66,0x0F,0x38,0x32],eVdqUdq_Mw)]
mnem_to_encodings[v(Pmovzxwd)]    = [Ordinary([0x66,0x0F,0x38,0x33],eVdqUdq_Mq)]
mnem_to_encodings[v(Pmovzxwq)]    = [Ordinary([0x66,0x0F,0x38,0x34],eVdqUdq_Md)]
mnem_to_encodings[v(Pmovzxdq)]    = [Ordinary([0x66,0x0F,0x38,0x35],eVdqUdq_Mq)]
mnem_to_encodings[v(Pcmpgtq)]     = [Ordinary([0x66,0x0F,0x38,0x37],eVdqWdq)]
mnem_to_encodings[v(Pminsb)]      = [Ordinary([0x66,0x0F,0x38,0x38],eVdqWdq)]
mnem_to_encodings[v(Pminsd)]      = [Ordinary([0x66,0x0F,0x38,0x39],eVdqWdq)]
mnem_to_encodings[v(Pminuw)]      = [Ordinary([0x66,0x0F,0x38,0x3A],eVdqWdq)]
mnem_to_encodings[v(Pminud)]      = [Ordinary([0x66,0x0F,0x38,0x3B],eVdqWdq)]
mnem_to_encodings[v(Pmaxsb)]      = [Ordinary([0x66,0x0F,0x38,0x3C],eVdqWdq)]
mnem_to_encodings[v(Pmaxsd)]      = [Ordinary([0x66,0x0F,0x38,0x3D],eVdqWdq)]
mnem_to_encodings[v(Pmaxuw)]      = [Ordinary([0x66,0x0F,0x38,0x3E],eVdqWdq)]
mnem_to_encodings[v(Pmaxud)]      = [Ordinary([0x66,0x0F,0x38,0x3F],eVdqWdq)]
mnem_to_encodings[v(Pmulld)]      = [Ordinary([0x66,0x0F,0x38,0x40],eVdqWdq)]
mnem_to_encodings[v(Phminposuw)]  = [Ordinary([0x66,0x0F,0x38,0x41],eVdqWdq)]
mnem_to_encodings[v(Crc32)]    = [
  Ordinary([0x0F,0x38,0xF0],eGdEb),
  Ordinary([0x0F,0x38,0xF1],eGdEv),
  ]
mnem_to_encodings[v(Roundps)] = [Ordinary([0x66,0x0F,0x3A,0x08],eVdqWdqIb)]
mnem_to_encodings[v(Roundpd)] = [Ordinary([0x66,0x0F,0x3A,0x09],eVdqWdqIb)]
mnem_to_encodings[v(Roundss)] = [Ordinary([0x66,0x0F,0x3A,0x0A],eVssWssIb)]
mnem_to_encodings[v(Roundsd)] = [Ordinary([0x66,0x0F,0x3A,0x0B],eVsdWsdIb)]
mnem_to_encodings[v(Blendps)] = [Ordinary([0x66,0x0F,0x3A,0x0C],eVdqWdqIb)]
mnem_to_encodings[v(Blendpd)] = [Ordinary([0x66,0x0F,0x3A,0x0D],eVdqWdqIb)]
mnem_to_encodings[v(Pblendw)] = [Ordinary([0x66,0x0F,0x3A,0x0E],eVdqWdqIb)]
mnem_to_encodings[v(Palignr)] = [
  Ordinary([0x0F,0x3A,0x0F],ePqQqIb),
  Ordinary([0x66,0x0F,0x3A,0x0F],eVdqWdqIb),
  ]
mnem_to_encodings[v(Pextrb)]    = [Ordinary([0x66,0x0F,0x3A,0x14],eRd_MbVdqIb)]
mnem_to_encodings[v(Pextrd)]    = [Ordinary([0x66,0x0F,0x3A,0x16],eEdVdqIb)]
mnem_to_encodings[v(Extractps)] = [Ordinary([0x66,0x0F,0x3A,0x17],eEdVdqIb)]
mnem_to_encodings[v(Pinsrb)]    = [Ordinary([0x66,0x0F,0x3A,0x20],eVdqEdIb)]
mnem_to_encodings[v(Insertps)]  = [Ordinary([0x66,0x0F,0x3A,0x21],eVdqUdq_MdIb)]
mnem_to_encodings[v(Pinsrd)]    = [Ordinary([0x66,0x0F,0x3A,0x22],eVdqEdIb)]
mnem_to_encodings[v(Dpps)]      = [Ordinary([0x66,0x0F,0x3A,0x40],eVdqWdqIb)]
mnem_to_encodings[v(Dppd)]      = [Ordinary([0x66,0x0F,0x3A,0x41],eVdqWdqIb)]
mnem_to_encodings[v(Mpsadbw)]   = [Ordinary([0x66,0x0F,0x3A,0x42],eVdqWdqIb)]
mnem_to_encodings[v(Pcmpestrm)] = [Ordinary([0x66,0x0F,0x3A,0x60],eVdqWdqIb)]
mnem_to_encodings[v(Pcmpestri)] = [Ordinary([0x66,0x0F,0x3A,0x61],eVdqWdqIb)]
mnem_to_encodings[v(Pcmpistrm)] = [Ordinary([0x66,0x0F,0x3A,0x62],eVdqWdqIb)]
mnem_to_encodings[v(Pcmpistri)] = [Ordinary([0x66,0x0F,0x3A,0x63],eVdqWdqIb)]

