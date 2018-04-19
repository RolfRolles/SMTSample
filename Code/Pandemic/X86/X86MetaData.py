""" This file contains enumerations (in the style of :mod:`~.Enumerate`) for
common objects in X86:

* Prefixes: :class:`~.PF1Elt`
* Mnemonics: :class:`~.MnemElt`
* Register types:
* * 8-bit registers: :class:`~.R8Elt` 
* * 16-bit registers: :class:`~.R16Elt` 
* * 32-bit registers: :class:`~.R32Elt`
* * Segment registers: :class:`~.SegElt`
* * Control registers: :class:`~.CntElt`
* * Debug registers: :class:`~.DbgElt` 
* * FPU registers: :class:`~.FPUElt`
* * MMX registers: :class:`~.MMXElt`
* * XMM registers: :class:`~.XMMElt`
* Memory sizes: :class:`~.FlagElt`
* Flags: :class:`~.FlagElt`
"""

from Pandemic.Util.Enumerate import enum_lower, enum_specialstr, enum_upper

pf1e,     PF1List = enum_lower("PF1",["REP","REPNE","LOCK"])
r8e,       R8List = enum_lower("R8", ['Al','Cl','Dl','Bl','Ah','Ch','Dh','Bh'])
r16e,     R16List = enum_lower("R16",['Ax','Cx','Dx','Bx','Sp','Bp','Si','Di'])
r32e,     R32List = enum_lower("R32",['Eax','Ecx','Edx','Ebx','Esp','Ebp','Esi','Edi'])
sege,     SegList = enum_lower("Seg",['ES','CS','SS','DS','FS','GS'])
cnte,     CntList = enum_lower("Cnt",['CR0','CR1','CR2','CR3','CR4','CR5','CR6','CR7'])
dbge,     DbgList = enum_lower("Dbg",['DR0','DR1','DR2','DR3','DR4','DR5','DR6','DR7'])
fpue,     FPUList = enum_lower("FPU",['ST0','ST1','ST2','ST3','ST4','ST5','ST6','ST7'])
mmxe,     MMXList = enum_lower("MMX",['MM0','MM1','MM2','MM3','MM4','MM5','MM6','MM7'])
xmme,     XMMList = enum_lower("XMM",['XMM0','XMM1','XMM2','XMM3','XMM4','XMM5','XMM6','XMM7'])
flage,   FlagList = enum_upper("Flag",['OF','DF','SF','ZF','AF','PF','CF'])
mse,       MSList = enum_specialstr("MemSize",[('Mb',"byte"),('Mw',"word"),('Md',"dword"),('Mf',"fword"),('Mq',"qword"),('Mt',"tword"),('Mdq',"dqword")])

# We write it this way so Sphinx can pick up on the types.
PF1Elt  = pf1e  #: `type` object for group 1 prefix enumeration elements
R8Elt   = r8e   #: `type` object for 8-bit register enumeration elements
R16Elt  = r16e  #: `type` object for 16-bit register enumeration elements
R32Elt  = r32e  #: `type` object for 32-bit register enumeration elements
SegElt  = sege  #: `type` object for segment register enumeration elements
CntElt  = cnte  #: `type` object for control register enumeration elements
DbgElt  = dbge  #: `type` object for debug register enumeration elements
FPUElt  = fpue  #: `type` object for FPU register enumeration elements
MMXElt  = mmxe  #: `type` object for MMX register enumeration elements
XMMElt  = xmme  #: `type` object for XMM register enumeration elements
FlagElt = flage #: `type` object for flag register enumeration elements
MSElt   = mse   #: `type` object for memory access size enumeration elements

