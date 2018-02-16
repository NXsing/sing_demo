import os, hashlib
import pickle
def UUID():
	# генерация случайных строк вида f114b8379a7eebf2870a1ec9770c139a
	return hashlib.md5(os.urandom(32)).hexdigest().lower()

# не забываем про команду next
# и про r() - можно указывать комнату без имени - удобно для последовательных комнат

# исправил работу условий в интерпретаторе и веб-версии

def d(varname,varval=False):
	global vVar
	
	varname=varname.lower()
	
	if varname in vVar.keys():
		raise Exception("ERROR: declvar: var "+varname+" already there")
	else:
		vVar[varname]=varval

curRoom=None
vRoom=[]
vVar={}

d("never",False)
d("always",True)

class Command:
	def __repr__(self):
		return "<Command:'{}', arg:'{}'>".format(self.name,self.arg)
	def __init__(self,s):
		s=s.strip()
		
		#неправильно - должно быть разделение до
		com_arg=s.split(" ")
		
		com=com_arg[0]
		arg=None
		
		if len(com_arg)==1:
			self.name=com
			self.arg=None
		
		if len(com_arg)>1:
			self.name=com
			self.arg=" ".join(com_arg[1:])
		
		#print(self)
		
		if self.name==None and self.arg==None:
			print('Wrong command : '+s)

class Condition:
	def __repr__(self):
		return "<Cond:'{}', arg:'{}'>".format(self.cvar,self.ctype)
		
	def __init__(self,s):
		#условная переменная
		self.cvar=None
		
		#тип условия
		self.ctype=None
		
		s=s.strip()
		
		if s.startswith("ifset"):
			self.cvar=s.replace("ifset","").strip()
			self.ctype="positive"
		
		if s.startswith("ifnot"):
			self.cvar=s.replace("ifnot ","").strip()
			self.ctype="negative"
				
		if s=="always":
			self.ctype="always"
			self.cvar="always"

		if s=="never":
			self.ctype="never"
			self.cvar="never"
		
		#print(self)
		#print("COND",[self.ctype,self.cvar],s)

# активный элемент комнаты - строка текста, действие
class Atom:
	def __repr__(self):
		res=""
		res+="\t<'{}'\n".format(self.text)
		
		for x in self.vCond:
			res+="\t\t"+str(x)+"\n"
		
		for x in self.vComm:
			res+="\t\t"+str(x)+"\n"
		
		return res
		
	def __init__(self,text,cond=None,comm=None):
		self.text=text.replace("\n","\\n").replace("\r","\\r")
		
		self.anchor=UUID()
		
		self.vCond=list(map(lambda x: Condition(x.strip().lower()), cond.split(";") ))
		self.vComm=list(map(lambda x: Command(x.strip().lower()), comm.split(";") ))
		
		for cond in self.vCond:
			if cond.ctype=="always" or cond.ctype=="never":
				self.vCond=[cond]
				break
		
		self.trueVec=list(map(lambda z: z.cvar, filter(lambda x: x.ctype=="always" or x.ctype=="positive", self.vCond)))
		self.falseVec=list(map(lambda z: z.cvar, filter(lambda x: x.ctype=="negative" or x.ctype=="never", self.vCond)))
		#print(self)



class Room:
	def __repr__(self):
		res="<Room:'{}', anchor:'{}'\n".format(self.roomname,self.anchor)
		
		for x in self.vText:
			res+="TEXT"+str(x)
			
		for x in self.vAct:
			res+="ACT"+str(x)
	
		return res
		
	def __init__(self, s):
		s=s.lower()
		
		self.anchor=UUID()
		self.later=False
		self.roomname=s
		
		self.vText=[]
		self.vAct=[]

class Var:
	def __init__(self,vname,vval):
		vname=vname.lower()
		self.name=vname
		self.val=vval


	
	

# обяъвление комнаты
# вызов может быть пустым
def r(s=None):
	global curRoom
	if s==None:
		curRoom=Room("_rname_"+UUID())
	else:
		curRoom=Room(s)

# добавление действия в комнату
# для действия, у аргументов, иной порядок - команда первична
def a(text,comm="nothing",cond="always"):
	global curRoom
	curRoom.vAct.append(Atom(text,cond,comm))

# добавление элемента текста в комнату
# условие первично
def t(text,cond="always",comm="nothing"):
	global curRoom
	curRoom.vText.append(Atom(text,cond,comm))

