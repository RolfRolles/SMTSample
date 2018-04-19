import X86Lex
import X86
import X86MetaData as XM
import X86ModRM
import X86TypeChecker
import X86EncodeTable
import itertools
import ply.yacc as yacc

class X86UnknownSizeImmediate(X86.Id):
	pass

class X86UnknownSizeMem16(X86.Mem16):
	pass

class X86UnknownSizeMem32(X86.Mem32):
	pass

memsizes = [XM.Mb,XM.Mw,XM.Md,XM.Mf,XM.Mq,XM.Mt,XM.Mdq]

class X86Pseudo(object):
	def __init__(self,pf=None,mnem=None,op1=None,op2=None,op3=None):
		self.pf,self.mnem,self.op1,self.op2,self.op3 = pf,mnem,op1,op2,op3

def validate_scale(num):
	if not ((num & (num-1) == 0) and (num != 0) and (num <= 8)):
		raise ValueError("Decoding memory expression:  bad scale factor %d" % num)
	return 3 if num==8 else 2 if num==4 else 1 if num==2 else 0

def validate_meminner(mi,unk=False):
	me = mi
	if isinstance(mi,X86.Mem16):
		m = X86ModRM.ModRM16()
		try:
			m.EncodeFromParts(mi.BaseReg,mi.IndexReg,mi.Disp)
			br,ir,disp,_ = m.Interpret()
			if unk:
				me = X86UnknownSizeMem16(XM.CS,XM.Mb,br,ir,disp)
			else:
				me = X86.Mem16(XM.CS,XM.Mb,br,ir,disp)
		except IndexError, e:
			raise ValueError("%s:  invalid ModRM/16 expression" % mi)
	elif isinstance(mi,X86.Mem32):
		m = X86ModRM.ModRM32()
		m.EncodeFromParts(mi.BaseReg,mi.IndexReg,mi.ScaleFac,mi.Disp)
		br,ir,sf,disp,_ = m.Interpret()
		if unk:
			me = X86UnknownSizeMem32(XM.CS,XM.Mb,br,ir,sf,disp)
		else:
			me = X86.Mem32(XM.CS,XM.Mb,br,ir,sf,disp)
	else:
		raise ValueError("WTF is this memory expression %s" % mi)
	me.Seg = me.DefaultSeg()
	return me