REP,REPNE,LOCK                          = PF1List
Al, Cl, Dl, Bl, Ah, Ch, Dh, Bh          = R8List  
Ax, Cx, Dx, Bx, Sp, Bp, Si, Di          = R16List 
Eax,Ecx,Edx,Ebx,Esp,Ebp,Esi,Edi         = R32List 
ES, CS, SS, DS, FS, GS                  = SegList 
CR0,CR1,CR2,CR3,CR4,CR5,CR6,CR7         = CntList 
DR0,DR1,DR2,DR3,DR4,DR5,DR6,DR7         = DbgList 
ST0,ST1,ST2,ST3,ST4,ST5,ST6,ST7         = FPUList 
MM0,MM1,MM2,MM3,MM4,MM5,MM6,MM7         = MMXList 
XMM0,XMM1,XMM2,XMM3,XMM4,XMM5,XMM6,XMM7 = XMMList 
Mb,Mw,Md,Mf,Mq,Mt,Mdq                   = MSList  
OF,DF,SF,ZF,AF,PF,CF                    = FlagList


#: Maps flags to their bit positions in EFLAGS.
FlagToEFLAGSPosition = dict() 

FlagToEFLAGSPosition[OF] = 11
FlagToEFLAGSPosition[DF] = 10
FlagToEFLAGSPosition[SF] = 7
FlagToEFLAGSPosition[ZF] = 6
FlagToEFLAGSPosition[AF] = 4
FlagToEFLAGSPosition[PF] = 2
FlagToEFLAGSPosition[CF] = 0