def e():
	# добавляем комнату в глобальный список комнат
	global curRoom
	global vRoom
	global vVar
	print(curRoom)
	vRoom.append(curRoom)
	curRoom=None
	
	# добавляем переменные комнаты в глобальный хеш переменных
	# инициализируем в False
	
	#если переменная не инициализирована через d() со значением иди не объявлена ранее,
	# инициализируем её в false
	for x in collectVariables():
		if not x in vVar:
			vVar[x]=False
	
	print("Total variables: \n\t",vVar)
	
	# из-за abay - не сейчас, а конструкторе, после расщепления
	#выполнить преобразование команды next в goto послеующей комнаты "goto "+R.roomname
	#~ if len(vRoom)>2:
		#~ for RID in range(0,len(vRoom)):
			#~ R=vRoom[RID]
			#~ for AID in range(0,len(R.vAct)):
				#~ A=R.vAct[AID]
				#~ for CID in range(0,len(A.vComm)):
					#~ C=A.vComm[CID]
					#~ if C.name=="next":
						#~ if RID+1>len(vRoom)-1:
							#~ print("ERR: can't refer to NEXT room")
						#~ else:
							#~ C.name="goto"
							#~ C.arg=vRoom[RID+1].roomname
							#~ print(C)
			
	with open('SOURCE/_room.pick', 'wb') as f:
		pickle.dump(vRoom, f)
	
	#print(vVar)
	with open('SOURCE/_var.pick', 'wb') as f:
		pickle.dump(vVar, f)

def img(s):
	t(""" <img src="{}" style="width:100%"  class="img-fluid" alt="s"> """.format(s))


def abay(_act,_mess,_cond="always",_code="nothing"):
	global curRoom
	global vRoom
	
	
	print("act: ",_act, " mess: ",_mess, " cond: ", _cond, " comm: ",_code)
	
	rname=UUID()
	_cond=_cond.lower()
	_code=_code.lower()
	
	R=Room(rname)
	R.later=True
	a(_act, "goto "+rname, _cond)
	
	R.vText.append(Atom(_mess,"always","nothing"))
	R.vAct.append(Atom("Обратно","always",_code+";return"))
	
	vRoom.append(R)

def collectVariables():
	global vRoom
	
	# объявляем набор уникальных значений, который будет хранить набор уникальных значений(в set'е значения не повторяются)
	varset=set()
	
	# собираем имена переменных по всем комнатам, по всем условиям и командам
	for R in vRoom:
		vAtom=[]
		vAtom+=R.vText
		vAtom+=R.vAct
		
		for A in vAtom:
			#print("tt: ",A.text, A.trueVec,A.falseVec)
			for V in A.trueVec:
				varset.add(V)
			#print("falsevec: ",A.falseVec)
			for V in A.falseVec:
				varset.add(V)
			
			for V in A.vComm:
				if(V.name=="set"):
					varset.add(V.arg)
				if(V.name=="unset"):
					varset.add(V.arg)
	# исключаем не-имена переменных
	# используя правило Де Моргана :)
	res=list(filter(lambda x: x!="always" and x!="never", list(varset)))
	#print("roomvars",res)
	return res



def rb(rname,rtxt,rcom="nothing"):
	r(rname)
	t(rtxt)
	a("Обратно","return"+";"+rcom)
	e()


def isCondition(x):
	if x==None:
		return False
	return ("ifset" in x) or ("ifnot" in x) or ("always" in x) or ("never" in x)

def isCommand(x):
	if x==None:
		return False
	return (("set" in x) and (not "ifset" in x)) or ("next" in x) or ("unset" in x) or ("goto" in x) or ("nothing" in x) or ("return" in x)
	

# сделать x более простым и умным(учитывающим abay, t, a разных формулировок)

def x(text,q1=None,q2=None):
	presentQ1=(q1!=None)
	presentQ2=(q2!=None)
	
	
	
	condQ1=isCondition(q1)
	condQ2=isCondition(q2)
	
	commQ1=isCommand(q1)
	commQ2=isCommand(q2)
	
	textQ1=(not condQ1) and (not commQ1)
	
	if textQ1 and commQ2:
		abay(text,q1,"always",q2)
	
	if (not presentQ1) and (not presentQ2):
		t(text)
	
	if presentQ1 and (not presentQ2):
		if condQ1:
			t(text,q1) #~ a(text,"nothing",q1)
		if commQ1:
			a(text,q1)
		
	if presentQ1 and presentQ2:
		if condQ1 and condQ2:
			raise("Wrong x: double cond")
		if commQ1 and commQ2:
			raise("Wrong x: double comm")
		if condQ1 and commQ2:
			a(text,q2,q1) #commands first
		if commQ1 and condQ2:
			a(text,q1,q2)
	#учитывая что text с коммандой - редкость




#~ def chain(lst):
	#~ for phrase in lst:
		#~ r()
		#~ x(phrase)
		#~ x("далее","next")
		#~ e()

#~ r()
#~ x("hello world")
#~ x("далее","next")
#~ e()

#~ chain(["я сел","я выпил чай","я задумался","я встал"])

#~ r()
#~ x("hi")
#~ e()