class X86Yacc(object):
	start = 'instr'

	def p_op_gb(self,p):
		'op : Gb'
		p[0] = X86.Gb(p[1])

	def p_op_gw(self,p):
		'op : Gw'
		p[0] = X86.Gw(p[1])

	def p_op_gd(self,p):
		'op : Gd'
		p[0] = X86.Gd(p[1])

	def p_op_seg(self,p):
		'op : Seg'
		p[0] = X86.SegReg(p[1])

	def p_op_cnt(self,p):
		'op : CNT'
		p[0] = X86.ControlReg(p[1])

	def p_op_dbg(self,p):
		'op : DBG'
		p[0] = X86.DebugReg(p[1])

	def p_op_fpu(self,p):
		'op : FPU'
		p[0] = X86.FPUReg(p[1])

	def p_op_mmx(self,p):
		'op : MMX'
		p[0] = X86.MMXReg(p[1])

	def p_op_xmm(self,p):
		'op : XMM'
		p[0] = X86.XMMReg(p[1])

	def p_meminner_Gd_plus_Gd_times_num_plus_num(self,p):
		'meminner : Gd PLUS Gd TIMES NUM PLUS NUM'
		p[0] = X86.Mem32(XM.CS,XM.Mb,p[1],p[3],validate_scale(p[5]),p[7])

	def p_meminner_Gd_plus_Gd_plus_num(self,p):
		'meminner : Gd PLUS Gd PLUS NUM'
		p[0] = X86.Mem32(XM.CS,XM.Mb,p[1],p[3],0,p[5])

	def p_meminner_Gd_plus_Gd_times_num(self,p):
		'meminner : Gd PLUS Gd TIMES NUM'
		p[0] = X86.Mem32(XM.CS,XM.Mb,p[1],p[3],validate_scale(p[5]),None)

	def p_meminner_Gd_times_num_plus_num(self,p):
		'meminner : Gd TIMES NUM PLUS NUM'
		p[0] = X86.Mem32(XM.CS,XM.Mb,None,p[1],validate_scale(p[3]),p[5])

	def p_meminner_Gd_times_num(self,p):
		'meminner : Gd TIMES NUM'
		p[0] = X86.Mem32(XM.CS,XM.Mb,None,p[1],validate_scale(p[3]),None)

	def p_meminner_Gd_plus_Gd(self,p):
		'meminner : Gd PLUS Gd'
		p[0] = X86.Mem32(XM.CS,XM.Mb,p[1],p[3],0,None)

	def p_meminner_Gd_plus_num(self,p):
		'meminner : Gd PLUS NUM'
		p[0] = X86.Mem32(XM.CS,XM.Mb,p[1],None,0,p[3])

	def p_meminner_Gd(self,p):
		'meminner : Gd'
		p[0] = X86.Mem32(XM.CS,XM.Mb,p[1],None,0,None)

	def p_meminner_num(self,p):
		'meminner : NUM'
		p[0] = X86.Mem32(XM.CS,XM.Mb,None,None,0,p[1])

	def p_meminner_Gw_plus_Gw_plus_num(self,p):
		'meminner : Gw PLUS Gw PLUS NUM'
		p[0] = X86.Mem16(XM.CS,XM.Mb,p[1],p[3],p[5])

	def p_meminner_Gw_plus_Gw(self,p):
		'meminner : Gw PLUS Gw'
		p[0] = X86.Mem16(XM.CS,XM.Mb,p[1],p[3],None)

	def p_meminner_Gw_plus_num(self,p):
		'meminner : Gw PLUS NUM'
		p[0] = X86.Mem16(XM.CS,XM.Mb,p[1],None,p[3])

	def p_meminner_Gw(self,p):
		'meminner : Gw'
		p[0] = X86.Mem16(XM.CS,XM.Mb,p[1],None,None)

	def p_memexpr_size_meminner(self,p):
		'memexpr : SIZE PTR LSQBR meminner RSQBR'
		mi = validate_meminner(p[4])
		mi.size = p[1]
		p[0] = mi
	
	def p_memexpr_size_seg_meminner(self,p):
		'memexpr : SIZE PTR Seg COLON LSQBR meminner RSQBR'
		mi = validate_meminner(p[6])
		mi.size = p[1]
		mi.Seg = p[3]
		p[0] = mi

	def p_memexpr_seg_meminner(self,p):
		'memexpr : Seg COLON LSQBR meminner RSQBR'
		mi = validate_meminner(p[4],True)
		mi.Seg = p[1]
		p[0] = mi

	def p_memexpr_meminner(self,p):
		'memexpr : LSQBR meminner RSQBR'
		mi = validate_meminner(p[2],True)
		p[0] = mi

	def p_op_memexpr(self,p):
		'op : memexpr'
		p[0] = p[1]

	def p_op_ap32(self,p):
		'op : NUM COLON NUM'
		p[0] = X86.AP32(p[1],p[3])

	def p_op_imm(self,p):
		'op : NUM'
		p[0] = X86UnknownSizeImmediate(p[1])

	def p_pfxlist_pfx(self,p):
		'pfxlist : PFX'
		p[0] = [p[1]]
	
	def p_pfxlist_pfxlist_pfx(self,p):
		'pfxlist : pfxlist PFX'
		p[1].append(p[2])
		p[0] = p[1]

	def p_pfxlist_pseudo3(self,p):
		'pseudo : pfxlist Mnem op COMMA op COMMA op'
		p[0] = X86Pseudo(p[1],p[2],p[3],p[5],p[7])

	def p_pfxlist_pseudo2(self,p):
		'pseudo : pfxlist Mnem op COMMA op'
		p[0] = X86Pseudo(p[1],p[2],p[3],p[5])

	def p_pfxlist_pseudo1(self,p):
		'pseudo : pfxlist Mnem op'
		p[0] = X86Pseudo(p[1],p[2],p[3])
	
	def p_pfxlist_pseudo(self,p):
		'pseudo : pfxlist Mnem'
		p[0] = X86Pseudo(p[1],p[2])

	def p_pseudo3(self,p):
		'pseudo : Mnem op COMMA op COMMA op'
		p[0] = X86Pseudo([],p[1],p[2],p[4],p[6])

	def p_pseudo2(self,p):
		'pseudo : Mnem op COMMA op'
		p[0] = X86Pseudo([],p[1],p[2],p[4])

	def p_pseudo1(self,p):
		'pseudo : Mnem op'
		p[0] = X86Pseudo([],p[1],p[2])
	
	def p_pseudo(self,p):
		'pseudo : Mnem'
		p[0] = X86Pseudo([],p[1])

	def p_instr_pseudo(self,p):
		'instr : pseudo'
		pseudo = p[1]
		def mk_op_list(op):
			if op is None: return [None]
			if isinstance(op,X86UnknownSizeImmediate):
				v = op.value
				l = [X86.Id(v)]
				if v <= 0xFF or (v <= 0x7F or v >= 0xFFFFFF80) or (v <= 0x7F or (v >= 0xFF80 and v <= 0xFFFF)):
					l.append(X86.Ib(v))
				if v <= 0xFFFF or (v <= 0x7F or v >= 0xFFFF8000) or (v <= 0x7F or (v >= 0xFF80 and v <= 0xFFFF)):
					l.append(X86.Iw(v))
				return l
			elif isinstance(op,X86UnknownSizeMem16):
				return map(lambda s: X86.Mem16(op.Seg,s,op.BaseReg,op.IndexReg,op.Disp),memsizes)
			elif isinstance(op,X86UnknownSizeMem32):
				return map(lambda s: X86.Mem32(op.Seg,s,op.BaseReg,op.IndexReg,op.ScaleFac,op.Disp),memsizes)
			else:
				return [op]
		g = itertools.product(*tuple(map(mk_op_list,[pseudo.op1,pseudo.op2,pseudo.op3])))
		tc = X86TypeChecker.X86TypeChecker()
		for t in g:
			i = X86.Instruction(pseudo.pf,pseudo.mnem,*t)
			for enc in X86EncodeTable.mnem_to_encodings[i.mnem.IntValue()]:
				# See if the encoding matches, i.e. if the operands type-check.
				val = tc.TypeCheckInstruction_opt(i,enc.ops)
				if val == None: 
					continue
				p[0] = i
				return
		raise ValueError("%s: bad instruction" % pseudo)
	
	def p_error(self,p):
		if not p:
			raise SyntaxError("at end of file")
		raise SyntaxError("at token %s" % p)

 	def Init(self,**kwargs):
		self.lexer = X86Lex.X86Lexer()
		self.tokens = self.lexer.tokens
		self.parser = yacc.yacc(module=self, **kwargs)
 	
 	def Parse(self,text):
 		return self.parser.parse(text,lexer=self.lexer.lexer)
 	
 	# Build the parser
	def __init__(self,**kwargs):                      
		self.Init(**kwargs)