mneme, MnemList = enum_lower("Mnem", 
['Aaa', 'Aad', 'Aam', 'Aas', 'Adc', 'Add', 'Addpd', 'Addps', 'Addsd', 'Addss',
'Addsubpd', 'Addsubps', 'And', 'Andnpd', 'Andnps', 'Andpd', 'Andps', 'Arpl',
'Blendpd', 'Blendps', 'Blendvpd', 'Blendvps', 'Bound', 'Bsf', 'Bsr', 'Bswap',
'Bt', 'Btc', 'Btr', 'Bts', 'Call', 'CallF', 'Cbw', 'Cdq', 'Clc', 'Cld',
'Clflush', 'Cli', 'Clts', 'Cmc', 'Cmova', 'Cmovae', 'Cmovb', 'Cmovbe', 'Cmovg',
'Cmovge', 'Cmovl', 'Cmovle', 'Cmovno', 'Cmovnp', 'Cmovns', 'Cmovnz', 'Cmovo',
'Cmovp', 'Cmovs', 'Cmovz', 'Cmp', 'Cmppd', 'Cmpps', 'Cmpsb', 'Cmpsd', 'Cmpss',
'Cmpsw', 'Cmpxchg', 'Cmpxchg8b', 'Comisd', 'Comiss', 'Cpuid', 'Crc32',
'Cvtdq2pd', 'Cvtdq2ps', 'Cvtpd2dq', 'Cvtpd2pi', 'Cvtpd2ps', 'Cvtpi2pd',
'Cvtpi2ps', 'Cvtps2dq', 'Cvtps2pd', 'Cvtps2pi', 'Cvtsd2si', 'Cvtsd2ss',
'Cvtsi2sd', 'Cvtsi2ss', 'Cvtss2sd', 'Cvtss2si', 'Cvttpd2dq', 'Cvttpd2pi',
'Cvttps2dq', 'Cvttps2pi', 'Cvttsd2si', 'Cvttss2si', 'Cwd', 'Cwde', 'Daa', 'Das',
'Dec', 'Div', 'Divpd', 'Divps', 'Divsd', 'Divss', 'Dppd', 'Dpps', 'Emms',
'Enter', 'Extractps', 'F2xm1', 'Fabs', 'Fadd', 'Faddp', 'Fbld', 'Fbstp', 'Fchs',
'Fclex', 'Fcmovb', 'Fcmovbe', 'Fcmove', 'Fcmovnb', 'Fcmovnbe', 'Fcmovne',
'Fcmovnu', 'Fcmovu', 'Fcom', 'Fcomi', 'Fcomip', 'Fcomp', 'Fcompp', 'Fcos',
'Fdecstp', 'Fdiv', 'Fdivp', 'Fdivr', 'Fdivrp', 'Ffree', 'Fiadd', 'Ficom',
'Ficomp', 'Fidiv', 'Fidivr', 'Fild', 'Fimul', 'Fincstp', 'Finit', 'Fist',
'Fistp', 'Fisttp', 'Fisub', 'Fisubr', 'Fld', 'Fld1', 'Fldcw', 'Fldenv',
'Fldl2e', 'Fldl2t', 'Fldlg2', 'Fldln2', 'Fldpi', 'Fldz', 'Fmul', 'Fmulp',
'Fnop', 'Fpatan', 'Fprem', 'Fprem1', 'Fptan', 'Frndint', 'Frstor', 'Fsave',
'Fscale', 'Fsin', 'Fsincos', 'Fsqrt', 'Fst', 'Fstcw', 'Fstenv', 'Fstp', 'Fstsw',
'Fsub', 'Fsubp', 'Fsubr', 'Fsubrp', 'Ftst', 'Fucom', 'Fucomi', 'Fucomip',
'Fucomp', 'Fucompp', 'Fxam', 'Fxch', 'Fxrstor', 'Fxsave', 'Fxtract', 'Fyl2x',
'Fyl2xp1', 'Getsec', 'Haddpd', 'Haddps', 'Hlt', 'Hsubpd', 'Hsubps', 'Icebp',
'Idiv', 'Imul', 'In', 'Inc', 'Insb', 'Insd', 'Insertps', 'Insw', 'Int', 'Int3',
'Into', 'Invd', 'Invlpg', 'Iretd', 'Iretw', 'Ja', 'Jae', 'Jb', 'Jbe', 'Jcxz',
'Jecxz', 'Jg', 'Jge', 'Jl', 'Jle', 'Jmp', 'JmpF', 'Jno', 'Jnp', 'Jns', 'Jnz',
'Jo', 'Jp', 'Js', 'Jz', 'Lahf', 'Lar', 'Lddqu', 'Ldmxcsr', 'Lds', 'Lea',
'Leave', 'Les', 'Lfence', 'Lfs', 'Lgdt', 'Lgs', 'Lidt', 'Lldt', 'Lmsw', 'Lodsb',
'Lodsd', 'Lodsw', 'Loop', 'Loopnz', 'Loopz', 'Lsl', 'Lss', 'Ltr', 'Maskmovdqu',
'Maskmovq', 'Maxpd', 'Maxps', 'Maxsd', 'Maxss', 'Mfence', 'Minpd', 'Minps',
'Minsd', 'Minss', 'Monitor', 'Mov', 'Movapd', 'Movaps', 'Movd', 'Movddup',
'Movdq2q', 'Movdqa', 'Movdqu', 'Movhlps', 'Movhpd', 'Movhps', 'Movlhps',
'Movlpd', 'Movlps', 'Movmskpd', 'Movmskps', 'Movntdq', 'Movntdqa', 'Movnti',
'Movntpd', 'Movntps', 'Movntq', 'Movq', 'Movq2dq', 'Movsb', 'Movsd', 'Movshdup',
'Movsldup', 'Movss', 'Movsw', 'Movsx', 'Movupd', 'Movups', 'Movzx', 'Mpsadbw',
'Mul', 'Mulpd', 'Mulps', 'Mulsd', 'Mulss', 'Mwait', 'Neg', 'Nop', 'Not', 'Or',
'Orpd', 'Orps', 'Out', 'Outsb', 'Outsd', 'Outsw', 'Pabsb', 'Pabsd', 'Pabsw',
'Packssdw', 'Packsswb', 'Packusdw', 'Packuswb', 'Paddb', 'Paddd', 'Paddq',
'Paddsb', 'Paddsw', 'Paddusb', 'Paddusw', 'Paddw', 'Palignr', 'Pand', 'Pandn',
'Pause', 'Pavgb', 'Pavgw', 'Pblendvb', 'Pblendw', 'Pcmpeqb', 'Pcmpeqd',
'Pcmpeqq', 'Pcmpeqw', 'Pcmpestri', 'Pcmpestrm', 'Pcmpgtb', 'Pcmpgtd', 'Pcmpgtq',
'Pcmpgtw', 'Pcmpistri', 'Pcmpistrm', 'Pextrb', 'Pextrd', 'Pextrw', 'Phaddd',
'Phaddsw', 'Phaddw', 'Phminposuw', 'Phsubd', 'Phsubsw', 'Phsubw', 'Pinsrb',
'Pinsrd', 'Pinsrw', 'Pmaddubsw', 'Pmaddwd', 'Pmaxsb', 'Pmaxsd', 'Pmaxsw',
'Pmaxub', 'Pmaxud', 'Pmaxuw', 'Pminsb', 'Pminsd', 'Pminsw', 'Pminub', 'Pminud',
'Pminuw', 'Pmovmskb', 'Pmovsxbd', 'Pmovsxbq', 'Pmovsxbw', 'Pmovsxdq',
'Pmovsxwd', 'Pmovsxwq', 'Pmovzxbd', 'Pmovzxbq', 'Pmovzxbw', 'Pmovzxdq',
'Pmovzxwd', 'Pmovzxwq', 'Pmuldq', 'Pmulhrsw', 'Pmulhuw', 'Pmulhw', 'Pmulld',
'Pmullw', 'Pmuludq', 'Pop', 'Popad', 'Popaw', 'Popcnt', 'Popfd', 'Popfw', 'Por',
'Prefetchnta', 'Prefetcht0', 'Prefetcht1', 'Prefetcht2', 'Psadbw', 'Pshufb',
'Pshufd', 'Pshufhw', 'Pshuflw', 'Pshufw', 'Psignb', 'Psignd', 'Psignw', 'Pslld',
'Pslldq', 'Psllq', 'Psllw', 'Psrad', 'Psraw', 'Psrld', 'Psrldq', 'Psrlq',
'Psrlw', 'Psubb', 'Psubd', 'Psubq', 'Psubsb', 'Psubsw', 'Psubusb', 'Psubusw',
'Psubw', 'Ptest', 'Punpckhbw', 'Punpckhdq', 'Punpckhqdq', 'Punpckhwd',
'Punpcklbw', 'Punpckldq', 'Punpcklqdq', 'Punpcklwd', 'Push', 'Pushad', 'Pushaw',
'Pushfd', 'Pushfw', 'Pxor', 'Rcl', 'Rcpps', 'Rcpss', 'Rcr', 'Rdmsr', 'Rdpmc',
'Rdtsc', 'Ret', 'Retf', 'Rol', 'Ror', 'Roundpd', 'Roundps', 'Roundsd',
'Roundss', 'Rsm', 'Rsqrtps', 'Rsqrtss', 'Sahf', 'Sal', 'Salc', 'Sar', 'Sbb',
'Scasb', 'Scasd', 'Scasw', 'Seta', 'Setae', 'Setb', 'Setbe', 'Setg', 'Setge',
'Setl', 'Setle', 'Setno', 'Setnp', 'Setns', 'Setnz', 'Seto', 'Setp', 'Sets',
'Setz', 'Sfence', 'Sgdt', 'Shl', 'Shld', 'Shr', 'Shrd', 'Shufpd', 'Shufps',
'Sidt', 'Sldt', 'Smsw', 'Sqrtpd', 'Sqrtps', 'Sqrtsd', 'Sqrtss', 'Stc', 'Std',
'Sti', 'Stmxcsr', 'Stosb', 'Stosd', 'Stosw', 'Str', 'Sub', 'Subpd', 'Subps',
'Subsd', 'Subss', 'Syscall', 'Sysenter', 'Sysexit', 'Sysret', 'Test', 'Ucomisd',
'Ucomiss', 'Ud2', 'Unpckhpd', 'Unpckhps', 'Unpcklpd', 'Unpcklps', 'Verr',
'Verw', 'Vmcall', 'Vmclear', 'Vmlaunch', 'Vmptrld', 'Vmptrst', 'Vmread',
'Vmresume', 'Vmwrite', 'Vmxoff', 'Vmxon', 'Wait', 'Wbinvd', 'Wrmsr', 'Xadd',
'Xlat', 'Xchg', 'Xor', 'Xorpd', 'Xorps'])

