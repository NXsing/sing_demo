import pickle

vVar=pickle.load( open( "SOURCE/_var.pick", "rb" ) )
vRoom=pickle.load( open( "SOURCE/_room.pick", "rb" ) )

aR=list(filter(lambda x: x.later==True, vRoom))
bR=list(filter(lambda x: x.later==False, vRoom))
vRoom=bR+aR

# обработка "виртуальной команды" next
# преобразование её в goto roomname_следующей_комнаты
if len(vRoom)>1:
	for RID in range(0,len(vRoom)):
		R=vRoom[RID]
		for AID in range(0,len(R.vAct)):
			A=R.vAct[AID]
			for CID in range(0,len(A.vComm)):
				C=A.vComm[CID]
				if C.name=="next":
					if (RID+1)>=(len(vRoom)):
						print("ERR: can't refer to NEXT room")
					else:
						C.name="goto"
						C.arg=vRoom[RID+1].roomname
						print(C)

print(vVar)

actLater=[]

# счетчик инструкций и функция ip() - только для отладки
instruction=0

# переменная хранит итоговый исходный код
total=""

vTotal=[]


def quote(s):
	return "\""+s+"\""

def skobe(a=""):
	return "("+a+")"

def call(fname,a=None,b=None):
	global vTotal
	
	vTotal.append((fname,a,b))
	#~ if a!=None and b!=None:
		#~ vTotal.append((fname,a,b))
	
	#~ if a!=None and b==None:
		#~ vTotal.append((fname,a))
	#~ if a==None and b==None:
		#~ vTotal.append((fname))


def ip(val):
	global instruction
	instruction+=val

def declvar(varname,val):
	if val==True:
		call("byte1",varname)
	else:
		call("byte0",varname)
	
	ip(+1)

def rest():
	call("rest")
	ip(+1)
	
def condjmp(s):
	call("condjmp",s)
	ip(+1+3)

def lab(s):
	call("label",s)

def setName(s):
	call("setname",s)
	ip(+1+3)

import hashlib

def room(R):
	lab(R.roomname)
	setName(R.anchor)

#генерируем блок переменных
rest()
condjmp("mainprogram")
for V in vVar:
	declvar(V,vVar[V])
lab("mainprogram")
rest()




def onv(s):
	call("onv",s)
	ip(+1+3)
	
def offv(s):
	call("offv",s)
	ip(+1+3)

def condtext(CT):
	call("condtxt",CT.anchor)
	ip(+1+3)

messXanchor={}

def condmes(CT):
	call("condmes",messXanchor[CT])
	ip(+1+3)

def nop():
	call("nop")
	ip(+1)


def interpCond(A):
	rest()
	if A.trueVec==None and A.falseVec==None:
		onv("always")
	
	for ct in A.trueVec:
		onv(ct)
	for ct in A.falseVec:
		offv(ct)


def condset(s):
	call("condset",s)
	ip(+1+3)
	
def condunset(s):
	call("condunset",s)
	ip(+1+3)

def interpComm(A):
	for C in A.vComm:
		nam=C.name.strip()
		print(nam)
		if "goto"==nam:
			condjmp(C.arg)
		if "nothing"==nam:
			nop()
		if "set"==nam:
			condset(C.arg)
		if "unset"==nam:
			condunset(C.arg)
		if "return"==nam:
			condret()
		if "mes"==nam:
			condmes(C.arg)



def text(A):
	interpCond(A)
	condtext(A)
	interpComm(A)


def condact(A):
	call("condact",A.anchor)
	ip(+1+3)

def act(A):
	interpCond(A)
	condact(A)
	
	global actLater
	actLater.append(A)


def waitKey():
	call("waitkey")
	ip(+1)
	
def condret():
	call("condret")
	ip(+1)

def eq(s):
	call("eq",s)
	ip(+1+3)

def end():
	waitKey()
	
	global actLater
	for A in actLater:
		rest()
		eq(A.anchor)
		print(A)
		interpComm(A)
	
	actLater.clear()





def UUID():
	import os
	# генерация случайных строк вида f114b8379a7eebf2870a1ec9770c139a
	return hashlib.md5(os.urandom(32)).hexdigest().lower()

for R in vRoom:
	room(R)
	rest()
	
	#объявление текстов в комнате
	condjmp(R.roomname+"_decl")
	for T in (R.vText+R.vAct):
		call("decl",T.anchor,T.text)
		ip(+len(T.text)+1)
	
	
	# объявление данных для команды mes
	for T in (R.vText+R.vAct):
		for C in T.vComm:
			print(dir(C))
			if C.name=="mes":
				messXanchor[C.arg]=UUID()
				call("decl", messXanchor[C.arg] ,C.arg)
	
	call("decl",R.anchor,R.roomname)
	lab(R.roomname+"_decl")
		
	for T in R.vText:
		text(T)
			
	for A in R.vAct:
		act(A)

	end()

import sys
for x in vTotal:
	sys.stdout.write(x[0]+" ")
	if x[1]:
		sys.stdout.write(x[1]+" ")
	if x[2]:
		sys.stdout.write(x[2]+" ")
	print("")

import pickle

pickle.dump( vTotal, open( "SOURCE/_quest.pick", "wb" ) )