MnemElt = mneme #: `type` object for mnemonics
mnem_tuple = tuple(MnemList)

(Aaa, Aad, Aam, Aas, Adc, Add, Addpd, Addps, Addsd, Addss, Addsubpd, Addsubps,
And, Andnpd, Andnps, Andpd, Andps, Arpl, Blendpd, Blendps, Blendvpd, Blendvps,
Bound, Bsf, Bsr, Bswap, Bt, Btc, Btr, Bts, Call, CallF, Cbw, Cdq, Clc, Cld,
Clflush, Cli, Clts, Cmc, Cmova, Cmovae, Cmovb, Cmovbe, Cmovg, Cmovge, Cmovl,
Cmovle, Cmovno, Cmovnp, Cmovns, Cmovnz, Cmovo, Cmovp, Cmovs, Cmovz, Cmp, Cmppd,
Cmpps, Cmpsb, Cmpsd, Cmpss, Cmpsw, Cmpxchg, Cmpxchg8b, Comisd, Comiss, Cpuid,
Crc32, Cvtdq2pd, Cvtdq2ps, Cvtpd2dq, Cvtpd2pi, Cvtpd2ps, Cvtpi2pd, Cvtpi2ps,
Cvtps2dq, Cvtps2pd, Cvtps2pi, Cvtsd2si, Cvtsd2ss, Cvtsi2sd, Cvtsi2ss, Cvtss2sd,
Cvtss2si, Cvttpd2dq, Cvttpd2pi, Cvttps2dq, Cvttps2pi, Cvttsd2si, Cvttss2si, Cwd,
Cwde, Daa, Das, Dec, Div, Divpd, Divps, Divsd) = mnem_tuple[0:100]

(Divss, Dppd, Dpps, Emms, Enter, Extractps, F2xm1, Fabs, Fadd, Faddp, Fbld,
Fbstp, Fchs, Fclex, Fcmovb, Fcmovbe, Fcmove, Fcmovnb, Fcmovnbe, Fcmovne,
Fcmovnu, Fcmovu, Fcom, Fcomi, Fcomip, Fcomp, Fcompp, Fcos, Fdecstp, Fdiv, Fdivp,
Fdivr, Fdivrp, Ffree, Fiadd, Ficom, Ficomp, Fidiv, Fidivr, Fild, Fimul, Fincstp,
Finit, Fist, Fistp, Fisttp, Fisub, Fisubr, Fld, Fld1, Fldcw, Fldenv, Fldl2e,
Fldl2t, Fldlg2, Fldln2, Fldpi, Fldz, Fmul, Fmulp, Fnop, Fpatan, Fprem, Fprem1,
Fptan, Frndint, Frstor, Fsave, Fscale, Fsin, Fsincos, Fsqrt, Fst, Fstcw, Fstenv,
Fstp, Fstsw, Fsub, Fsubp, Fsubr, Fsubrp, Ftst, Fucom, Fucomi, Fucomip, Fucomp,
Fucompp, Fxam, Fxch, Fxrstor, Fxsave, Fxtract, Fyl2x, Fyl2xp1, Getsec, Haddpd,
Haddps, Hlt, Hsubpd, Hsubps) = mnem_tuple[100:200]

(Icebp, Idiv, Imul, In, Inc, Insb, Insd, Insertps, Insw, Int, Int3, Into, Invd, Invlpg,
Iretd, Iretw, Ja, Jae, Jb, Jbe, Jcxz, Jecxz, Jg, Jge, Jl, Jle, Jmp, JmpF, Jno,
Jnp, Jns, Jnz, Jo, Jp, Js, Jz, Lahf, Lar, Lddqu, Ldmxcsr, Lds, Lea, Leave, Les,
Lfence, Lfs, Lgdt, Lgs, Lidt, Lldt, Lmsw, Lodsb, Lodsd, Lodsw, Loop, Loopnz,
Loopz, Lsl, Lss, Ltr, Maskmovdqu, Maskmovq, Maxpd, Maxps, Maxsd, Maxss, Mfence,
Minpd, Minps, Minsd, Minss, Monitor, Mov, Movapd, Movaps, Movd, Movddup,
Movdq2q, Movdqa, Movdqu, Movhlps, Movhpd, Movhps, Movlhps, Movlpd, Movlps,
Movmskpd, Movmskps, Movntdq, Movntdqa, Movnti, Movntpd, Movntps, Movntq, Movq,
Movq2dq, Movsb, Movsd, Movshdup, Movsldup)  = mnem_tuple[200:300]

(Movss, Movsw, Movsx, Movupd, Movups, Movzx, Mpsadbw, Mul, Mulpd, Mulps, Mulsd, 
Mulss, Mwait, Neg, Nop, Not, Or, Orpd, Orps, Out, Outsb, Outsd, Outsw, Pabsb, Pabsd, 
Pabsw, Packssdw, Packsswb, Packusdw, Packuswb, Paddb, Paddd, Paddq, Paddsb, Paddsw, 
Paddusb, Paddusw, Paddw, Palignr, Pand, Pandn, Pause, Pavgb, Pavgw, Pblendvb, Pblendw,
Pcmpeqb, Pcmpeqd, Pcmpeqq, Pcmpeqw, Pcmpestri, Pcmpestrm, Pcmpgtb, Pcmpgtd,
Pcmpgtq, Pcmpgtw, Pcmpistri, Pcmpistrm, Pextrb, Pextrd, Pextrw, Phaddd, Phaddsw,
Phaddw, Phminposuw, Phsubd, Phsubsw, Phsubw, Pinsrb, Pinsrd, Pinsrw, Pmaddubsw,
Pmaddwd, Pmaxsb, Pmaxsd, Pmaxsw, Pmaxub, Pmaxud, Pmaxuw, Pminsb, Pminsd, Pminsw,
Pminub, Pminud, Pminuw, Pmovmskb, Pmovsxbd, Pmovsxbq, Pmovsxbw, Pmovsxdq,
Pmovsxwd, Pmovsxwq, Pmovzxbd, Pmovzxbq, Pmovzxbw, Pmovzxdq, Pmovzxwd, Pmovzxwq,
Pmuldq, Pmulhrsw) = mnem_tuple[300:400]

(Pmulhuw, Pmulhw, Pmulld, Pmullw, Pmuludq, Pop, Popad, Popaw, Popcnt, Popfd, Popfw, 
Por, Prefetchnta, Prefetcht0, Prefetcht1, Prefetcht2, Psadbw, Pshufb, Pshufd, 
Pshufhw, Pshuflw, Pshufw, Psignb, Psignd, Psignw, Pslld, Pslldq, Psllq, Psllw, 
Psrad, Psraw, Psrld, Psrldq, Psrlq, Psrlw, Psubb, Psubd, Psubq, Psubsb, Psubsw, 
Psubusb, Psubusw, Psubw, Ptest, Punpckhbw, Punpckhdq, Punpckhqdq, Punpckhwd, 
Punpcklbw, Punpckldq, Punpcklqdq, Punpcklwd, Push, Pushad, Pushaw, Pushfd, Pushfw, 
Pxor, Rcl, Rcpps, Rcpss, Rcr, Rdmsr, Rdpmc, Rdtsc, Ret, Retf, Rol, Ror, Roundpd, 
Roundps, Roundsd, Roundss, Rsm, Rsqrtps, Rsqrtss, Sahf, Sal, Salc, Sar, Sbb, Scasb, 
Scasd, Scasw, Seta, Setae, Setb, Setbe, Setg, Setge, Setl, Setle, Setno, Setnp, Setns, 
Setnz, Seto, Setp, Sets, Setz) = mnem_tuple[400:500]

(Sfence,Sgdt, Shl, Shld, Shr, Shrd, Shufpd, Shufps, Sidt, Sldt, Smsw, Sqrtpd, Sqrtps, 
Sqrtsd, Sqrtss, Stc, Std, Sti, Stmxcsr, Stosb, Stosd,
Stosw, Str, Sub, Subpd, Subps, Subsd, Subss, Syscall, Sysenter, Sysexit, Sysret,
Test, Ucomisd, Ucomiss, Ud2, Unpckhpd, Unpckhps, Unpcklpd, Unpcklps, Verr, Verw,
Vmcall, Vmclear, Vmlaunch, Vmptrld, Vmptrst, Vmread, Vmresume, Vmwrite, Vmxoff,
Vmxon, Wait, Wbinvd, Wrmsr, Xadd, Xlat, Xchg, Xor, Xorpd, Xorps) = mnem_tuple[500:]

X86_LAST_MNEMONIC = Xorps.IntValue()